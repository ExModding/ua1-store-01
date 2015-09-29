# from flask_ldap3_login import LDAP3LoginManager
from flask_login import LoginManager, login_user, UserMixin, current_user
from app import ldap_manager, login_manager, db, models
#from app.models import User

# from flask.ext.ldap3_login.forms import LDAPLoginForm
# Create a dictionary to store the users in when they authenticate
# This example stores users in memory.

#users = models.User.query.all()
#print("*-*-*-*", users)

# Declare an Object Model for the user, and make it comply with the
# flask-login UserMixin mixin.
class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn
#        return self

    def is_anonymous(self):
        return False


# Declare a User Loader for Flask-Login.
# Simply returns the User if it exists in our 'database', otherwise
# returns None.
@login_manager.user_loader
def load_user(id):
#    if models.User.query.filter_by(dn=id).first():
#        get_user = models.User.query.filter_by(dn=id).first()
#        user = User(dn = get_user.dn, username=get_user.username, data=get_user.data)
#        print('Fuck 1', user)
#        return user
    if id in users:
        return users[id]
    else:
        return None


# Declare The User Saver for Flask-Ldap3-Login
# This method is called whenever a LDAPLoginForm() successfully validates.
# Here you have to save the user, and return it so it can be used in the
# login controller.
@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    user = User(dn, username, data)
#    users[dn] = user
    new_user = models.User(data=data, username=username, dn=dn)
    db.session.add(new_user)
    return user


#@ldap_manager.save_user
#def save_user(dn, username, data, memberships):
#    user = User(dn, username, data)
#    new_user = User(data=user)
#    db.session.add(new_user)
#    users[dn] = user
#    return user

users = {}
for user in models.User.query.all():
    users[user.dn] = User(dn=user.dn, username=user.username, data=user.data)
    print(users)