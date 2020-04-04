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
from cmd2 import style, fg, bg

summary_choices = ['yes', 'no']

###SEARCH COMMAND

# create the top-level parser for the search command
search_parser = argparse.ArgumentParser()
search_subparsers = search_parser.add_subparsers(title='subcommands', help='subcommand help')

# create the parser for the "entry" subcommand
parser_entry = search_subparsers.add_parser('entry', help='entry help')
parser_entry.add_argument('-id', '--entry_id', help='id of the entry')
parser_entry.add_argument('-idr', '--id_range', nargs=2,
                              help='minimum and maximum ids')
parser_entry.add_argument('-d', '--date', help='date of entry')
parser_entry.add_argument('-l', '--url', help='article_url')
parser_entry.add_argument('-t', '--title', nargs='*', help='entry name')
parser_entry.add_argument('-dr', '--date_range', nargs=2, help='start date, end date')
parser_entry.add_argument('-c', '--category_id', help='category id')
parser_entry.add_argument('-cn', '--category_name', nargs='*', help='category name')
parser_entry.add_argument('-p', '--publication_id', help='publication id')
parser_entry.add_argument('-pt', '--publication_title', help='publication title')
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

#create the parser for the "publication" subcommand
parser_publication = search_subparsers.add_parser('publication', help='publication help')
parser_publication.add_argument('-id', '--publication_id', help='publication id')
parser_publication.add_argument('-t', '--title', help='publication title')
parser_publication.add_argument('-l', '--url', help='publication url')
#add argument for title


###ADD COMMAND
add_parser = argparse.ArgumentParser()
add_subparsers = add_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "entry" subcommand

parser_add_entry = add_subparsers.add_parser('entry', help='entry help')
parser_add_entry.add_argument('-l', '--url', help='url of article')
parser_add_entry.add_argument('-c', '--category_id', help='category id e.g. Comoros is 1')
parser_add_entry.add_argument('-cn', '--category_name',
                              nargs='*', help='category name e.g. Arts and Culture')
parser_add_entry.add_argument('-d','--date', help='article date')
parser_add_entry.add_argument('-desc',  '--description', nargs='*',
                           help='article description (optional)')
parser_add_entry.add_argument('-md', '--manual_description', help='view summary, enter yes or no',
                          choices=summary_choices)

#create the parser for the "entries" subcommand

parser_add_entries = add_subparsers.add_parser('entries', help='multiple entries')
parser_add_entries.add_argument('-ls', '--links', nargs='*', help='multiple entries help')
parser_add_entries.add_argument('-all', '--complete_info', nargs='*', help='[url]-[category_id]-[date]')
parser_add_entries.add_argument('-c', '--category_id',help='category IDs help')
parser_add_entries.add_argument('-d', '--date', help='multiple articles from the same date')
#add entries

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

#create the parser for the "keyword" subcommand
parser_add_kw = add_subparsers.add_parser(name='keyword', help='keyword help')
parser_add_kw.add_argument('-w', '--word', help='keyword word text')
parser_add_kw.add_argument('-e', '--entry_id', help='entry ID for keyword')

##EDIT COMMAND: parsers for editing Entries, Categories, Sections, Keywords,
#Publications, and Authors

edit_parser = argparse.ArgumentParser() #main parser for the edit command
edit_subparsers = edit_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "entry" subcommand
edit_entry_parser = edit_subparsers.add_parser('entry', help='entry help')
edit_entry_parser.add_argument('-id', '--entry_id', help='the id number of the entry to edit')
edit_entry_parser.add_argument('-t', '--edit_type', nargs='*',
                            help='edit types: title, date, keywords, description, category_id')

#create the parser for the "category" subcommand
#edit_category_parser = edit_subparsers.add_parser('category', help='category help')
#edit_category_parser.add_argument('-id', '--category_id', help='edit category id')
#edit_category_parser.add_argument('-nn', '--new_name', nargs='*', help='new name value')

edit_category_parser = edit_subparsers.add_parser('category', help='category help')
edit_category_parser.add_argument('-id', '--category_id', help='edit category id')
edit_category_parser.add_argument('-idr', '--id_range', help='id range')
#edit_category_parser.add_argument('-nn', '--new_name', nargs='*', help='new name value')
edit_category_parser.add_argument('-n', '--name', nargs='*', help='category name e.g. Python')
edit_category_parser.add_argument('-s', '--section_id', help='section id')

edit_pub_parser = edit_subparsers.add_parser('publication', help='publication help')
edit_pub_parser.add_argument('-id', '--publication_id', help='edit publication id')
edit_pub_parser.add_argument('-t', '--title', nargs='*', help='new title value')
edit_pub_parser.add_argument('-idr', '--id_range', nargs=2, help='publication id range')
edit_pub_parser.add_argument('-l', '--url', help='publication url')

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
docx_parser.add_argument('-i', '--introduction', nargs='*', help='roundup introduction')

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

