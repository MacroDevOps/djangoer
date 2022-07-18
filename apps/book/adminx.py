from .models import Book


import xadmin

"""
choose icon from https://fontawesome.com/v4.7.0/icons/
"""


class BookAdmin(object):
    list_display = ["name", "author", "username"]
    model_icon = 'fa fa-book'


xadmin.site.register(Book, BookAdmin)
