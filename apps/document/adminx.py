from djangoer.utils import CustomerRulesAdmin
from .models import ExampleModel

import xadmin

"""
choose icon from https://fontawesome.com/v4.7.0/icons/
"""


class ExampleModelAdmin(CustomerRulesAdmin):
    list_display = ["name"]
    model_icon = 'fa fa-book'


xadmin.site.register(ExampleModel, ExampleModelAdmin)
