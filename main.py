from flask import Flask, render_template, request, redirect, url_for, session, flash
from authlib.integrations.flask_client import OAuth
from module.BaseClass import *
from helper.Constant import *
import io
from base64 import b64encode
from collections import OrderedDict
import logging as log
import os
import re
from flask_bcrypt import Bcrypt
import urllib.parse
import json
import requests

app = Flask(__name__)

app.secret_key = os.urandom(12)
oauth = OAuth(app)
bcrypt = Bcrypt(app)


@app.route('/', methods=["GET"])
@app.route('/home', methods=["GET"])
def home():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        base_object = BaseClass()
        rating_data = base_object.get_ratings_data_base([])
        customer_count = base_object.get_total_customer_count([])
        cars_count = base_object.get_total_cars_count([])
        url = 'https://api.whygo.link/trending_now'
        response = requests.get(url)
        trending_now_data = None
        if response.status_code == 200:
            trending_now_data = json.loads(response.json()['body'])
        else:
            print('Error getting trending now data')

        trending_data = None
        if trending_now_data is not None:
            vehicle_id = [int(item['itemId']) for item in trending_now_data]
            trending_data = base_object.get_trending_cars((tuple(vehicle_id),))
        del base_object
        return render_template('index.html', username=session['username'], loggedin=session['loggedin'],
                               rating_data=rating_data, customer_count=customer_count, cars_count=cars_count,
                               trending_data=trending_data)
    elif request.method == "GET":
        base_object = BaseClass()
        rating_data = base_object.get_ratings_data_base([])
        customer_count = base_object.get_total_customer_count([])
        cars_count = base_object.get_total_cars_count([])
        url = 'https://api.whygo.link/trending_now'
        response = requests.get(url)
        trending_now_data = None
        if response.status_code == 200:
            if 'body' in response.json():
                trending_now_data = json.loads(response.json()['body'])
        else:
            print('Error getting trending now data')

        trending_data = None
        if trending_now_data is not None:
            vehicle_id = [int(item['itemId']) for item in trending_now_data]
            trending_data = base_object.get_trending_cars((tuple(vehicle_id),))
        del base_object
        return render_template('index.html', rating_data=rating_data, customer_count=customer_count,
                               cars_count=cars_count,
                               trending_data=trending_data)


@app.route('/about', methods=["GET"])
def about():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        base_object = BaseClass()
        rating_data = base_object.get_ratings_data_base([])
        customer_count = base_object.get_total_customer_count([])
        cars_count = base_object.get_total_cars_count([])
        del base_object
        return render_template('about.html', username=session['username'], loggedin=session['loggedin'],
                               rating_data=rating_data, customer_count=customer_count, cars_count=cars_count)
    elif request.method == "GET":
        base_object = BaseClass()
        rating_data = base_object.get_ratings_data_base([])
        customer_count = base_object.get_total_customer_count([])
        cars_count = base_object.get_total_cars_count([])
        del base_object
        return render_template('about.html', rating_data=rating_data, customer_count=customer_count,
                               cars_count=cars_count)


@app.route('/blog', methods=["GET"])
def blog():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        return render_template('blog.html', username=session['username'], loggedin=session['loggedin'])
    elif request.method == "GET":
        return render_template('blog.html')


@app.route('/blogSingle', methods=["GET"])
def blogSingle():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        return render_template('blog-single.html', username=session['username'], loggedin=session['loggedin'])
    elif request.method == "GET":
        return render_template('blog-single.html')


@app.route('/services', methods=["GET"])
def services():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        return render_template('services.html', username=session['username'], loggedin=session['loggedin'])
    elif request.method == "GET":
        return render_template('services.html')


@app.route('/reviews', methods=["POST"])
def reviews():
    if request.method == "POST" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        comment = request.form.get("comment")
        vehicle_rate = request.form.get('vehicle_rate')
        cleanliness_rate = request.form.get('cleanliness_rate')
        comfort_rate = request.form.get('comfort_rate')
        car_id = request.form.get('car_id')
        if comment in ("", None):
            comment = None
        base_object = BaseClass()
        data_list = [car_id, None, session['id'], vehicle_rate, comment, cleanliness_rate, comfort_rate, None, None]

        vehicle_review = base_object.insert_car_reviews(data_list)
        if vehicle_review:
            vehicle_data = base_object.get_vehicle_data_id([car_id])
            related_data = base_object.get_related_vehicle_data([])
            rating_data = base_object.get_ratings_data([car_id])
            # rating_count = base_object.get_ratings_count([])
            rating_data_percentage = base_object.get_ratings_data_percentage([car_id])
            del base_object
            flash("Review is submitted.", "success")
            return render_template('car-single.html', username=session['username'], loggedin=session['loggedin'],
                                   data=vehicle_data, related_data=related_data, car_id=car_id, rating_data=rating_data,
                                   rating_data_percentage=rating_data_percentage)
    elif request.method == "POST":
        return render_template('login.html')


