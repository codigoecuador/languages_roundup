#!/usr/bin/env python3
# coding=utf-8
"""A simple example demonstrating how to use Argparse to support subcommands.
This example shows an easy way for a single command to have many subcommands, each of which takes different arguments
and provides separate contextual help.
"""
import argparse
import sys, glob, os
from datetime import date, timedelta
#import cmd2
from typing import List
import itertools as it
import warnings, functools, pprint
import cmd2
#import newspaper as np
from dateutil.parser import parse
from roundup_db1 import Entry, Category, Keyword, Publication, Author, Section, Introduction, DataAccessLayer
import app
import BTCInput3 as btc
import warnings, functools, pprint
from cmd2 import style, fg, bg

summary_choices = ['yes', 'no']
#date_range_choices = {'yes':True, 'no': False}
date_range_choices2 = ['yes', 'no']




###ADD COMMAND
add_parser = argparse.ArgumentParser()
add_subparsers = add_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "introduction" subcommand

parser_add_intro = add_subparsers.add_parser('introduction', help='introduction help')
parser_add_intro.add_argument('-n', '--name',
                              nargs='*', help='intro name e.g. Sub Saharan Roundup Intro')
parser_add_intro.add_argument('-t', '--text', nargs='*', help='introduction text')

#create the parser for the "entry" subcommand

parser_add_entry = add_subparsers.add_parser('entry', help='entry help')
parser_add_entry.add_argument('-l', '--url', help='url of article')
parser_add_entry.add_argument('-c', '--category_id', help='category id e.g. Comoros is 1')
parser_add_entry.add_argument('-cn', '--category_name',
                              nargs='*', help='category name e.g. Arts and Culture')
parser_add_entry.add_argument('-d','--date', help='article date')
parser_add_entry.add_argument('-desc',  '--description', nargs='*',
                           help='article description (optional)')
parser_add_entry.add_argument('-kw', '--new_keywords', nargs='*',
                              help='article custom keywords e.g. Covid-19')
parser_add_entry.add_argument('-md', '--manual_description', help='view summary, enter yes or no',
                          choices=summary_choices)
parser_add_entry.add_argument('-dr', '--date_range', nargs=2,
                              help='enter a start date and end date and manually select the date using the menu')
parser_add_entry.add_argument('-s', '--section_id',
                          help='choose from categories in one section')

#create the parser for the "entries" subcommand

parser_add_entries = add_subparsers.add_parser('entries', help='multiple entries')
parser_add_entries.add_argument('-ls', '--links', nargs='*', help='multiple entries help')
parser_add_entries.add_argument('-all', '--complete_info', nargs='*', help='[url]`[category_id]`[date]')
parser_add_entries.add_argument('-c', '--category_id',help='category IDs help')
parser_add_entries.add_argument('-d', '--date', help='multiple articles from the same date')
parser_add_entries.add_argument('-s', '--section_id',
                                help='select categories from a single section')
parser_add_entries.add_argument('-drm', '--use_date_range', help='select the articles from a date range',
                                choices = date_range_choices2)
parser_add_entries.add_argument('-dr', '--date_range', nargs=2,
                                help='articles are between two dates')

parser_add_to_section = add_subparsers.add_parser('entries_to_section', help='multiple entries')
parser_add_to_section.add_argument('-ls', '--links', nargs='*', help='multiple entries help')
#parser_add_entries.add_argument('-all', '--complete_info', nargs='*', help='[url]-[category_id]-[date]')
#parser_add_entries.add_argument('-c', '--category_id',help='category IDs help')
parser_add_to_section.add_argument('-d', '--date', help='multiple articles from the same date')
parser_add_to_section.add_argument('-s', '--section_id',
                                help='select categories from a single section')
parser_add_to_section.add_argument('-drm', '--use_date_range', help='select the articles from a date range',
                                choices = date_range_choices2)
parser_add_to_section.add_argument('-dr', '--date_range', nargs=2,
                                help='articles are between two dates')
#add entries

parser_add_with_names = add_subparsers.add_parser('entries_cat_name',
                                                  help='multiple entries with category names')
parser_add_with_names.add_argument('-all', '--complete_info', nargs='*', help='[url]`[category_name]`[date]')

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


###SEARCH COMMAND

