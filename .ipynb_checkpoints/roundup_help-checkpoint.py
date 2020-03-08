def add_article_help():
    print('adds new article to database')
    print('paste or type the url directly after the command')
    print('add_article [article_url]')

def add_category_help():
    print('Creates a new category')
    print('add_category [category_name]')
    print('eg. add_category Canada creates a category for Canada')
    
def add_section_help():
    print('''Adds a new section to the database''')
    print('''e.g. add_section [section_name] will add a new section with
    that name. Section names must be unique.''')

def article_count_help():
    print('Article_count prints out a list of how many articles are in each')
    print('category. It works either by itself or with a start and end state')
    print('By itself (prints the article counts for whole database):')
    print('article_count')
    print('With date range:')
    print('article_count [start_date] [end_date]')
    print('e.g.')
    print('article_count 01/01/2020 01/31/2020')
    
def articles_needed_help():
    print('Identifies how many articles needed to reach minimum of 5')
    print('format: articles_needed [start_date] [end_date]')
    print('e.g. articles_needed 02/01/2020 02/29/2020')

def delete_entry_keyword():
    print('example: delete_entry_keyword [entry_id]')
    print('Cycles through the keywords in an entry')
    print('The user can choose to delete the keywords as they come up')    

def delete_item_help():
    print('Deletes an item from the database')
    print('delete_item [item_type] [item_id]')
    print('for example:')
    print('delete_item category 23')
    print('deletes the category with the id of 23')
    print('will not delete a section, category, or publication that has items in it')
    print('shows user the items that must be deleted first')

def display_categories_help():
    print('display_categories without a suffix displays a list of')
    print('all categories in the database')
    print('display_categories [section_id]')
    print('displays all categories in that section')

def edit_entry_help():
    print('''Edits an entry. This function rotates among attributes and lets you
    edit them one by one.
    Example: edit_entry 1 edits the entry with entry_id 1''')

def export_docx_help():
    print('Enter "export_docx" without a suffix to export an article')
    print('The program will take user input to get specifications for the roundup')
    
def export_html_help():
    print('''export_html is entered with no suffix,
    the command prompts the user for information about the roundup
    and then exports a roundup based on user specifications''')
    
def finalize_help():
    print('searches for articles without descriptions and lets user edit them')
    print('finalize [start_date] [end_date]')
    print('e.g. finalize 02/01/2020 02/29/2020')

def search_by_id_help():
    print('search_id [search_type] [item_id]')
    print('e.g. search_id entry 4')
    print('Search types: entry, publication, section, category, keyword')
    
def search_exact_name_help():
    print('Enter the EXACT name of an Entry, Publication, Keyword, Section, or Author')
    print('e.g. search_exact_name publication The Guardian') 
    
##deprecated