@app.route('/pricing', methods=["GET"])
def pricing():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        base_object = BaseClass()
        vehicle_data = base_object.get_vehicle_data([])
        del base_object
        return render_template('pricing.html', username=session['username'], loggedin=session['loggedin'],
                               data=vehicle_data)
    elif request.method == "GET":
        base_object = BaseClass()
        vehicle_data = base_object.get_vehicle_data([])
        del base_object
        return render_template('pricing.html', data=vehicle_data)


@app.route('/contact', methods=["GET"])
def contact():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:

        return render_template('contact.html', username=session['username'], loggedin=session['loggedin'])
    elif request.method == "GET":
        return render_template('contact.html')


@app.route('/car', methods=["GET"])
def car():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:

        base_object = BaseClass()
        vehicle_data = base_object.get_vehicle_data([])
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)

        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        data = vehicle_data[start_index:end_index]

        total_items = len(vehicle_data)
        total_pages = (total_items + per_page - 1) // per_page
        page_range = range(1, total_pages + 1)

        del base_object
        return render_template('car.html', username=session['username'], loggedin=session['loggedin'], data=data,
                               page_range=page_range, current_page=page)
    elif request.method == "GET":
        base_object = BaseClass()
        vehicle_data = base_object.get_vehicle_data([])
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=12, type=int)

        start_index = (page - 1) * per_page
        end_index = start_index + per_page
        data = vehicle_data[start_index:end_index]

        total_items = len(vehicle_data)
        total_pages = (total_items + per_page - 1) // per_page
        page_range = range(1, total_pages + 1)

        del base_object
        return render_template('car.html', data=data, page_range=page_range, current_page=page)


@app.route('/carSingle', methods=["GET"])
def carSingle():
    if request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        car_id = request.args.get('car_id')
        base_object = BaseClass()
        vehicle_data = base_object.get_vehicle_data_id([car_id])
        # related_data = base_object.get_related_vehicle_data([])
        rating_data = base_object.get_ratings_data([car_id])
        # rating_count = base_object.get_ratings_count([])
        rating_data_percentage = base_object.get_ratings_data_percentage([car_id])
        url = 'https://api.whygo.link/personalization_hrnn'

        data = {
            "user_id": str(session['id'])
        }
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))

        hrnn_data = None
        if response.status_code == 200:
            hrnn_data = json.loads(response.json()['body'])
        else:
            print('Error getting trending now data')

        related_data = None
        if hrnn_data is not None:
            vehicle_id = [int(item['itemId']) for item in hrnn_data]
            related_data = base_object.get_trending_cars((tuple(vehicle_id),))
        del base_object
        return render_template('car-single.html', username=session['username'], loggedin=session['loggedin'],
                               data=vehicle_data, related_data=related_data, car_id=car_id, rating_data=rating_data,
                               rating_data_percentage=rating_data_percentage)
    elif request.method == "GET":
        car_id = request.args.get('car_id')
        base_object = BaseClass()
        vehicle_data = base_object.get_vehicle_data_id([car_id])
        related_data = base_object.get_related_vehicle_data([])
        rating_data = base_object.get_ratings_data([car_id])
        rating_data_percentage = base_object.get_ratings_data_percentage([car_id])
        del base_object
        return render_template('car-single.html', data=vehicle_data, related_data=related_data, car_id=car_id,
                               rating_data=rating_data,
                               rating_data_percentage=rating_data_percentage)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        login_email = request.form.get("loginemailid")
        login_password = request.form.get("logininputPassword")
        base_object = BaseClass()
        data_list = [login_email]
        account_status = base_object.get_login_data(data_list)

        if len(account_status) == 0:
            flash("Invalid Credentails !", "danger")
            del base_object
            return render_template('login.html')

        elif len(account_status) == 1 and account_status[0]['status'] in ('approved', 'google-approved') and \
                bcrypt.check_password_hash(account_status[0]['password'], login_password):
            account_id = account_status[0]['customer_id']
            user_name = account_status[0]['first_name']
            status = account_status[0]['status']
            session['loggedin'] = True
            session['id'] = account_id
            session['username'] = user_name
            session['status'] = status

            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')

            # Use the user agent string to determine the user's device type and operating system
            if 'Mobile' in user_agent:
                device_type = 'Mobile'
            elif 'Tablet' in user_agent:
                device_type = 'Tablet'
            else:
                device_type = 'Desktop'

            if 'Windows' in user_agent:
                os = 'Windows'
            elif 'Macintosh' in user_agent:
                os = 'Macintosh'
            elif 'Linux' in user_agent:
                os = 'Linux'
            elif 'Android' in user_agent:
                os = 'Android'
            elif 'iOS' in user_agent:
                os = 'iOS'
            else:
                os = 'Unknown'

            data_list = [login_email, ip_address, None, device_type, os, 'whygo_managed']

            user_creation_status = base_object.insert_customer_login(data_list)
            del base_object
            if user_creation_status:
                return redirect(url_for('home'))

    elif request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        return redirect(url_for('home'), username=session['username'], loggedin=session['loggedin'])
    elif request.method == "GET":
        return render_template('login.html')
    else:
        pass


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == "POST":

        base_object = BaseClass()

        firstName = request.form.get("firstName")
        middleName = request.form.get("middleName")
        lastName = request.form.get("lastName")
        inputEmail = request.form.get("inputEmail")
        birthday = request.form.get("birthday")
        country_code = request.form.get('country_code')
        country_code_name = request.form.get('country_code_name')
        pattern = r"(.*?)\s+\((.*)\)"
        match = re.search(pattern, country_code_name)
        country_name = match.group(1)
        country_code_extension = match.group(2)
        typePhone = request.form.get("typePhone")
        inputPassword = bcrypt.generate_password_hash(request.form.get("inputPassword")).decode('utf-8')
        driverLicense = request.form.get("driverLicense")
        driving_license_country_code_name = request.form.get("driving_license_country_code_name")
        pattern = r"(.*?)\s+\-\s+(.*)"
        match = re.search(pattern, driving_license_country_code_name)
        state_name = match.group(1)
        state_code = match.group(2)
        drivingLicenceExpiry = request.form.get("DrivingLicenceExpiry")
        ip_address = request.remote_addr

        # check email is already taken
        data_list = [inputEmail.lower()]
        email_status = base_object.check_email_exist(data_list)
        if email_status:
            flash("Email address is already Taken !", "danger")
            del base_object
            return render_template('signup.html')

        # check user exist
        data_list = [firstName, lastName, inputEmail, birthday]
        account_status = base_object.check_user_exist(data_list)
        # check account exist
        if account_status:
            flash("User is Already Registered !", "danger")
            del base_object
            return render_template('signup.html')

        if middleName in ("", None):
            middleName = None

        # print(firstName, middleName, lastName, inputEmail, birthday, country_code,country_name, country_code_extension , typePhone
        #       ,inputPassword, driverLicense, state_name,state_code , drivingLicenceExpiry, ip_address)

        data_list = [firstName, middleName, lastName, inputEmail, birthday, ip_address, country_code, country_name,
                     country_code_extension, typePhone, inputPassword, driverLicense, state_name, state_code,
                     drivingLicenceExpiry
                     ]
        user_creation_status = base_object.insert_new_user(data_list)
        del base_object
        if user_creation_status:
            return render_template('login.html')

    elif request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        return redirect(url_for('home'), username=session['username'], loggedin=session['loggedin'])
    elif request.method == "GET":
        return render_template('signup.html')
    else:
        pass


