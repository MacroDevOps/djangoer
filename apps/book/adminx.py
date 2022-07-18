from .models import Book, BookFactory

import xadmin

"""
choose icon from https://fontawesome.com/v4.7.0/icons/
"""


class BookAdmin(object):
    list_display = ["name", "author", "factory"]
    model_icon = 'fa fa-book'


class BookFactoryAdmin(object):
    list_display = ["name"]
    model_icon = 'fa fa-book'


xadmin.site.register(BookFactory, BookFactoryAdmin)
xadmin.site.register(Book, BookAdmin)
