#from app import db, models, admin
#from flask.ext.admin.contrib.sqla import ModelView
#from flask.ext.admin import BaseView, expose
#from app.models import PC, ItemStatus


#class MyView(BaseView):
#    @expose('/')
#    def index(self):
#        return self.render('admin_index.html')
#admin.add_view(MyView(name='Hello'))


#admin.add_view(ModelView(PC, db.session))
#admin.add_view(ModelView(ItemStatus, db.session))