from django.contrib.auth import get_permission_codename


class CustomerRulesAdmin(object):
    def has_change_permission(self, obj=None):
        codename = get_permission_codename('change', self.opts)
        return self.user.has_perm('%s.%s' % (self.app_label, codename), obj)

    def has_delete_permission(self, obj=None):
        codename = get_permission_codename('delete', self.opts)
        return self.user.has_perm('%s.%s' % (self.app_label, codename), obj)

    def queryset(self):
        qs = super(CustomerRulesAdmin, self).queryset()
        if self.request.user.is_superuser or self.is_taixiang_admin(self.request.user):
            return qs
        try:
            return qs.filter(company_code=self.request.user.companyuser.company_code)
        except AttributeError:
            return None
