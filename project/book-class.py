import time
import argparse

def timing_decorator(func):
    def inner_call(*args,**kwargs):
        timer_start = time.perf_counter()
        func(*args,**kwargs)
        timer_end = time.perf_counter()
        timer = timer_end - timer_start
        print(f"---- execution time: {timer:.4f} ----")
    return inner_call

class LogFile:
    def __init__(self, filename: str):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, "a+", encoding="utf-8")
        return self

    def write_log(self, text: str):
        if self.file:
            self.file.write(text)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

class item():
    allitem = []
    bookitem = []
    magazineitem = []
    def __init__(self,title=str,year=int):
        self.title = title
        self.year = year
    def __str__(self):
        return f"title: {self.title} - year: {self.year}"
    
    @timing_decorator
    def search_item(self,title=str,type="all"):
        if type == "all":
            for all in item.allitem:
                if all['title'] == title:
                    print(f"item found! title: {all['title']} year: {all['year']}")
        elif type == "book":
            for book in item.bookitem:
                if book['title'] == title:
                    print(f"Book found! title: {book['title']} year: {book['year']} author: {book['author']}")
        elif type == "magazine":
            for magazine in item.magazineitem:
                if magazine['title'] == magazine:
                    print(f"magazine found! title: {magazine['title']} year: {magazine['year']} issue_number: {magazine['issue_number']}")
        else:
            print(f"{title} not found!")
    
    def iterate_items(self, type="all"):
        cont = 0
        if type == "all":
            for a in item.allitem:
                cont += 1
                yield f"item{cont} - {a['title']} {a['year']}"
        elif type == "book":
            for a in item.allitem:
                cont += 1
                yield f"book{cont} - {a['title']} {a['year']} by {a['author']}"
        elif type == "magazine":
            for a in item.allitem:
                cont += 1
                yield f"magazine{cont} - {a['title']} {a['year']} issue number: {a['issue_number']}"
        else:
            print(f"type {type} not found!")

class Book(item):
    def __init__(self,title=str,year=int,author=str):
        self.title = title
        self.year = year
        self.author = author
        self.list = {"title":self.title,"year":self.year,"author":self.author}
        item.allitem.append(self.list)
        item.bookitem.append(self.list)
        with LogFile("log.text") as logger:
            logger.write_log(f"{self.title} book add\n")

class Magazine(item):
    def __init__(self,title=str,year=int,magazine=int):
        self.title = title
        self.year = year
        self.magazine = magazine
        self.list = {"title":self.title,"year":self.year,"magazine":self.magazine}
        item.allitem.append(self.list)
        item.magazineitem.append(self.list)
        with LogFile("log.text") as logger:
            logger.write_log(f"{self.title} magazine add\n")

parser = argparse.ArgumentParser(description="Book and magazine management")

parser.add_argument('--addbook',help="Add books to items",default=None)
parser.add_argument('--addmagazine',help="Add magazine to items",default=None)
parser.add_argument('--list',help="List of books and magazines",default=None)
parser.add_argument('--search',help="Search between books and magazines",default=None)

args = parser.parse_args()

items = item()

if args.addbook != None:
    items = item(Book(args.addbook))
if args.addmagazine != None:
    items = item(Magazine(args.addmagazine))
if args.list != None:
    for ITEM in items.iterate_items():
        print(ITEM)
if args.search != None:
    items.search_item(args.search)