@app.route('/forget_password', methods=['GET', 'POST'])
def forget_password():
    if request.method == "POST":
        login_email = request.form.get("forgetinputEmail")
        login_password = bcrypt.generate_password_hash(request.form.get("inputPassword")).decode('utf-8')
        # check terms and condition checkbox
        if not request.form.get('forgetpswterms'):
            flash("Please Accept the Terms and Condition !", "danger")
            return render_template('forget_password.html')

        base_object = BaseClass()

        # check email exist
        data_list = [login_email.lower()]
        email_status = base_object.check_email_exist(data_list)
        if not email_status:
            flash("Email Address does not exist !", "danger")
            del base_object
            return render_template('forget_password.html')

        # updating the database for the password reset
        data_list = [login_password, login_email]
        update_status = base_object.update_password(data_list)
        del base_object
        if update_status:
            session.clear()
            return redirect(url_for('login'))
        else:
            flash("Old and New password is Same !", "danger")
            return render_template('forget_password.html')
    elif request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        return redirect(url_for('home'), username=session['username'], loggedin=session['loggedin'])
    elif request.method == "GET":
        return render_template('forget_password.html')
    else:
        pass


@app.route('/google/')
def google():
    GOOGLE_CLIENT_ID = '667336428321-9p86qi1ft3ni297rp20gnljp5340j3ck.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = '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'

    CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url=CONF_URL,
        client_kwargs={
            'scope': 'openid email profile'
        }
    )

    # Redirect to google_auth function
    redirect_uri = url_for('google_auth', _external=True)

    return oauth.google.authorize_redirect(redirect_uri)


@app.route('/google/auth/')
def google_auth():
    token = dict(oauth.google.authorize_access_token())
    token_id = token['access_token']
    nonce = token['userinfo']['nonce']
    user = dict(oauth.google.parse_id_token(token, nonce))

    # Encode user data as JSON and as a query parameter in the URL
    encoded_user_data = urllib.parse.quote(json.dumps(user))
    redirect_url = url_for('fedrated_login', user_data=encoded_user_data)
    return redirect(redirect_url)