#parser for the
delete_parser = argparse.ArgumentParser()
delete_subparsers = delete_parser.add_subparsers(title='subcommands', help='subcommand help')

delete_ent_parser = delete_subparsers.add_parser('entry', help='entry help')
delete_ent_parser.add_argument('-id', '--entry_id', help='entry id')

delete_cat_parser = delete_subparsers.add_parser('category', help='section help')
delete_cat_parser.add_argument('-id', '--category_id', help='category id')

delete_sec_parser = delete_subparsers.add_parser('section', help='section help')
delete_sec_parser.add_argument('-id', '--section_id', help='section id')

#finalize section

#parser for the base finalize command

finalize_parser = argparse.ArgumentParser()
finalize_subparsers = finalize_parser.add_subparsers(title='finalize', help='finalize help')

#parser for the entries subcommand

finalize_entries_parser = finalize_subparsers.add_parser('entries', help='finalize entries help')
finalize_entries_parser.add_argument('-d', '--date', help='search a single date')
finalize_entries_parser.add_argument('-r', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')

#parser for the publishers subcommand

set_pub_names = finalize_subparsers.add_parser('publications', help='publication help')
set_pub_names.add_argument('-idr', '--id_range', nargs=2, help='pubname help')

#parser for the merge_publishers subcommand

merge_publishers = finalize_subparsers.add_parser('merge_pubs', help='merge publications help')
merge_publishers.add_argument('-idr', '--id_range', nargs=2, help='id range')


class RoundupCMD(cmd2.Cmd):
    """
    Example cmd2 application where we a base command which has a couple subcommands
    and the "sport" subcommand has tab completion enabled.
    """
    
    def __init__(self):
        super().__init__(multiline_commands=['add', 'export'], use_ipython=True)
        self.disable_command('quit', message_to_print='Enter "exit" to quit')
        self.intro = style('Welcome to RoundupCLI and cmd2!', fg=cmd2.fg.red, bg=cmd2.bg.white, bold=True) + ' 😀'
        self.prompt= style('(cmd)')
        self.continuation_prompt = '...'
        #self.background_color='cyan'
        self.self_in_py = True
        self.allow_style='Always'
        
    
    def base_ent(self, args):
        '''Adds an article with a single type entry on the command line'''
        try:
            assert args.date
        except AssertionError:
            date = btc.read_date('Enter date of article: ')
            args.date = date
        try:
            assert args.category_id
        except AssertionError:
            try:
                assert args.category_name
                args.category_id = app.get_category(args.category_name, session=a.d.session).category_id
                assert args.category_id
            except AssertionError: #if we don't get a category name
                category_list = [i for i in enumerate(map(str, app.get_categories()),1)]
                self.poutput('Enter category ID to select section or "." to quit: ')
                category_choice = self.select(category_list)
                args.category_id=category_choice
        assert args.url, 'URL must be specified after the -l parameter'
        if not args.description:
            if args.manual_description == 'yes':
                app.add_entry(session=a.d.session, url=args.url, category_id=args.category_id, date=args.date,
                              manual_description=True)
            else:
                app.add_entry(session=a.d.session, url=args.url,
                              category_id=args.category_id, date=args.date)
        else:
            app.add_entry(session=a.d.session, url=args.url, category_id=args.category_id,
                   date=args.date, description=' '.join(args.description))
            
    def base_multiple(self, args):
        '''Adds multiple entries with a single command on the command line'''
        def set_up_entry(link_arg, category_id=None, date=None):
            print('Link to the article is:', link_arg)
            date = btc.read_date('Enter date of article: ')
            #args.date = date
            try:
                assert category_id
            except AssertionError:
                category_list = [i for i in enumerate(map(str, app.get_categories()),1)]
                self.poutput('Enter category ID to select section or "." to quit: ')
                category_id = self.select(category_list)
                #category_id=category_choice
            #assert args.url, 'URL must be specified after the -l parameter'
            app.add_entry(session=a.d.session, url=link_arg, category_id=args.category_id, date=date)
        if args.complete_info: #the "all" argument 
            entries = [i for i in args.complete_info]
            for i in entries:
                #i = i.split('-')
                url, category_id, date = i.split('`')
                app.add_entry(session=a.d.session, url=url,
                              category_id=category_id,
                              date=date)
                #print(url, category_id, date)
            #print(entries)
            #for arg in statement.arg_list:
              #  link_arg, category_id_arg, date_arg = arg.split('-')
               # set_up_entry(link_arg=link_arg, category=args.category_id, date=args.date)
        else:
            if args.category_id:
                if args.date:
                    for argument in args.links:
                        set_up_entry(link_arg=argument, category_id=args.category_id, date=args.date)
                else:
                    for argument in args.links:
                        set_up_entry(link_arg=argument, category_id=args.category_id)
            else:
                if args.date:
                    for argument in args.links:
                        set_up_entry(link_arg=argument, date_arg=args.date)
                else:
                    for argument in args.links:
                        #print(argument)
                        set_up_entry(link_arg=argument)
        
            
    def base_cat(self, args):
        '''Adds a category with a single entry on the command line'''
        if not args.section_id:
            #if the user forgets to enter a section id
            section_list = [i for i in enumerate(map(str, app.get_sections()),1)]
            self.poutput('Enter section ID to select section or "." to quit: ')
            section_choice = self.select(section_list)
            if section_choice == ".":
                self.poutput('Add category cancelled, return to main menu')
                return
            else:
                args.section_id=section_choice
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
        
    def base_kw(self, args):
        '''Adds a keyword to the database'''
        warnings.warn('add keyword not yet tested')
        app.add_keyword_to_article(session=a.d.session, new_keyword=args.word,
                                   entry_id=args.entry_id)
        
    parser_add_entry.set_defaults(func=base_ent)
    parser_add_entries.set_defaults(func=base_multiple)
    parser_add_cat.set_defaults(func=base_cat)
    parser_add_sec.set_defaults(func=base_sect)
    parser_add_pub.set_defaults(func=base_pub)
    parser_add_kw.set_defaults(func=base_kw)
    
    @cmd2.with_argparser(add_parser)
    def do_add(self, args):
        """Search command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('add')
    
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
        
    def base_publication(self, args):
        '''Generic publication search function'''
        warnings.warn('Publication search not fully implemented')
        app.find_publication(session=a.d.session, args=args)
        
    parser_category.set_defaults(func=base_category)
    parser_section.set_defaults(func=base_section)
    parser_entry.set_defaults(func=base_entry)
    parser_keyword.set_defaults(func=base_keyword)
    parser_publication.set_defaults(func=base_publication)

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
        edit_types = {'all': app.edit_entry2, 'description': app.desc_from_input,
                      'category_id': app.cat_id_from_input, 'add keyword': app.add_keyword_to_article,
                    'title': app.name_from_input, 'date': app.date_from_input,
                     'delete keyword': app.delete_entry_keyword}
        if not args.entry_id:
            raise Exception('Must enter entry id')
        if args.entry_id:
            if not args.edit_type:
                app.edit_entry2(session=a.d.session, entry_id=args.entry_id)
            else:
                edit_type = ' '.join(args.edit_type).lower() #make into a string with spaces
                edit_types[edit_type](session=a.d.session, entry_id=args.entry_id)
                
#    def base_edit_cat(self, args):
#        '''Generic edit category function'''
#        if args.new_name:
#            app.edit_name(session=a.d.session, model='category',
#                         id_value=args.category_id, new_name=' '.join(args.new_name))
#        else:
#            new_name = btc.read_text('Enter new category name or "." to cancel: ')
#            if new_name != ".":
#                app.edit_name(session=a.d.session, model='category',
#                         id_value=args.category_id, new_name=new_name)
    def base_edit_cat(self, args):
        '''Generic edit category function'''
        app.edit_category2(session=a.d.session, args=args)
    
    def base_edit_pub(self, args):
        '''Generic edit publication function'''
        app.edit_pub2(session=a.d.session, args=args)
    
#    def base_edit_pub(self, args):
#        '''Generic add publication function'''
#            #print(result)
#        
#        if args.new_title:
#            result = app.edit_pub(session=a.d.session,
#                                      publication_id=args.publication_id,
#                                      new_title=' '.join(args.new_title))
#        elif not args.new_title:
#            item = app.get(session=a.d.session,
#                    model=Publication, id_value=args.publication_id)
#            print(item)
#            manual_title = btc.read_text('Enter new title: ')
#            result = app.edit_pub(session=a.d.session,
#                                      publication_id=args.publication_id,
#                                      new_title=manual_title)
#        modified_result = str(result) + '\x1b[2m'
#        cmd2.utils.align_center(text=modified_result) #not working
#        self.poutput(result)
        

            
    edit_category_parser.set_defaults(func=base_edit_cat)
    edit_entry_parser.set_defaults(func=base_edit_entry)
    edit_pub_parser.set_defaults(func=base_edit_pub)
    
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
        if args.introduction:
            args.introduction = ' '.join(args.introduction)
        app.create_docx_roundup(args)
    
    def base_html(self, args):
        '''Generic export html function'''
        warnings.warn('introduction not yet set up for html export')
        app.export_html2(session=a.d.session, program=args.filename,
                        start_date=parse(args.date_range[0]).date(),
                         end_date=parse(args.date_range[1]).date(),
                        title=' '.join(args.title))
        
    def base_jsx(self, args):
        '''Generic export jsx function for react'''
        #print(args)
        warnings.warn('introduction not yet set up for jsx export')
        app.export_jsx(session=a.d.session, program=args.filename,
                        start_date=parse(args.date_range[0]).date(),
                         end_date=parse(args.date_range[1]).date(),
                        title=' '.join(args.title))
    
    def base_full_jsx_file(self, args):
        '''Generic export jsx function for react'''
        #print(args)
        #if hasattr(args, 'use_sections'):
        warnings.warn('introduction not yet set up for jsx export')
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
            

    
    #finalize section
    
    def base_merge_publishers(self, args):
        app.merge_pub(args=args, session=a.d.session)
    
    def base_pubnames(self, args):
        app.set_pubnames(args=args, session=a.d.session)
    
    
    def base_finish_articles(self, args):
        '''searches for articles without descriptions and lets user edit them'''
        if args.date:
            app.finalize(session=a.d.session, start_date =args.date, end_date=args.date)
        elif args.date_range:
            app.finalize(session=a.d.session, start_date = args.date_range[0],
                          end_date=args.date_range[1])
        else:
            self.poutput('Please enter date or date range. Check help for details')
            #print('Please enter date or date range. Check help for details')
            return
        
    set_pub_names.set_defaults(func=base_pubnames)
    finalize_entries_parser.set_defaults(func=base_finish_articles)
    merge_publishers.set_defaults(func=base_merge_publishers)
    
    @cmd2.with_argparser(finalize_parser)
    def do_finalize(self, args):
        """finalize command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('display')
#        if args.date:
#            app.finalize(session=a.d.session, start_date =args.date, end_date=args.date)
#        elif args.date_range:
#            app.finalize(session=a.d.session, start_date = args.date_range[0],
#                          end_date=args.date_range[1])
#        else:
#            self.poutput('Please enter date or date range. Check help for details')
#            #print('Please enter date or date range. Check help for details')
#            return
    
    #finalize publication
    
   # set_pub_names = argparse.ArgumentParser()
   # set_pub_names.add_argument('-idr', '--id_range', nargs=2, help='pubname help')
    
   # @cmd2.with_argparser(set_pub_names)
   # def do_set_pubnames(self, args):
   #     app.set_pubnames(args=args, session=a.d.session)
        
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
            self.do_help('display')
    
    #@cmd2.with_argparser(disp_parser)
    
        
   # count_parser = argparse.ArgumentParser()
   # count_parser.add_argument('-d','--date_range', nargs=2, help='start date, end_date')     

    #delete section
    
    def base_del_section(self, args):
        if args.section_id:
            app.delete_item(session=a.d.session, model='section',
                            id_value=args.section_id)
    
    def base_del_category(self, args):
        if args.category_id:
            app.delete_item(session=a.d.session, model='category',
                            id_value=args.category_id)
    
    def base_del_entry(self, args):
        if args.entry_id:
            app.delete_item(session=a.d.session, model='entry',
                            id_value=args.entry_id)
    
    delete_ent_parser.set_defaults(func=base_del_entry)
    delete_cat_parser.set_defaults(func=base_del_category)
    delete_sec_parser.set_defaults(func=base_del_section)
    
    @cmd2.with_argparser(delete_parser)
    def do_delete(self, args):
        """display command help"""
        func = getattr(args, 'func', None)
        if func is not None:
            # Call whatever subcommand function was selected
            func(self, args)
        else:
            # No subcommand was provided, so call help
            self.do_help('del')
    
    #del_parser = argparse.ArgumentParser()
    #del_parser.add_argument('-ty', '--item_type',
    #                        help='item type e.g. entry, category, section, author, publication')
    #del_parser.add_argument('-id', '--id_value', help='item id')
    
    #@cmd2.with_argparser(del_parser)
    #def do_delete_item(self, args):
    #    '''Delete item '''
    #    warnings.warn('Unified delete function not fully tested')
    #    app.delete_item(session=a.d.session, model=args.item_type, id_value=args.id_value)
    
    def do_exit(self, arg):
        '''Exits the program, any existing database connections will be closed'''
        a.close()
        self.poutput(msg='Exiting Roundup Generator')
        #print('Exiting Roundup Generator')
        return True
    
if __name__ == '__main__':
    a=app.App()
    a.setup()
    RoundupCMD().cmdloop()