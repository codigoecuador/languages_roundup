#!/usr/bin/env python3
# coding=utf-8
"""A simple example demonstrating how to use Argparse to support subcommands.
This example shows an easy way for a single command to have many subcommands, each of which takes different arguments
and provides separate contextual help.
"""
import argparse
import cmd2
import newspaper as np
from dateutil.parser import parse
from roundup_db1 import Entry, Category, Keyword, Publication, Author, Section, DataAccessLayer
import app
import sys, glob, datetime, os
import BTCInput2 as btc
import itertools as it
import warnings, functools, pprint

###SEARCH COMMAND

# create the top-level parser for the search command
search_parser = argparse.ArgumentParser()
search_subparsers = search_parser.add_subparsers(title='subcommands', help='subcommand help')

# create the parser for the "entry" subcommand
parser_entry = search_subparsers.add_parser('entry', help='entry help')
parser_entry.add_argument('-id', '--entry_id', help='id of the entry')
parser_entry.add_argument('-idr', '--id_range', nargs=2,
                              help='minimum and maximum ids', )
parser_entry.add_argument('-d', '--date', help='date of entry')
parser_entry.add_argument('-l', '--url', help='article_url')
parser_entry.add_argument('-t', '--title', nargs='*', help='entry name')
parser_entry.add_argument('-dr', '--date_range', nargs=2, help='start date, end date')
parser_entry.add_argument('-c', '--category_id', help='category id')
parser_entry.add_argument('-desc',  '--description', nargs='*',
                           help='article description (optional)')

#create the parser for the "category" subcommand
parser_category = search_subparsers.add_parser('category', help='category help')
parser_category.add_argument('-id', '--category_id', help='category id')
parser_category.add_argument('-n', '--category_name', nargs='*', help='category name e.g. Python')
parser_category.add_argument('-s', '--section_id', help='section id')

#create the parser for the "keyword" subcommand

parser_keyword = search_subparsers.add_parser('keyword', help='keyword help')
parser_keyword.add_argument('-id', '--keyword_id', help='keyword id')
parser_keyword.add_argument('-w', '--word', nargs='*', help='keyword text e.g. mapreduce')

#create the parser for the "section" subcommand
parser_section = search_subparsers.add_parser('section', help='section help')
parser_section.add_argument('-id', '--section_id', help='section id')
parser_section.add_argument('-n', '--name', help='section name')

###ADD COMMAND
add_parser = argparse.ArgumentParser()
add_subparsers = add_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "entry" subcommand

parser_add_entry = add_subparsers.add_parser('entry', help='entry help')
parser_add_entry.add_argument('-l', '--url', help='url of article')
parser_add_entry.add_argument('-c', '--category_id', help='category id e.g. Comoros is 1')
parser_add_entry.add_argument('-d','--date', help='article date')
parser_add_entry.add_argument('-desc',  '--description', nargs='*',
                           help='article description (optional)')

#create the parser for the "category" subcommand

parser_add_cat = add_subparsers.add_parser('category', help='category help')
parser_add_cat.add_argument('-n', '--name', nargs='*', help='category name e.g. Python')
parser_add_cat.add_argument('-s', '--section_id', help='section id')

#create the parser for the "section" subcommand
parser_add_sec = add_subparsers.add_parser('section', help='section help')
parser_add_sec.add_argument('-n', '--name', nargs='*', help='section name')

#create the parser for the "publication" subcommand
parser_add_pub = add_subparsers.add_parser('publication', help='publication help')
parser_add_pub.add_argument('-t', '--title', nargs='*', help='publication title')
parser_add_pub.add_argument('-l', '--url', help='publication url')

##EDIT COMMAND: parsers for editing Entries, Categories, Sections, Keywords,
#Publications, and Authors

edit_parser = argparse.ArgumentParser() #main parser for the edit command
edit_subparsers = edit_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "entry" subcommand
edit_entry_parser = edit_subparsers.add_parser('entry', help='entry help')
edit_entry_parser.add_argument('-id', '--entry_id', help='the id number of the entry to edit')
edit_entry_parser.add_argument('-t', '--edit_type', nargs='*',
                            help='edit types: title, date, keywords, description, category_id')

#DISPLAY COMMAND: parsers for displaying categories and sections

disp_parser = argparse.ArgumentParser()
disp_subparsers = disp_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the categories subcommand
disp_cat_parser = disp_subparsers.add_parser('categories', help='category help')
disp_cat_parser.add_argument('-s', '--section_id', help='section_id')

#create the parser for the sections subcommand
disp_sec_parser = disp_subparsers.add_parser('sections', help='section help')
disp_sec_parser.add_argument('-s', '--section_id', help='section_id')

#create the parser for the entry_count subcommand

