import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime, date

from sqlalchemy import Column, Integer, Numeric, String, Table, ForeignKey, Date, func
from sqlalchemy.orm import relationship, synonym
from sqlalchemy.ext.declarative import declarative_base, synonym_for
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

Base = declarative_base()


authorentries_table = Table('authorentries', Base.metadata,
    Column('entry_id', Integer(), ForeignKey("entries.entry_id"),
           primary_key=True),
    Column('author_id', Integer(), ForeignKey("authors.author_id"),
           primary_key=True)
)

keywordentries_table = Table('keywordentries', Base.metadata,
    Column('keyword_id', Integer(), ForeignKey("keywords.keyword_id"),
           primary_key=True),
    Column('entry_id', Integer(), ForeignKey("entries.entry_id"),
           primary_key=True)
)


class Introduction(Base):
    ''''''
    __tablename__ = 'Introductions'
    introduction_id = Column(Integer(), primary_key=True)
    name = Column(String(100), index=True, nullable=False)
    text = Column(String(2000), nullable=False)
    
    def __repr__(self):
        return f'''Introduction(id='{self.introduction_id}', name='{self.name}')
Text: {self.text}'''

    @hybrid_property
    def id_value(self):
        return self.introduction_id

class Publication(Base):
    
    @classmethod
    def from_input(cls, url=None):
        title = input('Enter publication title: ')
        if url == None:
            url = input('Enter publication url: ')
        else:
            url = url
        return cls(title=title, url=url)
    
    __tablename__ = 'publications'
    publication_id = Column(Integer(), primary_key=True)
    title = Column(String(100), index=True, unique=True)
    url = Column(String(100), default=None, unique=True)
    entries = relationship("Entry", back_populates="publication")
    name=synonym('title')
    second_item=synonym('url') #we use this synonym for functions that affect more than one type of object
    
    def __repr__(self):
        return f'''Pub(id='{self.publication_id}' title='{self.title}', 'url={self.url})'''
    
    @hybrid_property
    def name_value(self):
        return self.title
    
    @hybrid_property
    def id_value(self):
        return self.publication_id
    
    @hybrid_property
    def items(self):
        return self.entries
    
class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer(), primary_key=True)
    author_name = Column(String(100))
    entries = relationship("Entry", secondary=lambda: authorentries_table)
    entry_names = association_proxy('entries', 'entry_name')
    name=synonym('author_name')
    
    def __repr__(self):
        return "Author(id='{self.author_id}' name='{self.author_name}')".format(self=self)
    
    @hybrid_property
    def id_value(self):
        return self.author_id
    
    @hybrid_property
    def name_value(self):
        return self.author_name
    
    @name_value.setter
    def name_value(self, name_value):
        self.author_name = name_value
    
    @hybrid_property
    def items(self):
        return self.entries
    
class Category(Base):
    
    @classmethod
    def from_input(cls, session, category_name=None):
        if category_name == None:
            name=input('Enter category name: ')
        else:
            name=category_name
        section_list = session.query(Section).all()
        print(section_list)
        section_id = input('Enter section id: ')
        return cls(name=name, section_id=section_id)
    
    __tablename__ = 'categories'
    
    category_id = Column(Integer(), primary_key=True)
    name = Column(String(255), index=True)
    section_id = Column(Integer(), ForeignKey('sections.section_id'))
    section=relationship("Section", back_populates="categories")
    entries = relationship("Entry", back_populates="category")
    entry_names = association_proxy('entries', 'entry_name')
    second_item = synonym('section_id')
    
    def __repr__(self):
        return "Category(id='{self.id_value}' name='{self.name}', section={self.section_id})".format(self=self)
    
    @property
    def wrapped_html_string(self):
        return f'''<p>{self.name}</p>'''

    @property
    def wrapped_jsx_string(self):
        title = self.name.title()
        return f'''<p><i>{title}</i></p>\n'''
    
    @hybrid_property
    def id_value(self):
        return self.category_id
    
    @hybrid_property
    def name_value(self):
        '''Used so each datatype has a name value that is uniform across all datatypes'''
        return self.name
    
    @hybrid_property
    def items(self):
        '''Used to give each datatype a uniform value for any groups of items it contains'''
        return self.entries
    
