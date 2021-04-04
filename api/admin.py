import flask_admin as admin
from api.models import Book, Transaction, User, db
from api.views import main
from app import app
from flask_admin.contrib.sqla import ModelView

admin = admin.Admin(app, name='api', index_view=main.MyAdminIndexView(),
                    template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Book, db.session))
admin.add_view(ModelView(Transaction, db.session))
