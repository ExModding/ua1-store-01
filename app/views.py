from app import app, models, db, login_manager
from flask import render_template, session, redirect, url_for, flash, request, g
from flask_login import login_user, current_user, logout_user, login_required, user_loaded_from_cookie
from flask.ext.ldap3_login.forms import LDAPLoginForm
from app.ldap import User, LoginManager
from config import ACCESS_ADD_ITEM, ACCESS_APPROVE
#from app.models import PC
from datetime import datetime
from app.forms import AddPC, AddMonitor
from app.ldap import users

login_manager.login_view = 'login'
print('******', users)

#@login_manager.user_loader
#def load_user(id):
#    return User.get_id(id)


@app.route('/', methods=['GET', 'POST'])

#@login_manager.user_loader
def index():
    if not current_user.is_authenticated:
            return redirect(url_for('login'))
    print('******', users)
    # Redirect users who are not logged in.#
#    if not current_user.is_authenticated:
#        return redirect(url_for('login'))
#    else:
#        user = current_user.username
    user = current_user
    print(session)
    pc_list = models.PC.query.filter(models.PC.status_id.in_([2, 3]))
    monitor_list = models.Monitor.query.filter(models.Monitor.status_id.in_([2, 3]))

    if request.method == 'POST' and request.form.get("pc_reserve"):
        pc_id = request.form.get("pc_reserve")
        print(request.form.get("pc_reserve"))
        print(models.PC.query.filter_by(id=pc_id).first().status_id)
        if models.PC.query.filter_by(id=pc_id).first().status.description == 'Reserved':
            print('Already booked :-(')
            flash('Похоже, что кто-то другой уже успел зарезервировать эту позицию :-(')
        else:
            models.PC.query.filter_by(id=pc_id).update(dict(status_id='3',
                                                            buyer=current_user.username,
                                                            reserved_time=datetime.now()))
            return redirect(url_for('reserved'))
        db.session.commit()

    elif request.method == 'POST' and request.form.get("monitor_reserve"):
        monitor_id = request.form.get("monitor_reserve")
        print(request.form.get("monitor_reserve"))
        print(models.Monitor.query.filter_by(id=monitor_id).first().status_id)
        if models.Monitor.query.filter_by(id=monitor_id).first().status.description == 'Reserved':
            print('Already booked :-(')
            flash('Похоже, что кто-то другой уже успел зарезервировать эту позицию :-(')
        else:
            models.Monitor.query.filter_by(id=monitor_id).update(dict(status_id='3',
                                                                      buyer=current_user.username,
                                                                      reserved_time=datetime.now()))
            return redirect(url_for('reserved'))
        db.session.commit()

    return render_template("index.html", title="Home", approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM,
                           PC_list=pc_list,
                           monitor_list=monitor_list, user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    user=current_user
    # Instantiate a LDAPLoginForm which has a validator to check if the user
    # exists in LDAP.
    form = LDAPLoginForm()
    if form.validate_on_submit():
        # Successfully logged in, We can now access the saved user object
        # via form.user.
        print(form.user)
        login_user(form.user)  # Tell flask-login to log them in.
        flash('Вы успешно авторизованы под именем {}'.format(current_user.username))

        return redirect(request.args.get('next') or url_for('index'))  # Send them home
    return render_template('login.html', form=form, approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM, user=user)


@app.route('/reserved')
def reserved():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return render_template('reserve_page.html', approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM)


@app.route('/add_pc', methods=['GET', 'POST'])
@login_required
def add_pc():
#    if current_user.is_authenticated:
#        if current_user.username not in ACCESS_ADD_ITEM:
#            return redirect(url_for('login'))
#    else:
#        return redirect(url_for('login'))

    form = AddPC()
    text = 'системный блок'
    if request.method == 'POST' and form.validate_on_submit():
        print('ok')
        new_pc = models.PC(CPU=form.cpu.data,
                           RAM=form.ram.data,
                           HDD=form.hdd.data,
                           price=form.price.data,
                           comment=form.comment.data,
                           assembly_time=datetime.now(),
                           assembly_by=current_user.username,
                           status_id='1')
        db.session.add(new_pc)
        db.session.commit()
        flash("Позиция успешно добавлена.")
        return redirect(url_for('add_pc'))
    return render_template('add_item.html', approve=ACCESS_APPROVE, form=form, add_item=ACCESS_ADD_ITEM, text=text)


@app.route('/add_monitor', methods=['GET', 'POST'])
def add_monitor():
    if current_user.is_authenticated:
        if current_user.username not in ACCESS_ADD_ITEM:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

    form = AddMonitor()
    text = 'монитор'
    if request.method == 'POST' and form.validate_on_submit():
        print('ok')
        new_monitor = models.Monitor(manufacturer=form.manufacturer.data,
                                     monitor_model=form.monitor_model.data,
                                     size=form.size.data,
                                     price=form.price.data,
                                     comment=form.comment.data,
                                     assembly_time=datetime.now(),
                                     assembly_by=current_user.username,
                                     status_id='1')
        db.session.add(new_monitor)
        db.session.commit()
        flash("Позиция успешно добавлена.")
        return redirect(url_for('add_monitor'))
    return render_template('add_item.html', approve=ACCESS_APPROVE, form=form, add_item=ACCESS_ADD_ITEM, text=text)


@app.route('/add_other')
def add_other():
    if current_user.is_authenticated:
        if current_user.username not in ACCESS_ADD_ITEM:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

    return render_template('add_item.html', approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM)


@app.route('/manage_pc', methods=['GET', 'POST'])
def manage_pc():
    if current_user.is_authenticated:
        if current_user.username not in ACCESS_ADD_ITEM:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    pc_list = models.PC.query.all()
    if request.method == 'POST':
        if request.form.get("reserve"):
            pc_id = request.form.get("reserve")
            if models.PC.query.filter_by(id=pc_id).first().status.description == 'Reserved':
                print('Already booked :-(')
                flash('Похоже, что кто-то другой уже успел зарезервировать этот товар :-(')
            else:
                models.PC.query.filter_by(id=pc_id).update(dict(status_id='3',
                                                                buyer=current_user.username,
                                                                reserved_time=datetime.now()))
                flash('Позиция зарезервирована')

        elif request.form.get("approve"):
            pc_id = request.form.get("approve")
            if models.PC.query.filter_by(id=pc_id).first().status.description == 'Approved':
                print('Already approved')
                flash('Похоже, что кто-то другой уже успел подтвердить эту позицию :-(')
            else:
                models.PC.query.filter_by(id=pc_id).update(dict(status_id='2',
                                                                approved_by=current_user.username,
                                                                approved_time=datetime.now()))
                flash('Позиция подтверждена')

        elif request.form.get("sold"):
            pc_id = request.form.get("sold")
            if models.PC.query.filter_by(id=pc_id).first().status.description == 'Sold':
                print('Already sold')
                flash('Похоже, что кто-то другой уже успел продать эту позицию :-(')
            else:
                models.PC.query.filter_by(id=pc_id).update(dict(status_id='4',
                                                                sold_by=current_user.username,
                                                                sale_time=datetime.now()))
                flash('Позиция продана')

        db.session.commit()

    return render_template('manage_pc.html', pc_list=pc_list, approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM)


@app.route('/manage_monitor', methods=['GET', 'POST'])
def manage_monitor():
    if current_user.is_authenticated:
        if current_user.username not in ACCESS_ADD_ITEM:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    monitor_list = models.Monitor.query.all()
    if request.method == 'POST':
        if request.form.get("reserve"):
            monitor_id = request.form.get("reserve")
            if models.Monitor.query.filter_by(id=monitor_id).first().status.description == 'Reserved':
                print('Already booked :-(')
                flash('Похоже, что кто-то другой уже успел зарезервировать эту позицию :-(')
            else:
                models.Monitor.query.filter_by(id=monitor_id).update(dict(status_id='3',
                                                                          buyer=current_user.username,
                                                                          reserved_time=datetime.now()))
                flash('Позиция зарезервирована')

        elif request.form.get("approve"):
            monitor_id = request.form.get("approve")
            if models.Monitor.query.filter_by(id=monitor_id).first().status.description == 'Approved':
                print('Already approved')
                flash('Похоже, что кто-то другой уже успел подтвердить эту позицию :-(')
            else:
                models.Monitor.query.filter_by(id=monitor_id).update(dict(status_id='2',
                                                                          approved_by=current_user.username,
                                                                          approved_time=datetime.now()))
                flash('Позиция подтверждена')

        elif request.form.get("sold"):
            monitor_id = request.form.get("sold")
            if models.Monitor.query.filter_by(id=monitor_id).first().status.description == 'Sold':
                print('Already sold')
                flash('Похоже, что кто-то другой уже успел продать эту позицию :-(')
            else:
                models.Monitor.query.filter_by(id=monitor_id).update(dict(status_id='4',
                                                                          sold_by=current_user.username,
                                                                          sale_time=datetime.now()))
                flash('Позиция продана')

        db.session.commit()

    return render_template('manage_monitor.html', monitor_list=monitor_list, approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM)


@app.route('/edit_pc', methods=['GET', 'POST'])
def edit_pc():
    if current_user.is_authenticated:
        if current_user.username not in ACCESS_ADD_ITEM:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    form = AddPC()
    if request.method == 'POST'and request.form.get("edit"):
        pc_id = request.form.get("edit")
        form.cpu.data = models.PC.query.filter_by(id=pc_id).first().CPU
        form.ram.data = models.PC.query.filter_by(id=pc_id).first().RAM
        form.mb.data = models.PC.query.filter_by(id=pc_id).first().MB
        form.video.data = models.PC.query.filter_by(id=pc_id).first().video
        form.hdd.data = models.PC.query.filter_by(id=pc_id).first().HDD
        form.price.data = models.PC.query.filter_by(id=pc_id).first().price
        form.comment.data = models.PC.query.filter_by(id=pc_id).first().comment
        form.pc_id.data = models.PC.query.filter_by(id=pc_id).first().id

    if request.method == 'POST' and form.validate_on_submit():
        print('ok')
        models.PC.query.filter_by(id=form.pc_id.data).update(dict(CPU=form.cpu.data,
                                                        RAM=form.ram.data,
                                                        HDD=form.hdd.data,
                                                        price=form.price.data,
                                                        comment=form.comment.data))
        db.session.commit()
        flash("Позиция {} успешно обновлена.".format(form.pc_id.data))
        return redirect(url_for('manage'))
    return render_template('edit_pc.html', form=form, approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM)


@app.route('/edit_monitor', methods=['GET', 'POST'])
def edit_monitor():
    if current_user.is_authenticated:
        if current_user.username not in ACCESS_ADD_ITEM:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
    form = AddMonitor()
    if request.method == 'POST'and request.form.get("edit"):
        monitor_id = request.form.get("edit")
        form.manufacturer.data = models.Monitor.query.filter_by(id=monitor_id).first().manufacturer
        form.monitor_model.data = models.Monitor.query.filter_by(id=monitor_id).first().monitor_model
        form.size.data = models.Monitor.query.filter_by(id=monitor_id).first().size
        form.price.data = models.Monitor.query.filter_by(id=monitor_id).first().price
        form.comment.data = models.Monitor.query.filter_by(id=monitor_id).first().comment
        form.monitor_id.data = models.Monitor.query.filter_by(id=monitor_id).first().id

    if request.method == 'POST' and form.validate_on_submit():
        print('ok')
        models.Monitor.query.filter_by(id=form.monitor_id.data).update(dict(manufacturer=form.manufacturer.data,
                                                        monitor_model=form.monitor_model.data,
                                                        size=form.size.data,
                                                        price=form.price.data,
                                                        comment=form.comment.data))
        db.session.commit()
        flash("Позиция {} успешно обновлена.".format(form.monitor_id.data))
        return redirect(url_for('manage_monitor'))
    return render_template('edit_monitor.html', form=form, approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM)



@app.route('/test')
def test():
#    if not current_user.is_authenticated:
#        return redirect(url_for('login'))
    return render_template('test.html', approve=ACCESS_APPROVE, add_item=ACCESS_ADD_ITEM)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))