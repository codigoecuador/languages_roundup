import newspaper as np
from dateutil.parser import parse
from roundup_db1 import Entry, Category, Keyword, Publication, Author, Section, DataAccessLayer
import app,roundup_help
import sys, glob, datetime, os
import BTCInput2 as btc
import itertools as it
import warnings, functools, pprint
import csv
import cmd2
import argparse
from collections import namedtuple

'''Note: not all of these commands will end up being included in the final
command line interface.

Note for 2/7/20: Add WrappedHTMLFormat properties to each class that we have created.'''

class RoundupCMD(cmd2.Cmd):
    '''
    The actual content of the commands should be moved to the app.py file.
    '''
    prompt='NewsRoundup'
    intro='Welcome to LanguageRoundup, powered by SQLAlchemy'
    
    def __init__(self):
        super().__init__()
    
    add_parser = argparse.ArgumentParser()
    add_parser.add_argument('-l', '--url', help='article url')
    add_parser.add_argument('-c', '--category_id',
            help='category id, type display_categories to view category ids')
    add_parser.add_argument('-d', '--date', help='date of article')
    
    @cmd2.with_argparser(add_parser)
    def do_add_article(self, args):
        '''Adds a new article to the roundup.
        User can add category_id and date as optional arguments'''
        if not args.category_id:
            category_id = None
        else:
            category_id = args.category_id
        if not args.date:
            date = None
        else:
            date = parse(args.date).date()
        app.add_entry(url=args.url, category_id=category_id, date=date,
                     session=a.d.session)
    
    qa_parser = argparse.ArgumentParser()
    qa_parser.add_argument('-l', '--url', help='url of article')
    qa_parser.add_argument('-c', '--category_id', help='category id e.g. Comoros is 1')
    qa_parser.add_argument('-d','--date', help='article date')
    qa_parser.add_argument('-desc',  '--description', nargs='*',
                           help='article description (optional)')
    
    @cmd2.with_argparser(qa_parser)
    def do_qa(self, args):
        '''Adds an article with a single type of the command line. 
        quick_add url cat_id date'''
        
        if not args.category_id:
            print('category does not exist')
            category_name = btc.read_text('Enter new category name or "." to cancel: ')
            if category_name != ".":
                app.display_sections()
                section_choice = btc.read_int('Enter section ID: ')
                app.add_pub_or_cat(session=a.d.session, add_type='category',
                                   new_name=category_name, second_item=section_choice)
                new_cat = app.get(session=a.d.session, model=Category, name=category_name)
        else:
            new_cat = args.category_id #we create a new label so that the function is harmonized
            if args.description: 
                app.qa(session=a.d.session, url=args.url, category_id=new_cat,
                       date=args.date, description=' '.join(args.description))
            else:
                app.qa(session=a.d.session, url=args.url, category_id=new_cat, date=args.date)
        
    cat_parser = argparse.ArgumentParser()
    cat_parser.add_argument('-n', '--name', nargs='+', help='name of new category')
    cat_parser.add_argument('-s', '--section_id', help='id of the section the category is in')
    
    @cmd2.with_argparser(cat_parser)
    def do_add_category(self, args):
        '''Adds a new category'''
        app.add_pub_or_cat(session=a.d.session, new_name=' '.join(args.name),
                           second_item=args.section_id, add_type='category')
    

    
    def do_add_keyword(self, line):
        warnings.warn('add_keyword not yet implemented')
        #app.add_keyword(session=a.d.session, keyword_text=line)
        app.add_item(session=a.d.session, search_type='keyword', new_name=line)
        
    def help_add_keyword(self, line):
        print('Not implemented yet; you can add keywords when adding articles')
    
    def do_add_keyword_to_article(self, line):
        warnings.warn('add_keyword_to_article not yet complete')
        app.add_keyword_to_article(session=a.d.session, entry_id=line)
        
    def help_add_keyword_to_article(self):
        print('searches by article and lets the user add keywords to it')
        print('e.g. add_keyword_to_article 4')
        print('lets the user cycle through keywords and add one to the article')
    
    pub_parser = argparse.ArgumentParser()
    pub_parser.add_argument('-t', '--title', nargs='+', help='title of publication')
    pub_parser.add_argument('-l', '--url', help='link to publication home page')
    
    @cmd2.with_argparser(pub_parser)
    def do_add_publication(self, args):
        '''Adds a new publication'''
        app.add_pub_or_cat(session=a.d.session, new_name=' '.join(args.title),
                           second_item=args.url, add_type='publication')
    
    sec_parser = argparse.ArgumentParser()
    sec_parser.add_argument('-n', '--section_name', nargs='+', help='name of section')
    
    @cmd2.with_argparser(sec_parser)
    def do_add_section(self, args):
        '''Adds a new section to the roundup'''
        warnings.warn('add_section not yet tested')
        app.add_item(session=a.d.session, search_type='section',
                     new_name=' '.join(args.section_name))
    
    def do_search_exact_name(self, line):
        app.search_exact_name(line=line, session=a.d.session)
        
    def help_search_exact_name(self):
        roundup_help.search_exact_name_help()
    
    id_search_parser = argparse.ArgumentParser()
    id_search_parser.add_argument('-st', '--search_type', help='type of search')
    id_search_parser.add_argument('-id', '--item_id', help='numerical id of item')
    
    @cmd2.with_argparser(id_search_parser)
    def do_search_by_id(self, args):
        '''Search by id, with search types entry, category, publication, section, and author'''
        app.search_by_id(search_type=args.search_type, item_id=args.item_id, session=a.d.session)
    
    def do_name_search(self, line):
        '''Searches for items using the name'''
        warnings.warn('name_search not tested yet')
        app.name_search(session=a.d.session, line=line)
    
    def do_get_entries_by_category(self, line):
        '''We will replace this command, but I am keeping it here
        to observe its syntax when writing other commands'''
        app.get_entries_by_category(session=a.d.session, line=line)
        
    def help_get_entries_by_category(self):
        print("Enter a category name, and the program will find all entries")
        print("in that category.")
    
    #move the division of the line from the app.py file to this notebook
    
    count_parser = argparse.ArgumentParser()
    count_parser.add_argument('-d','--date_range', nargs=2, help='start date, end_date')
    
    @cmd2.with_argparser(count_parser)
    def do_article_count(self, args):
        app.date_range_count(session=a.d.session,
                             start_date = args.date_range[0],
                            end_date = args.date_range[1])
        
    def help_article_count(self):
        roundup_help.article_count_help()
    
    @cmd2.with_argparser(count_parser)
    def do_articles_needed(self, args):
        app.articles_needed(start_date=args.date_range[0],
                            end_date=args.date_range[1],
                            session=a.d.session)
    
    def do_edit_entry(self, line):
        app.edit_entry(session=a.d.session, entry_id=line)
        
    def help_edit_entry(self):
        roundup_help.edit_entry_help()
    
    del_parser = argparse.ArgumentParser()
    del_parser.add_argument('-ty', '--item_type',
                            help='item type e.g. entry, category, section, author, publication')
    del_parser.add_argument('-id', '--id_value', help='item id')
    
    @cmd2.with_argparser(del_parser)
    def do_delete_item(self, args):
        '''Delete item '''
        warnings.warn('Unified delete function not fully tested')
        app.delete_item(session=a.d.session, model=args.item_type, id_value=args.id_value)
        
    def do_delete_entry_keyword(self, line):
        warnings.warn('Entry keyword removal not tested')
        app.delete_entry_keyword(session=a.d.session, entry_id=line)
        
    def help_delete_entry_keyword(self):
        roundup_help.delete_entry_keyword()
    
    display_parser = argparse.ArgumentParser()
    display_parser.add_argument('-s', '--section_id', help='section_id')
    
    @cmd2.with_argparser(display_parser)
    def do_display_categories(self, args):
        '''Displays category names for user convenience'''
        try:
            if args.section_id.isnumeric() == True:
                app.display_categories(section_id=args.section_id)
        except AttributeError:
            app.display_categories()
        
    def do_display_sections(self, line):
        '''Enter without a prefix, displays a list of all sections in the database'''
        app.display_sections()
    
    finalize_parser = argparse.ArgumentParser()
    finalize_parser.add_argument('-d', '--date', help='search a single date')
    finalize_parser.add_argument('-r', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')
    
    @cmd2.with_argparser(finalize_parser)
    def do_finalize(self, args):
        '''searches for articles without descriptions and lets user edit them'''
        if args.date:
            app.finalize2(session=a.d.session, start_date =args.date, end_date=args.date)
        elif args.date_range:
            app.finalize2(session=a.d.session, start_date = args.date_range[0],
                          end_date=args.date_range[1])
        else:
            print('Please enter date or date range. Check help for details')
            return
        
    def do_export_docx(self, line):
        '''Exports a roundup in docx form. The "line" argument is deleted by the function'''
        app.create_docx_roundup(line)
    
    export_parser = argparse.ArgumentParser()
    export_parser.add_argument('-t', '--title', nargs='*', help='roundup title')
    export_parser.add_argument('-f',
        '--filename', help='filename (same directory as the app)')
    export_parser.add_argument('-r', '--date_range', nargs=2,
                                 help='search the dates between the start and end dates')
    
    @cmd2.with_argparser(export_parser)
    def do_export_html(self, args):
        '''Export an html version of the roundup'''
        warnings.warn('export_html implementation in testing phase')
        app.export_html2(session=a.d.session, program=args.filename,
                        start_date=parse(args.date_range[0]).date(),
                         end_date=parse(args.date_range[1]).date(),
                        title=' '.join(args.title))
    
    def do_exit(self, arg):
        '''Exits the program, any existing database connections will be closed'''
        a.close()
        print('Exiting Roundup Generator')
        return True
    
if __name__ == '__main__':    
    a=app.App()
    a.setup()
    RoundupCMD().cmdloop()