@app.route('/fedrated_login', methods=['GET', 'POST'])
def fedrated_login():
    print("hello1")
    if request.method == "POST":
        print("hello4")
        base_object = BaseClass()
        firstName = request.form.get("firstName")
        middleName = request.form.get("middleName")
        lastName = request.form.get("lastName")
        inputEmail = request.form.get("inputEmail")
        birthday = request.form.get("birthday")
        country_code = request.form.get('country_code')
        country_code_name = request.form.get('country_code_name')
        pattern = r"(.*?)\s+\((.*)\)"
        match = re.search(pattern, country_code_name)
        country_name = match.group(1)
        country_code_extension = match.group(2)
        typePhone = request.form.get("typePhone")
        driverLicense = request.form.get("driverLicense")
        driving_license_country_code_name = request.form.get("driving_license_country_code_name")
        pattern = r"(.*?)\s+\-\s+(.*)"
        match = re.search(pattern, driving_license_country_code_name)
        state_name = match.group(1)
        state_code = match.group(2)
        drivingLicenceExpiry = request.form.get("DrivingLicenceExpiry")
        ip_address = request.remote_addr

        if middleName in ("", None):
            middleName = None

        data_list = [firstName, middleName, lastName, inputEmail, birthday, ip_address, country_code, country_name,
                     country_code_extension, typePhone, driverLicense, state_name, state_code,
                     drivingLicenceExpiry
                     ]
        user_creation_status = base_object.insert_new_user_fedrated(data_list)

        if user_creation_status:
            # getting Ip Address
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')

            # Use the user agent string to determine the user's device type and operating system
            if 'Mobile' in user_agent:
                device_type = 'Mobile'
            elif 'Tablet' in user_agent:
                device_type = 'Tablet'
            else:
                device_type = 'Desktop'

            if 'Windows' in user_agent:
                os = 'Windows'
            elif 'Macintosh' in user_agent:
                os = 'Macintosh'
            elif 'Linux' in user_agent:
                os = 'Linux'
            elif 'Android' in user_agent:
                os = 'Android'
            elif 'iOS' in user_agent:
                os = 'iOS'
            else:
                os = 'Unknown'

            data_list = [inputEmail.lower()]
            account_status = base_object.get_login_data(data_list)
            account_id = account_status[0]['customer_id']
            user_name = account_status[0]['first_name']
            status = account_status[0]['status']
            session['loggedin'] = True
            session['id'] = account_id
            session['username'] = user_name
            session['status'] = status
            data_list = [inputEmail, ip_address, None, device_type, os, 'google-approved']
            customer_status = base_object.insert_customer_login(data_list)
            del base_object
            if customer_status:
                return redirect(url_for('home'))

    elif request.method == "GET" and 'loggedin' in session and session['status'] in ['approved', 'google-approved']:
        print("hello3")
        return redirect(url_for('home'), username=session['username'], loggedin=session['loggedin'])
    elif request.method == "GET":
        print("hello2")
        # Decode the user data from the query parameter
        encoded_user_data = request.args.get('user_data')
        user_data = json.loads(urllib.parse.unquote(encoded_user_data))
        given_name = user_data['given_name'].split(' ')
        first_name = given_name[0]
        try:
            middle_name = given_name[1]
        except:
            middle_name = ""
        user_data['first_name'] = first_name
        user_data['middle_name'] = middle_name

        base_object = BaseClass()
        # check email is already taken
        email = user_data['email'].lower()
        data_list = [email]
        email_status = base_object.get_login_data(data_list)
        if len(email_status) == 1:
            # getting Ip Address
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')

            # Use the user agent string to determine the user's device type and operating system
            if 'Mobile' in user_agent:
                device_type = 'Mobile'
            elif 'Tablet' in user_agent:
                device_type = 'Tablet'
            else:
                device_type = 'Desktop'

            if 'Windows' in user_agent:
                os = 'Windows'
            elif 'Macintosh' in user_agent:
                os = 'Macintosh'
            elif 'Linux' in user_agent:
                os = 'Linux'
            elif 'Android' in user_agent:
                os = 'Android'
            elif 'iOS' in user_agent:
                os = 'iOS'
            else:
                os = 'Unknown'

            session['loggedin'] = True
            session['id'] = email_status[0]['customer_id']
            session['username'] = email_status[0]['first_name']
            session['status'] = 'google-approved'
            data_list = [email, ip_address, None, device_type, os, 'google-approved']
            login_status = base_object.insert_customer_login(data_list)
            if login_status:
                del base_object
                return redirect(url_for('home'))
        else:
            del base_object
            return render_template('fedrated.html', data=user_data)
    else:
        pass


# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