# create the top-level parser for the search command
search_parser = argparse.ArgumentParser()
search_subparsers = search_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "introduction" subcommand
introduction_parser = search_subparsers.add_parser('introduction', help='introduction help')
introduction_parser.add_argument('-id', '--introduction_id',
                                 help='id number of the intro, basic intro is 1')

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
#add section id option to limit the number of category choices


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


##EDIT COMMAND: parsers for editing Entries, Categories, Sections, Keywords,
#Publications, and Authors

edit_parser = argparse.ArgumentParser() #main parser for the edit command
edit_subparsers = edit_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "entry" subcommand
edit_entry_parser = edit_subparsers.add_parser('entry', help='entry help')
edit_entry_parser.add_argument('-id', '--entry_id', help='the id number of the entry to edit')
edit_entry_parser.add_argument('-t', '--edit_type', nargs='*',
                            help='edit types: title, date, keywords, description, category_id')

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
disp_ent_count_parser.add_argument('-dr','--date_range', nargs=2, help='start date, end_date')

#create the parser for the entries_needed subcommand

disp_ents_needed_parser = disp_subparsers.add_parser('entries_needed', help='entries needed')
disp_ents_needed_parser.add_argument('-dr','--date_range', nargs=2, help='start date, end_date')

##EXPORT COMMAND: parsers for the commands

exp_parser = argparse.ArgumentParser() #different from the exportparser
exp_subparsers = exp_parser.add_subparsers(title='subcommands', help='subcommand help')

#create the parser for the "docx" subcommand

