# Name: Matthew Hartigan
# Assignment: CS336 Assignment #9
# Page Name: app.py
# Created: 4/30/2019
# Description: The app.py file for Assignment #9.

from flask import Flask, render_template, request, url_for, session
from functools import wraps
from datetime import datetime
import sqlite3


app = Flask(__name__)
app.secret_key = '@#$%sdf34587#$%asdfeFSv'


# HELPER FUNCTIONS
# DB Connection
def db_connect():
    db_name = 'database_code/conference.sqlite'
    # FIXME Toggle on this db_name to use scripts in database_code subdirectory
    # db_name = 'conference.sqlite'
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row

    return conn


# Status Check
def status(func):
    @wraps(func)
    def wrapper (*args, **kwargs):
        if 'logged_in' in session:
          return func(*args, **kwargs)
        print('failed')
        return "You are not logged in"
    return wrapper


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/activities')
def activities():
    return render_template('activities.html')


@app.route('/admin', methods=['GET', 'POST'])
@status
def admin():
    if request.method == 'POST':
        return_list = []

        # Connect to db
        with db_connect() as db:
            cur = db.cursor()
            if (request.values.get('list') == 'session_1a'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session1='Workshop A' '''
                title = 'All Session 1a Registrants'
            elif (request.values.get('list') == 'session_1b'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session1='Workshop B' '''
                title = 'All Session 1b Registrants'
            elif (request.values.get('list') == 'session_1c'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session1='Workshop C' '''
                title = 'All Session 1c Registrants'
            elif (request.values.get('list') == 'session_2a'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session2='Workshop D' '''
                title = 'All Session 2a Registrants'
            elif (request.values.get('list') == 'session_2b'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session2='Workshop E' '''
                title = 'All Session 2b Registrants'
            elif (request.values.get('list') == 'session_2c'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session2='Workshop F' '''
                title = 'All Session 2c Registrants'
            elif (request.values.get('list') == 'session_3a'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session3='Workshop G' '''
                title = 'All Session 3a Registrants'
            elif (request.values.get('list') == 'session_3b'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session3='Workshop H' '''
                title = 'All Session 3b Registrants'
            elif (request.values.get('list') == 'session_3c'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE session3='Workshop I' '''
                title = 'All Session 3c Registrants'
            elif (request.values.get('list') == 'meal_pack'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE meals='mealpack' '''
                title = 'All Meal Pack Registrants'
            elif (request.values.get('list') == 'dinner_only'):
                sql = '''SELECT firstname, lastname FROM registrants WHERE meals='dinnerday2' '''
                title = 'All Day 2 Dinner Only Registrants'
            elif (request.values.get('list') == 'registrants'):
                sql = '''SELECT firstname, lastname FROM registrants'''
                title = 'All Conference Registrants:'

            cur.execute(sql)
            for person in cur.fetchall():
                return_list.append([person[0], person[1]])

        db.close()

        return render_template('admin.html', title=title, return_list=return_list)

    else:
        return render_template('admin.html')


@app.route('/awards', methods=['GET', 'POST'])
def awards():
    current_votes = {'Mountain Biking': "", 'Road Biking': "", 'Leisure Biking': ""}

    if request.method == 'POST':

        # Connect to db
        with db_connect() as db:
            cur = db.cursor()

            if (request.values.get('nominee') == 'Mountain Biking'):
                sql = ''' UPDATE nominees SET current_votes = current_votes + 1 WHERE nominee_title = 'Mountain Biking' '''
                cur.execute(sql)

            elif (request.values.get('nominee') == 'Road Biking'):
                sql = ''' UPDATE nominees SET current_votes = current_votes + 1 WHERE nominee_title = 'Road Biking' '''
                cur.execute(sql)

            elif (request.values.get('nominee') == 'Leisure Biking'):
                sql = ''' UPDATE nominees SET current_votes = current_votes + 1 WHERE nominee_title = 'Leisure Biking' '''
                cur.execute(sql)
            db.commit()

            # Extract vote totals from db
            sql = ''' SELECT current_votes FROM nominees '''
            cur.execute(sql)
            current_votes ['Mountain Biking'] = cur.fetchall()[0][0]
            cur.execute(sql)
            current_votes['Road Biking'] = cur.fetchall()[1][0]
            cur.execute(sql)
            current_votes['Leisure Biking'] = cur.fetchall()[2][0]

        db.close()

        return render_template('awards.html', vote_submitted=True, current_votes=current_votes)

    else:
        # Connect to db
        with db_connect() as db:
            cur = db.cursor()

            # Extract vote totals from db
            sql = ''' SELECT current_votes FROM nominees '''
            cur.execute(sql)
            current_votes ['Mountain Biking'] = cur.fetchall()[0][0]
            cur.execute(sql)
            current_votes['Road Biking'] = cur.fetchall()[1][0]
            cur.execute(sql)
            current_votes['Leisure Biking'] = cur.fetchall()[2][0]

        db.close()

        return render_template('awards.html', vote_submitted=False, current_votes=current_votes, test='test')


@app.route('/keynote')
def keynote():
    return render_template('keynote.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        # Connect to db
        with db_connect() as db:
            cur = db.cursor()

            # Match username
            sql = '''SELECT lastname, password FROM users '''
            cur.execute(sql)

            # Assume that lastname is username
            for entry in cur.fetchall():
                if ((entry[0] == request.values.get('username')) and (entry[1] == request.values.get('password'))):
                    session['logged_in'] = True
                    return render_template("admin.html")

        db.close()
        return render_template('index.html')


@app.route('/meals')
def meals():
    return render_template('meals.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':

        # Connect to db
        with db_connect() as db:
            cur = db.cursor()
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql_input = (now, request.values.get('title'), request.values.get('first_name'), request.values.get('last_name'), request.values.get('address_1'), request.values.get('address_2'), request.values.get('city'), request.values.get('state'), request.values.get('zip_code'), request.values.get('telephone'), request.values.get('email'), request.values.get('company_website'), request.values.get('company_position'), request.values.get('company_name'), request.values.get('meal_option'), request.values.get('billing_first_name'), request.values.get('billing_last_name'), request.values.get('card_type'), request.values.get('card_number'), request.values.get('card_security_value'), request.values.get('expiration_year'), request.values.get('expiration_month'), request.values.get('session_1'), request.values.get('session_2'), request.values.get('session_3'))
            form_input = {'date_of_registration': now, 'title': request.values.get('title'), 'first_name': request.values.get('first_name'), 'last_name': request.values.get('last_name'), 'address_1': request.values.get('address_1'), 'address_2': request.values.get('address_2'), 'city': request.values.get('city'), 'state': request.values.get('state'), 'zip_code': request.values.get('zip_code'), 'telephone': request.values.get('telephone'), 'email': request.values.get('email'), 'company_website': request.values.get('company_website'), 'company_position': request.values.get('company_position'), 'company_name': request.values.get('company_name'), 'meal_option': request.values.get('meal_option'), 'billing_first_name': request.values.get('billing_first_name'), 'billing_last_name': request.values.get('billing_last_name'), 'card_type': request.values.get('card_type'), 'card_number': request.values.get('card_number'), 'card_security_value': request.values.get('card_security_value'), 'expiration_year': request.values.get('expiration_year'), 'expiration_month': request.values.get('expiration_month'), 'session_1': request.values.get('session_1'), 'session_2': request.values.get('session_2'), 'session_3': request.values.get('session_3')}

            # Add form contents to db as a new record
            sql = ''' INSERT INTO registrants(date_of_registration, title, firstname, lastname, address1, address2, city, state, zipcode, telephone, email, website, position, company, meals, billing_firstname, billing_lastname, card_type, card_number, card_csv, exp_year, exp_month, session1, session2, session3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            cur.execute(sql, sql_input)
            db.commit()

        db.close()

        return render_template('thankyou.html', form_input=form_input)

    else:
        return render_template('registration.html')


@app.route('/workshopschedule')
def workshopschedule():
    return render_template('workshopschedule.html')


if __name__ == '__main__':
    app.run()
    session['logged_in'] = False