disp_ent_count_parser = disp_subparsers.add_parser('entry_count', help='entry count')
disp_ent_count_parser.add_argument('-d','--date_range', nargs=2, help='start date, end_date')

#create the parser for the entries_needed subcommand

disp_ents_needed_parser = disp_subparsers.add_parser('entries_needed', help='entries needed')
disp_ents_needed_parser.add_argument('-d','--date_range', nargs=2, help='start date, end_date')

##EXPORT COMMAND: parsers for the commands

exp_parser = argparse.ArgumentParser() #different from the exportparser
exp_subparsers = exp_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "docx" subcommand

docx_parser = exp_subparsers.add_parser('docx', help='docx help')
docx_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
docx_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
docx_parser.add_argument('-r', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')

#create the parser for the "html" subcommand

html_parser = exp_subparsers.add_parser('html', help='docx help')
html_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
html_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
html_parser.add_argument('-r', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')
#create the parser for the jsx subcommand

jsx_parser = exp_subparsers.add_parser('jsx', help='docx help')
jsx_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
jsx_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
jsx_parser.add_argument('-r', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')

#create the parser for the jsx_file subcommand

jsx_full_parser = exp_subparsers.add_parser('jsx_file',
                                            help='creates a javascript file for the Codigo Ecuador website')
jsx_full_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
jsx_full_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
jsx_full_parser.add_argument('-r', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')
jsx_full_parser.add_argument('-sec', '--use_sections', help='enter "yes to use the sections"')

#DELETE: parsers for the delete command

class RoundupCMD(cmd2.Cmd):
    """
    Example cmd2 application where we a base command which has a couple subcommands
    and the "sport" subcommand has tab completion enabled.
    """
    def __init__(self):
        super().__init__()
        
    #add item section
    
    def base_ent(self, args):
        '''Adds an article with a single type entry on the command line'''
        if not args.description:
            app.add_entry(session=a.d.session, url=args.url, category_id=args.category_id, date=args.date)
        else:
            app.add_entry(session=a.d.session, url=args.url, category_id=args.category_id,
                   date=args.date, description=' '.join(args.description))
            
    def base_cat(self, args):
        '''Adds a category with a single entry on the command line'''
        app.add_pub_or_cat(new_name=' '.join(args.name),
                           second_item=args.section_id,
                          session=a.d.session, add_type='category')
        
    def base_sect(self, args):
        '''Adds a new section to the roundup'''
        warnings.warn('add_section not yet tested')
        app.add_item(session=a.d.session, search_type='section',
                     new_name=' '.join(args.section_name))
        
    def base_pub(self, args):
        '''Adds a publication to the database'''
        warnings.warn('add publication not yet tested')
        app.add_pub_or_cat(new_name=' '.join(args.title),
                           second_item=args.section_id,
                          session=a.d.session, add_type='publication')
        
    parser_add_entry.set_defaults(func=base_ent)
    parser_add_cat.set_defaults(func=base_cat)
    parser_add_sec.set_defaults(func=base_sect)
    parser_add_pub.set_defaults(func=base_pub)
    
    @cmd2.with_argparser(add_parser)
    def do_add(self, args):
        """Search command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('search')
    
    #search section
    
    def base_category(self, args):
        '''Generic category search function'''
        app.find_category(session=a.d.session, args=args)
        
    def base_entry(self, args):
        '''Generic entry search function'''
        app.find_entry(session=a.d.session, args=args)
    
    def base_section(self, args):
        '''Generic section search function'''
        app.find_section(session=a.d.session, args=args)
        
    def base_keyword(self, args):
        '''Generic keyword search function'''
        app.find_keyword(session=a.d.session, args=args)
        
    parser_category.set_defaults(func=base_category)
    parser_section.set_defaults(func=base_section)
    parser_entry.set_defaults(func=base_entry)
    parser_keyword.set_defaults(func=base_keyword)

    @cmd2.with_argparser(search_parser)
    def do_search(self, args):
        """Search command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('search')
    
    #edit section
    
    def base_edit_entry(self, args):
        '''Generic edit entry function'''
        edit_types = {'all': app.edit_entry, 'description': app.desc_from_input,
                      'category_id': app.cat_id_from_input, 'add keyword': app.add_keyword_to_article,
                    'title': app.name_from_input, 'date': app.date_from_input,
                     'delete keyword': app.delete_entry_keyword}
        if not args.entry_id:
            raise Exception('Must enter entry id')
        if args.entry_id:
            if not args.edit_type:
                app.edit_entry(session=a.d.session, entry_id=args.entry_id)
            else:
                edit_type = ' '.join(args.edit_type).lower() #make into a string with spaces
                edit_types[edit_type](session=a.d.session, entry_id=args.entry_id)
    
    edit_entry_parser.set_defaults(func=base_edit_entry)
    
    @cmd2.with_argparser(edit_parser)
    def do_edit(self, args):
        """Edit command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('edit')
    
    #export section 
    #create export function with html and docx as subcommands
    #jsx function not yet complete
    
    def base_docx(self, args):
        '''Generic export html function'''
        app.create_docx_roundup(args)
    
    def base_html(self, args):
        '''Generic export html function'''
        app.export_html2(session=a.d.session, program=args.filename,
                        start_date=parse(args.date_range[0]).date(),
                         end_date=parse(args.date_range[1]).date(),
                        title=' '.join(args.title))
        
    def base_jsx(self, args):
        '''Generic export jsx function for react'''
        #print(args)
        app.export_jsx(session=a.d.session, program=args.filename,
                        start_date=parse(args.date_range[0]).date(),
                         end_date=parse(args.date_range[1]).date(),
                        title=' '.join(args.title))
    
    def base_full_jsx_file(self, args):
        '''Generic export jsx function for react'''
        print(args)
        #if hasattr(args, 'use_sections'):
        if args.use_sections == None:
            app.exp_full_jsx(session=a.d.session, program=args.filename,
                            start_date=parse(args.date_range[0]).date(),
                             end_date=parse(args.date_range[1]).date(),
                            title=' '.join(args.title), use_sections=False)
            
        elif args.use_sections.lower() == 'yes':
            app.exp_full_jsx(session=a.d.session, program=args.filename,
                            start_date=parse(args.date_range[0]).date(),
                             end_date=parse(args.date_range[1]).date(),
                            title=' '.join(args.title), use_sections=True)
        else:
            raise Exception('use_sections only accepts "yes" as an argument')
   
    docx_parser.set_defaults(func=base_docx)
    html_parser.set_defaults(func=base_html)
    jsx_parser.set_defaults(func=base_jsx)
    jsx_full_parser.set_defaults(func=base_full_jsx_file)
    
    @cmd2.with_argparser(exp_parser)
    def do_export(self, args):
        """Search command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('exp')
            
    #create universal add entry functionality
            
    finalize_parser = argparse.ArgumentParser()
    finalize_parser.add_argument('-d', '--date', help='search a single date')
    finalize_parser.add_argument('-r', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')
    
    
    @cmd2.with_argparser(finalize_parser)
    def do_finalize(self, args):
        '''searches for articles without descriptions and lets user edit them'''
        if args.date:
            app.finalize(session=a.d.session, start_date =args.date, end_date=args.date)
        elif args.date_range:
            app.finalize(session=a.d.session, start_date = args.date_range[0],
                          end_date=args.date_range[1])
        else:
            print('Please enter date or date range. Check help for details')
            return
    
    #display section
    
    def base_entries_needed(self, args):
        '''Displays how many articles you need to get five per category'''
        app.articles_needed(start_date=args.date_range[0],
                            end_date=args.date_range[1],
                            session=a.d.session)
    
    def base_entry_count(self, args):
        '''Displays a count of articles in each category between the specified dates'''
        app.date_range_count(session=a.d.session,
                             start_date = args.date_range[0],
                            end_date = args.date_range[1])
    
    def base_display_sects(self, args):
        '''Generic display categories function'''
        app.display_sections()
    
    def base_display_cats(self, args):
        '''Generic display categories function'''
        try:
            if args.section_id.isnumeric() == True:
                app.display_categories(section_id=args.section_id)
        except AttributeError:
            app.display_categories()
    
    disp_cat_parser.set_defaults(func=base_display_cats)
    disp_sec_parser.set_defaults(func=base_display_sects)
    disp_ent_count_parser.set_defaults(func=base_entry_count)
    disp_ents_needed_parser.set_defaults(func=base_entries_needed)
    
    @cmd2.with_argparser(disp_parser)
    def do_display(self, args):
        """display command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('exp')
        
    count_parser = argparse.ArgumentParser()
    count_parser.add_argument('-d','--date_range', nargs=2, help='start date, end_date')     

    #delete section
    
    del_parser = argparse.ArgumentParser()
    del_parser.add_argument('-ty', '--item_type',
                            help='item type e.g. entry, category, section, author, publication')
    del_parser.add_argument('-id', '--id_value', help='item id')
    
    @cmd2.with_argparser(del_parser)
    def do_delete_item(self, args):
        '''Delete item '''
        warnings.warn('Unified delete function not fully tested')
        app.delete_item(session=a.d.session, model=args.item_type, id_value=args.id_value)
    
    def do_exit(self, arg):
        '''Exits the program, any existing database connections will be closed'''
        a.close()
        print('Exiting Languages Roundup')
        return True
    
if __name__ == '__main__':
    a=app.App()
    a.setup()
    RoundupCMD().cmdloop()