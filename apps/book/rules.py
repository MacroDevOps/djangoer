from __future__ import absolute_import

import rules

@rules.predicate
def is_colleague(user, entry):
    if not entry or not hasattr(user, 'companyuser'):
        return False
    return entry.category_code == user.companyuser.category_code


@rules.predicate
def is_admin(user):
    if not hasattr(user, 'companyuser'):
        return False
    return user.companyuser.is_admin


is_admins = is_admin | rules.is_superuser | is_colleague

# 设置Rules
rules.add_rule('can_view_user', is_admins)
rules.add_rule('can_delete_user', is_admins)
rules.add_perm('can_change_user', is_admins)

# 设置Permissions
rules.add_perm('data_import.view_user', is_admins)
rules.add_perm('data_import.delete_user', is_admins)
rules.add_perm('data_import.add_user', is_admins)
rules.add_perm('data_import.change_user', is_admins)
