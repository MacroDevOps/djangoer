from djangoer.utils import CustomerRulesAdmin
from .models import Book, BookFactory

import xadmin

"""
choose icon from https://fontawesome.com/v4.7.0/icons/
"""


class RulesBookAdmin(CustomerRulesAdmin):
    list_display = ["name", "author", "username", "factory"]
    model_icon = 'fa fa-book'


class RulesBookFactoryAdmin(CustomerRulesAdmin):
    list_display = ["name"]
    model_icon = 'fa fa-book'


xadmin.site.register(Book, RulesBookAdmin)
xadmin.site.register(BookFactory, RulesBookFactoryAdmin)
