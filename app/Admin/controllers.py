from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, Admin
from app import db
from app.models import User, Article
from flask_login import current_user
from flask import redirect, url_for, flash, request


class AdminMixin:
    def is_accessible(self):
        return True if current_user.is_authenticated and current_user.has_admin() else False

    def inaccessible_callback(self, name, **kwargs):
        flash('Вы не имеете доступ к этой странице!', category='error')
        return redirect(url_for('main.index', next=request.url))


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class UserAdminView(AdminMixin, ModelView):
    form_columns = ['username', 'email', 'admin']
    can_create = False
    column_exclude_list = ['image', 'password']


admin = Admin(name='MicroBlog', index_view=HomeAdminView(name='Админка'))
admin.url = '/'
admin.add_view(UserAdminView(User, db.session))
admin.add_view(AdminView(Article, db.session))