class Section(Base):
    __tablename__ = 'sections'
    
    section_id = Column(Integer(), primary_key=True)
    name = Column(String(100))
    categories = relationship("Category", back_populates="section")
    
    def __repr__(self):
        return "Section(id='{self.id_value}', name='{self.name}')".format(self=self)

    @property
    def wrapped_html_string(self):
        return '''<p>{0}</p>'''.format(self.name)
    
    @property
    def wrapped_jsx_string(self):
        title = self.name.title()
        return f'''<p><b>{title}</b></p>\n'''#.format(self.name)
    
    @hybrid_property
    def name_value(self):
        return self.name
    
    @hybrid_property
    def id_value(self):
        return self.section_id
    
    @hybrid_property
    def items(self):
        return self.categories

class Entry(Base):
    '''We use the name entries to avoid overriding the Article object from the
    newspaper module'''
    __tablename__ = 'entries'

    entry_id = Column(Integer(), primary_key=True)
    entry_name = Column(String(100), index=True)
    entry_url = Column(String(255))
    description = Column(String(500))
    summary = Column(String(1500), default=None)
    date = Column(Date(), default=date.today())
    authors = relationship("Author", secondary=lambda: authorentries_table)
    author_names = association_proxy("authors", 'name')
    category_id = Column(Integer(), ForeignKey('categories.category_id'))
    category=relationship("Category", back_populates="entries")
    category_name = association_proxy('category', 'name')
    publication_id = Column(Integer(), ForeignKey('publications.publication_id'))
    publication = relationship("Publication", back_populates="entries")
    #publication_title = association_proxy('publications', 'title')
    keywords = relationship("Keyword", secondary=lambda: keywordentries_table)
    keyword_list = association_proxy('keywords', 'word')
    name=synonym('entry_name')
    
    def __init__(self, entry_name, entry_url, description, date,
                publication_id, category_id, keywords, summary=None, authors=None):
        self.entry_name = entry_name
        self.entry_url = entry_url
        self.description = description
        self.date = date
        self.category_id=category_id
        self.publication_id = publication_id
        self.authors=authors
        self.keywords=keywords
        self.summary=summary
        
    def __repr__(self):
        return "Entry(entry_name='{self.entry_name}',\n " \
                    "entry_url='{self.entry_url}',\n " \
                    "description='{self.description}',\n " \
                    "date='{self.date}', \n"\
                    "entry_id='{self.entry_id}', \n"\
                    "category={self.category}, \n"\
                    "authors={self.authors})".format(self=self)
        
    @property
    def get_date_formatted(self):
        return f'{self.date.month}/{self.date.day}/{self.date.year}'
    
    @property
    def wrapped_html_string(self):
        '''For use when creating wrapped html strings for html files'''
        template = '<p><a href ={0}>{1}</a> ({2}) {3}</p>\n'
        return template.format(self.entry_url, self.entry_name, self.get_date_formatted,
                               self.description)
        
    @property
    def wrapped_jsx_string(self):
        '''For use when creating wrapped html strings for html files'''
        template = '<p><a href ="{0}">{1}</a> ({2}) {3}</p>\n'
        return template.format(self.entry_url, self.entry_name, self.get_date_formatted,
                               self.description)
    
    @hybrid_property
    def name_value(self):
        return self.entry_name
    
    @name_value.setter
    def name_value(self, new_name):
        self.entry_name = new_name
    
    @hybrid_property
    def id_value(self):
        return self.entry_id
    
    @hybrid_property
    def items(self):
        return self.keywords+self.authors

class Keyword(Base):
    __tablename__ = 'keywords'
    keyword_id = Column(Integer(), primary_key = True)
    word = Column(String(50), index=True, unique=True)
    entries = relationship("Entry", secondary=lambda: keywordentries_table)
    entry_names = association_proxy('entries', 'entry_name')
    name=synonym('word')
    #create table joining keywords and entries
    
    def __repr__(self):
        return "id={self.keyword_id} {self.word}".format(self=self)
    
    @hybrid_property
    def name_value(self):
        return self.word
    
    @hybrid_property
    def id_value(self):
        return self.keyword_id
    
    @hybrid_property
    def items(self):
        return self.entries
    
#Keywords will have a many to many relationship with entries and stories

class DataAccessLayer:
    def __init__(self):
        self.engine = None
        self.conn_string = 'sqlite:///roundup_db3.db'
        
    def connect(self):
        self.engine = create_engine(self.conn_string)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
dal = DataAccessLayer()