docx_parser = exp_subparsers.add_parser('docx', help='docx help')
docx_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
docx_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
docx_parser.add_argument('-dr', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')
docx_parser.add_argument('-i', '--introduction', nargs='*', help='roundup introduction')
docx_parser.add_argument('-iid', '--introduction_id',
                         help='id of an existing introduction')

#create the parser for the "html" subcommand

html_parser = exp_subparsers.add_parser('html', help='docx help')
html_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
html_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
html_parser.add_argument('-dr', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')
#create the parser for the jsx subcommand

jsx_parser = exp_subparsers.add_parser('jsx', help='docx help')
jsx_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
jsx_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
jsx_parser.add_argument('-dr', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')

#create the parser for the jsx_file subcommand

jsx_full_parser = exp_subparsers.add_parser('jsx_file',
                                            help='creates a javascript file for the Codigo Ecuador website')
jsx_full_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
jsx_full_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
jsx_full_parser.add_argument('-dr', '--date_range', nargs=2,
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
finalize_entries_parser.add_argument('-dr', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')

#parser for the publishers subcommand

set_pub_names = finalize_subparsers.add_parser('publications', help='publication help')
set_pub_names.add_argument('-idr', '--id_range', nargs=2, help='pubname help')

#parser for the merge_publishers subcommand

merge_publishers = finalize_subparsers.add_parser('merge_pubs', help='merge publications help')
merge_publishers.add_argument('-idr', '--id_range', nargs=2, help='id range')


#from datetime import date, timedelta

def make_date_range(sdate: date, edate: date) -> List:
    delta = edate-sdate
    dates = [sdate+timedelta(i) for i in range(delta.days+1)]
    return dates

class RoundupCMD(cmd2.Cmd):
    """
    Example cmd2 application where we a base command which has a couple subcommands
    and the "sport" subcommand has tab completion enabled.
    """
    
    def __init__(self):
        super().__init__(multiline_commands=['add', 'export'], use_ipython=True)
        self.disable_command('quit', message_to_print='Enter "exit" to quit')
        self.intro = style('Welcome to RoundupCLI and cmd2!', fg=cmd2.fg.red, bg=cmd2.bg.white, bold=True) + ' 😀'
        self.self_in_py = True
        self.allow_style='Always'
        
        new_app=app.App()
        new_app.setup()
        self.app=new_app
        self.session=new_app.d.Session()
       
    def base_intro(self, args):
        '''Adds an introduction with a single type entry on the command line'''
        #the title and text are paragraphs/sentences so let's combine them
        args.name = ' '.join(args.name)
        args.text = ' '.join(args.text)
        confirmation = cmd2.style(f'Confirm add? {args.name}, {args.text}',
                                  fg=cmd2.fg.red, bg=cmd2.bg.yellow)
        self.poutput(confirmation)
        confirm = self.select([(True, 'yes'), (False, 'no')])
        if confirm == True:
            app.add_intro(session=self.session, cmdobj=self, name=args.name,
                          text=args.text)
        else:
            self.poutput('Add cancelled')
        
    
    def add_entry(self, args):
        '''Adds an entry with a single type entry on the command line'''
        if not args.new_keywords:
            args.new_keywords=None
        try:
            assert args.date
        except AssertionError:
            try:
                assert args.date_range
                args.date_range[0] = parse(args.date_range[0])
                args.date_range[1] = parse(args.date_range[1])
                date_range = make_date_range(sdate=args.date_range[0],
                                            edate=args.date_range[1])
                
                date_dict = {str(i): i for i in date_range}
                date_choice = self.select(date_dict)
                print(date_choice)
                print(type(date_choice))
                args.date = date_choice
            except AssertionError:
                date = btc.read_date('Enter date of article: ')
                args.date = date
        try:
            assert args.category_id
        except AssertionError:
            try:
                assert args.category_name
                args.category_id = app.get_category(args.category_name, session=self.session).category_id
                assert args.category_id
            except AssertionError: #if we don't get a category name
                try:    
                    assert args.section_id
                    category_list = [i for i in enumerate(map(str,
                                app.get_categories(session=self.session,
                                section_id=args.section_id)),1)]
                    #get the categories for a section
                except AssertionError:
                    #we get all the categories if its not limited to a particular section
                    category_list = [i for i in enumerate(map(str, app.get_categories(session=self.session)),1)]
                self.poutput('Enter category ID to select section or "." to quit: ')
                category_choice = self.select(category_list)
                args.category_id=category_choice
        assert args.url, 'URL must be specified after the -l parameter'
        if not args.description:
            if args.manual_description == 'yes':
                app.add_entry(session=self.session, cmdobj=self, url=args.url, category_id=args.category_id, date=args.date,
                              manual_description=True, new_keywords=args.new_keywords)
            else:
                app.add_entry(session=self.session, cmdobj=self, url=args.url,
                              category_id=args.category_id,
                              date=args.date, new_keywords=args.new_keywords)
        else:
            app.add_entry(session=self.session, cmdobj=self,
                          url=args.url, category_id=args.category_id,
                   date=args.date, description=' '.join(args.description),
                   new_keywords=args.new_keywords)
            
    def add_multiple_entries(self, args):
        '''Adds multiple entries with a single command on the command line'''
        def set_up_entry(link_arg, category_id=None, date=None):
            '''
            Sets up each entry in a series of multiple entries
            link_arg: the link of the actual article
            category_id: the id of the category
            date: the date of the article
        
            
            '''
            print('Link to the article is:', link_arg)
            if date == None:
                date = btc.read_date_adv(prompt='Enter date of article: ')
            #args.date = date
            try:
                assert category_id
            except AssertionError:
                
                category_list = [i for i in enumerate(map(str, app.get_categories(session=self.session)),1)]
                self.poutput('Enter category ID to select section or "." to quit: ')
                args.category_id = self.select(category_list)
                self.poutput(f'Category ID is {category_id}')
                category_id=category_choice
            #assert args.url, 'URL must be specified after the -l parameter'
            app.add_entry(session=self.session, cmdobj=self, url=link_arg, category_id=args.category_id, date=date)
            return None
        
        #-----------------------------------------
        if args.complete_info: #the "all" argument 
            entries = [i for i in args.complete_info]
            for i in entries:
                #i = i.split('-')
                url, category_id, date = i.split('`')
                app.add_entry(session=self.session,
                              cmdobj=self, url=url,
                              category_id=category_id,
                              date=date)
        #fix the configuration of this command
        if args.use_date_range == 'yes':
            #date range only works if this has been called
            entries = [i for i in args.links]
            start_date = parse(args.date_range[0])
            end_date=parse(args.date_range[1])
           # start_date, end_date = parse(args.date_range)#[0]),
                #parse(args.date_range[1])
            dates = make_date_range(sdate=start_date,
                                    edate=end_date)
            date_choices = [(i, str(i)) for i in dates]
            for entry in entries:
                url, category_id = entry.split('`')
                self.poutput('Select date for article')
                self.poutput(url)
                date_choice = self.select(opts=date_choices)
                app.add_entry(session=self.session,
                              cmdobj=self, url=url,
                              category_id=category_id,
                              date=date_choice)
        else:
            if args.category_id:
                if args.date:
                    for argument in args.links:
                        set_up_entry(link_arg=argument, category_id=args.category_id, date=args.date)
                else:
                    for argument in args.links:
                        set_up_entry(link_arg=argument, category_id=args.category_id)
            elif args.section_id:
                print(args.section_id)
                for argument in args.links:
                    print(argument)
                    category_list = [(i.category_id,str(i)) for i in app.get_categories(session=self.session,
                                                                                        section_id=args.section_id)]
                    #list of tuples because we are going to be getting the category ID
                                                          #1): i for i in app.get_categories(section_id=args.section_id)}
                    cat_msg = cmd2.style('Enter category ID to select section or "." to quit: ',
                                         bg=cmd2.bg.blue, fg=cmd2.fg.white,
                                         bold=True)
                    self.poutput(cat_msg)
                    #self.poutput('Enter category ID to select section or "." to quit: ')
                    category_choice = self.select(category_list)
                    args.category_id=category_choice#.category_id
                    self.poutput(self.session.query(Category).filter(Category.category_id==args.category_id).first())
                    confirm = btc.read_int_ranged(f'Category is: {args.category_id} 1 to confirm, 2 to cancel', 1, 2)
                    if confirm == 2:
                        cancel_msg = cmd2.style('Add cancelled',
                                                fg=cmd2.fg.yellow,
                                                bg=cmd2.bg.red,
                                                bold=True)
                        self.poutput(cancel_msg)
                        return
                    #print(args.category_id)
                    if args.date:
                        set_up_entry(link_arg=argument, date=args.date,
                                     category_id=args.category_id)
                    else:
                        set_up_entry(link_arg=argument, category_id=args.category_id)
            else:
                if args.date:
                    for argument in args.links:
                        set_up_entry(link_arg=argument, date=args.date)
                else:
                    for argument in args.links:
                        #print(argument)
                        set_up_entry(link_arg=argument)
                        
    def add_entries_cat_names(self, args):
        '''Add entries based on category name'''
        new_entries = (i.split('`') for i in args.complete_info)
        #entries split into link, category name, and date
        try:
            while new_entry := next(new_entries):
                link, cat_name, date = new_entry
                try:
                    cat_for_id = app.get_category_name(category_name=cat_name,
                                                        session=self.session)
                    #we just got the category
                    try:
                        category_id = cat_for_id.id_value
                    except AttributeError:
                        category_id = None
                        no_cat_found_msg = cmd2.style('No category found',
                                                      bg=cmd2.bg.red,
                                                      fg=cmd2.fg.white,
                                                      bold=True)
                        self.poutput(no_cat_found_msg)
                        #print('No category found')
                        new_cat_choice = btc.read_int_ranged_adv(prompt=f'Add {cat_name} as a new category? 1-yes, 2-cancel',
                                                                 min_value=1, max_value=2,
                                                                 cmdobj=self,
                                                                 bg=cmd2.bg.blue,
                                                                 fg=cmd2.fg.white,
                                                                 bold=True)
                        if new_cat_choice == 1:
                            section_list = app.get_sections()
                            make_style = lambda x: cmd2.style(text=x, fg=cmd2.fg.white,
                                              bg=cmd2.bg.blue, bold=False)
                            section_list = [i for i in enumerate(map(make_style, app.get_sections()),1)]
                            section_id = self.select(section_list)
                            new_category = app.new_cat_with_entry(category_name=cat_name, section_id=section_id,
                                                                  session=self.session, cmdobj=self)
                            category_added = app.get_category_name(category_name=cat_name,
                                                                   session=self.session)

                            #print('Category ID', category_id)
                            #print('link', link)
                            #print('cat_name', cat_name)
                            if category_id == None:
                                try:
                                    new_cat_added = cmd2.style('New Category added:', bg=cmd2.bg.blue,
                                                               fg=cmd2.fg.white, bold=True)
                                    new_cat_style = cmd2.style(text=category_added, bg=cmd2.bg.blue,
                                                               fg=cmd2.fg.white, bold=False)
                                    self.poutput(new_cat_added)
                                    self.poutput(new_cat_style)
                                    #print('New category :', category_added)
                                    category_id = category_added.category_id
                                    #category_id = new_category.category_id
                                    #self.poutput(f'add for {link} failed')
                                    #return None
                                except Exception as e:
                                    self.poutput(e)
                                    return None
                            date = parse(date).date()
                            app.add_entry(session=self.session,
                                      cmdobj=self, url=link,
                                      category_id=category_id,
                                      date=date)
                except Exception as e:
                    exception_format = cmd2.style(text=e, bg=cmd2.bg.red,
                                                  fg=cmd2.fg.yellow,
                                                  bold=True)
                    self.poutput(exception_format)
                    #print(e)
                    continue
                
        except StopIteration:
            success = cmd2.style(text='Articles added successfully',
                                 bg=cmd2.bg.blue, fg=cmd2.fg.white,
                                 bold=True)
            self.poutput(success)
            #self.poutput('Articles added successfully')
        
    
    def add_entries_to_section(self, args):
        '''Add multiple entries to a single section'''
        def set_up_entry(link_arg, section_id, date_range=None,
                         date=None):
            '''Internal function to add multiple entries to the same section'''
            if args.date_range:
                assert not args.date, 'cannot have both date and date range'
                link_arg_style = cmd2.style(text=link_arg, fg=cmd2.fg.white,
                                            bg=cmd2.bg.blue, bold=True)
                self.poutput(link_arg_style)
                dates = make_date_range(sdate=args.date_range[0],
                                    edate=args.date_range[1])
                date_choices = [(i, str(i)) for i in dates]
                date = self.select(opts=date_choices)
            elif args.date:
                assert not args.date_range, 'cannot have both date and date range'
                date = args.date
            category_list = [(i.category_id,str(i)) for i in app.get_categories(session=self.session,
                                                                                        section_id=args.section_id)]
                    #list of tuples because we are going to be getting the category ID
            
            category_option = cmd2.style('Select category:', fg=cmd2.fg.white,
                                         bg=cmd2.bg.blue, bold=True)
            self.poutput(category_option)
            category_id = self.select(category_list)
            args.category_id=category_id
            self.poutput(self.session.query(Category).filter(Category.category_id==args.category_id).first())
            confirm = btc.read_int_ranged_adv(prompt=f'Category ID is: {args.category_id} 1 to confirm, 2 to cancel: ',
                                              min_value=1, max_value=2,
                                              bg=cmd2.bg.blue,
                                              fg=cmd2.bg.white)
            if confirm == 2:
                self.poutput('Add cancelled')
                return
            app.add_entry(session=self.session,
                              cmdobj=self, url=link_arg,
                              category_id=category_id,
                              date=date)
            return None
        
        #the code below runs before the function above
#        print(args)
        if not args.section_id:
            raise Exception('section_id is required')
        if (not args.date) and (not args.date_range):
            #if the user doesn't enter either date or date range it won't work
            raise Exception('"-d" date or "-dr" date range required')
        if args.use_date_range == 'yes':
            print('date range activated')
            args.date_range[0] = parse(args.date_range[0])
            args.date_range[1] = parse(args.date_range[1])
            #assert args.date_range[0] >= args.date_range[1], 'start date must come before end date'
#            print(True)
            for link in args.links:
                set_up_entry(link_arg=link, section_id=args.section_id,
                             date_range=args.date_range)
        if args.date:
            #print(False)
            if args.use_date_range == True:
                raise Exception('Cannot have both date and date range')
            args.date=parse(args.date)
            #print('date is', args.date)
            #print('section_id is', args.section_id)
           # print('link is', link)
            for link in args.links:
                #print('link is', link)
                #print('adding entry')
                set_up_entry(link_arg=link, section_id=args.section_id,
                             date=args.date)
        
    
    def base_cat(self, args):
        '''Adds a category with a single entry on the command line'''
        if not args.section_id:
            #if the user forgets to enter a section id
            make_style = lambda x: cmd2.style(text=x, fg=cmd2.fg.white,
                                              bg=cmd2.bg.blue, bold=False)
            section_list = [i for i in enumerate(map(make_style, app.get_sections()),1)]
            
            select_section = cmd2.style('Enter section ID to select section or "." to quit: ',
                                        bg=cmd2.bg.blue, fg=cmd2.fg.white, bold=False)
            self.poutput(select_section)
            section_choice = self.select(section_list)
            if section_choice == ".":
                self.poutput('Add category cancelled, return to main menu')
                return
            else:
                args.section_id=section_choice
        app.add_pub_or_cat(new_name=' '.join(args.name),
                           second_item=args.section_id,
                          session=self.session, add_type='category')
        
    def base_sect(self, args):
        '''Adds a new section to the roundup'''
        warnings.warn('add_section not yet tested')
        app.add_item(session=self.session, search_type='section',
                     new_name=' '.join(args.section_name))
        
    def base_pub(self, args):
        '''Adds a publication to the database'''
        warnings.warn('add publication not yet tested')
        app.add_pub_or_cat(new_name=' '.join(args.title),
                           second_item=args.section_id,
                          session=self.session, add_type='publication')
        
    def base_kw(self, args):
        '''Adds a keyword to the database'''
        warnings.warn('add keyword not yet tested')
        app.add_keyword_to_article(session=self.session, new_keyword=args.word,
                                   entry_id=args.entry_id)
        
    parser_add_intro.set_defaults(func=base_intro)
    parser_add_entry.set_defaults(func=add_entry)
    parser_add_entries.set_defaults(func=add_multiple_entries)
    parser_add_to_section.set_defaults(func=add_entries_to_section)
    parser_add_with_names.set_defaults(func=add_entries_cat_names)
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
    
    def search_introduction(self, args):
        '''Generic introduction search function'''
        warnings.warn('Introduction not fully implemented')
        app.find_introduction(session=self.session, cmdobj=self, args=args)
    
    def search_category(self, args):
        '''Generic category search function'''
        app.find_category(session=self.session, args=args)
        
    def search_entry(self, args):
        '''Generic entry search function'''
        app.find_entry(session=self.session, args=args, cmdobj=self)
    
    def search_section(self, args):
        '''Generic section search function'''
        app.find_section(session=self.session, args=args)
        
    def search_keyword(self, args):
        '''Generic keyword search function'''
        app.find_keyword(session=self.session, args=args)
        
    def search_publication(self, args):
        '''Generic publication search function'''
        warnings.warn('Publication search not fully implemented')
        app.find_publication(session=self.session, args=args)
        
    introduction_parser.set_defaults(func=search_introduction)
    parser_entry.set_defaults(func=search_entry)
    parser_category.set_defaults(func=search_category)
    parser_section.set_defaults(func=search_section)
    parser_keyword.set_defaults(func=search_keyword)
    parser_publication.set_defaults(func=search_publication)

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
    
    def edit_entry(self, args):
        '''Generic edit entry function'''
        edit_types = {'all': app.edit_entry, 'description': app.desc_from_input,
                      'category_id': app.cat_id_from_input, 'add keyword': app.add_keyword_to_article,
                    'title': app.name_from_input, 'date': app.date_from_input,
                     'delete keyword': app.delete_entry_keyword}
        if not args.entry_id:
            raise Exception('Must enter entry id')
        if args.entry_id:
            if not args.edit_type:
                app.edit_entry(session=self.session, entry_id=args.entry_id,
                                cmdobj=self)
            else:
                edit_type = ' '.join(args.edit_type).lower() #make into a string with spaces
                edit_types[edit_type](session=self.session, entry_id=args.entry_id)

    def edit_category(self, args):
        '''Generic edit category function'''
        app.edit_category2(session=self.session, args=args)
    
    def edit_publication(self, args):
        '''Generic edit publication function'''
        app.edit_pub2(session=self.session, args=args)
    
            
    edit_category_parser.set_defaults(func=edit_category)
    edit_entry_parser.set_defaults(func=edit_entry)
    edit_pub_parser.set_defaults(func=edit_publication)
    
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
    
    def export_docx(self, args):
        '''Generic export html function'''
        if args.introduction:
            if args.introduction_id:
                raise Exception('Cannot have both introduction and introduction_id')
            args.introduction = ' '.join(args.introduction)
            #app.create_docx_roundup(args)
        if args.introduction_id:
            if args.introduction:
                raise Exception('Cannot have both introduction and introduction_id')
        app.create_docx_roundup(args, session=self.session)
    
    def export_html(self, args):
        '''Generic export html function'''
        warnings.warn('introduction not yet set up for html export')
        app.export_html2(session=self.session, program=args.filename,
                        start_date=parse(args.date_range[0]).date(),
                         end_date=parse(args.date_range[1]).date(),
                        title=' '.join(args.title))
        
    def export_jsx(self, args):
        '''Generic export jsx function for react'''
        #print(args)
        warnings.warn('introduction not yet set up for jsx export')
        app.export_jsx(session=self.session, program=args.filename,
                        start_date=parse(args.date_range[0]).date(),
                         end_date=parse(args.date_range[1]).date(),
                        title=' '.join(args.title))
    
    def export_full_jsx_file(self, args):
        '''Generic export jsx function for react'''
        #print(args)
        #if hasattr(args, 'use_sections'):
        warnings.warn('introduction not yet set up for jsx export')
        if args.use_sections == None:
            app.exp_full_jsx(session=self.session, program=args.filename,
                            start_date=parse(args.date_range[0]).date(),
                             end_date=parse(args.date_range[1]).date(),
                            title=' '.join(args.title), use_sections=False)
            
        elif args.use_sections.lower() == 'yes':
            app.exp_full_jsx(session=self.session, program=args.filename,
                            start_date=parse(args.date_range[0]).date(),
                             end_date=parse(args.date_range[1]).date(),
                            title=' '.join(args.title), use_sections=True)
        else:
            raise Exception('use_sections only accepts "yes" as an argument')
   
    docx_parser.set_defaults(func=export_docx)
    html_parser.set_defaults(func=export_html)
    jsx_parser.set_defaults(func=export_jsx)
    jsx_full_parser.set_defaults(func=export_full_jsx_file)
    
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
        app.merge_pub(args=args, session=self.session)
    
    def base_pubnames(self, args):
        app.set_pubnames(args=args, session=self.session)
    
    
    def base_finish_articles(self, args):
        '''searches for articles without descriptions and lets user edit them'''
        if args.date:
            app.finalize_two(session=self.session, cmdobj=self,
                         start_date =args.date, end_date=args.date)
        elif args.date_range:
            app.finalize_two(session=self.session, cmdobj=self,
                         start_date = args.date_range[0],
                          end_date=args.date_range[1])
        else:
            #self.sdout('')
            error_msg = cmd2.style('Date "-d" or "-dr" date range required.',
                                   bg=cmd2.bg.red, fg=cmd2.fg.yellow,
                                   bold=True)
            self.perror(error_msg, apply_style=True)
            
            #self.poutput('Please enter date or date range. Check help for details')
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
        
    #display section
    
    def display_entries_needed(self, args):
        '''Displays how many articles you need to get five per category'''
        app.articles_needed(start_date=args.date_range[0],
                            end_date=args.date_range[1],
                            session=self.session)
    
    def display_entry_count(self, args):
        '''Displays a count of articles in each category between the specified dates'''
        app.date_range_count(session=self.session,
                             start_date = args.date_range[0],
                            end_date = args.date_range[1])
    
    def display_sections(self, args):
        '''Generic display categories function'''
        app.display_sections(cmdobj=self)
    
    def display_categories(self, args):
        '''Generic display categories function'''
        try:
            if args.section_id.isnumeric() == True:
                app.display_categories(section_id=args.section_id)
        except AttributeError:
            app.display_categories()
    
    disp_cat_parser.set_defaults(func=display_categories)
    disp_sec_parser.set_defaults(func=display_sections)
    disp_ent_count_parser.set_defaults(func=display_entry_count)
    disp_ents_needed_parser.set_defaults(func=display_entries_needed)
    
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

    #delete section
    
    def delete_section(self, args):
        if args.section_id:
            app.delete_item(cmdobj=self, session=self.session, model='section',
                            id_value=args.section_id)
    
    def delete_category(self, args):
        if args.category_id:
            app.delete_item(cmdobj=self, session=self.session, model='category',
                            id_value=args.category_id)
    
    def delete_entry(self, args):
        if args.entry_id:
            app.delete_item(cmdobj=self, session=self.session, model='entry',
                            id_value=args.entry_id)
    
    delete_ent_parser.set_defaults(func=delete_entry)
    delete_cat_parser.set_defaults(func=delete_category)
    delete_sec_parser.set_defaults(func=delete_section)
    
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
    
    
    def do_exit(self, arg):
        '''Exits the program, any existing database connections will be closed'''
        self.session.close()
        exit_message = cmd2.style('Exiting Roundup Generator',
                                  bg=cmd2.bg.white, fg=cmd2.fg.black,
                                  bold=True)
        self.poutput(exit_message)
        #self.poutput(msg='Exiting Roundup Generator')
        return True
    
if __name__ == '__main__':
    RoundupCMD().cmdloop()