import flask_admin
from flask_admin import expose


class MyAdminIndexView(flask_admin.AdminIndexView):

    @expose('/')
    def admin_index(self):
        return super(MyAdminIndexView, self).index()
