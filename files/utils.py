from flask import render_template, redirect, flash, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_babel import gettext
from sqlalchemy.exc import IntegrityError, DataError, DatabaseError, InterfaceError, InvalidRequestError
from werkzeug.routing import BuildError
from dao.models.models import User, Contact
from files.forms import login_form, register_form, contact_form
from files.implemented import user_service, contact_service
from files.setup_db import db
import random


def login():
    """Users authorization"""
    form = login_form()
    print(request.args.get('path'))
    if form.validate_on_submit():
        if request.method == 'POST':
            try:
                username = form.username.data
                password = form.password.data
                user = user_service.get_by_username(username)

                if user and user_service.compare_password(user.password, password):
                    login_user(user)
                    return redirect('/users/list/')
                else:
                    flash(gettext("Invalid Username or password!"), "danger")
            except Exception as e:
                flash(e, "danger")

    return render_template("auth.html",
        form=form,
        text=gettext("Login"),
        title=gettext("Login"),
        btn_action=gettext("Login"))

def register():
    """New user registration"""
    form = register_form()

    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                username = form.username.data
                password = form.password.data

                data = {
                    "username": username,
                    "password": password,
                }

                user_service.create(data)
                flash(gettext(f"Account Succesfully created!"), "success")
                return redirect(url_for("login"))
            except InvalidRequestError:
                db.session.rollback()
                flash(gettext(f"Something went wrong!"), "danger")
            except IntegrityError:
                db.session.rollback()
                flash(gettext(f"User already exists!"), "warning")
            except DataError:
                db.session.rollback()
                flash(gettext(f"Invalid Entry"), "warning")
            except InterfaceError:
                db.session.rollback()
                flash(gettext(f"Error connecting to the database"), "danger")
            except DatabaseError:
                db.session.rollback()
                flash(gettext(f"Error connecting to the database"), "danger")
            except BuildError:
                db.session.rollback()
                flash(gettext(f"An error occured!"), "danger")
    return render_template("auth.html",
        form=form,
        text=gettext("Create account"),
        title=gettext("Register"),
        btn_action=gettext("Register account")
        )

@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect('/user/login/')

def users():
    """Users list"""
    if request.method == 'GET':
        users = db.session.query(User).all()
        contacts = db.session.query(Contact).all()
    return render_template('users_list.html', users=users, contacts=contacts, text=gettext("Users"), text1="FAQ")

def user_delete(pk):
    """Delete user by id"""
    if pk != current_user.id:
        user_service.delete(pk)
        flash(gettext(f"User deleted seccessfully"), "success")
        return redirect('/users/list/')
    else: 
        flash(gettext(f"You cannot delete yourself"), "danger")
        return redirect('/users/list/')

def contact():
    """Add a review"""
    form = contact_form()
    answ, nums = captcha()
    if form.validate_on_submit():
        if request.method == 'POST':
            try:
                username = form.username.data
                text = form.text.data
                
                user = user_service.get_by_username(username)
                capt = form.captcha.data

                if int(capt) == answ:
                    data = {
                        'user_id': user.id,
                        'username': username,
                        'text': text,
                    }
                    contact_service.create(data)
                    flash(gettext(f"Review added successfully!"), "success")
                    return redirect("/users/list/")
                else:
                    flash(gettext(f"Captcha was failed!"), "warning")
            except InvalidRequestError:
                db.session.rollback()
                flash(gettext(f"Something went wrong!"), "danger")
            except DataError:
                db.session.rollback()
                flash(gettext(f"Invalid Entry"), "warning")
            except InterfaceError:
                db.session.rollback()
                flash(gettext(f"Error connecting to the database"), "danger")
            except DatabaseError:
                db.session.rollback()
                flash(gettext(f"Error connecting to the database"), "danger")
            except BuildError:
                db.session.rollback()
                flash(gettext(f"An error occured!"), "danger")
    return render_template("contact.html",
    form=form,
    text=gettext("Add a review"),
    title=gettext("Add a review"),
    btn_action=gettext("Add a review"),
    nums=nums)

def captcha():
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)
    nums = f'{num1} + {num2}'
    answ = num1 + num2
    return answ, nums
