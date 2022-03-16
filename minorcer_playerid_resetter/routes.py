from flask import render_template, url_for, flash, redirect, request
from minorcer_playerid_resetter import *
from minorcer_playerid_resetter.models import *
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import pytz
from sqlalchemy import desc


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        all_audit_objs = AuditLog.query.all()
        tz = pytz.timezone('Asia/Singapore')
        curr_date = str(datetime.now(tz).date()).split("-")[1]
        # curr_date = str(datetime.now()).split("-")[1]

        for each in all_audit_objs:
            if ((int(curr_date) - 8) % 12) < int(str(each.datetime.date()).split("-")[1]):
                db.session.delete(each)
                db.session.commit()
        print("home page ..")
        region = ""
        message = ""
        appid = ""
        openid = ""
        success = ""
        keyvalid = False
        if request.args.get('status') == 'success':
            success = flash('PlayerID ' + request.args.get('deletedopenid') + ' Deleted', "success")
        if request.method == 'POST':
            region = request.form['region']
            if request.form['region'] == 'Select Region':
                redisdb = connectRedis_MOS()
            elif request.form['region'] == 'EU':
                redisdb = connectRedis_EU()
                appid = str('1135')
            elif request.form['region'] == 'JP':
                redisdb = connectRedis_JP()
                appid = str('1188')
            elif request.form['region'] == 'ASIA':
                redisdb = connectRedis_ASIA()
                appid = str('1187')
            elif request.form['region'] == 'ME':
                redisdb = connectRedis_ME()
                appid = str('1420')
            elif request.form['region'] == 'MOS':
                redisdb = connectRedis_MOS()
                appid = str('1258')

            openid = str(request.form['openid'].strip())
            isExists = redisdb.exists('minorcer::' + appid + '::' + openid)

            if openid == '':
                message = 'Please enter playerID'
            elif region == 'Select Region':
                message = 'Please select region'
            elif isExists == 0:
                message = 'PlayerID not found'
            elif isExists == 1:
                keyvalid = True

        return render_template('home.html', message=message, region=region, appid=appid, openid=openid,
                               keyvalid=keyvalid, success=success)

    return render_template("signin-register.html")


@app.route('/deleteopenid/<region>/<appid>/<openid>', methods=['GET', 'POST'])
def deleteopenid(region, appid, openid, message_region=None):
    if region == 'Select Region':
        message_region == 'Please select region'
    elif region == 'EU':
        redisdb = connectRedis_EU()
    elif region == 'JP':
        redisdb = connectRedis_JP()
    elif region == 'ASIA':
        redisdb = connectRedis_ASIA()
    elif region == 'ME':
        redisdb = connectRedis_ME()
    elif region == 'MOS':
        redisdb = connectRedis_MOS()

    redisdb.delete('minorcer::' + appid + '::' + openid)
    print("Adding audit object.")
    all_audit_objs = AuditLog.query.all()

    tz = pytz.timezone('Asia/Singapore')
    datetimedeleted = datetime.now(tz)

    audit_object = AuditLog(userid=current_user.id, playerid=openid, region=region, datetime=datetimedeleted)
    db.session.add(audit_object)
    db.session.commit()
    return redirect(url_for('index', status='success', deletedopenid=openid))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form['password']
        user = User.query.filter_by(username=username.strip()).first()
        if user:
            if str(password) == str(user.password):
                # creates a login session for this particular user
                if user.role == "Admin":
                    login_user(user)
                    return redirect(url_for('admin'))
                else:
                    if user.approval_status == "True":
                        login_user(user)
                        return redirect(url_for('index'))
                    else:
                        flash("Unable to login, access not approved", "danger")

            else:
                print("Incorrect password")
                flash("Incorrect username or password", "danger")

            return redirect(url_for('index'))
        else:
            flash("User does not exist", "danger")
            return redirect(url_for('index'))


@app.route('/register_user', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        user = User.query.filter_by(email=email).first()
        user2 = User.query.filter_by(username=username).first()
        if user:
            flash("User already exists, please try logging in", "error")
            return redirect(url_for('index'))
        elif user2:
            flash("User already exists, please try logging in", "error")
            return redirect(url_for('index'))
        else:
            user = User(username=username.strip(), email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered', 'success')
            return redirect(url_for('user_auth'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user_auth'))


@app.route("/")
def user_auth():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('signin-register.html')


@app.route("/admin")
def admin():
    user_names = {}
    users = User.query.all()
    all_audit_objs = AuditLog.query.order_by(desc(AuditLog.datetime)).all()
    for each in users:
        user_names[each.id] = each.username

    print(user_names)

    return render_template('admin.html', audit=all_audit_objs, users=users, user_names=user_names)


@app.route("/enableStatus/<userid>", methods=['GET', 'POST'])
def enable_status(userid):
    user_object = User.query.get(userid)
    user_object.approval_status = "True"
    db.session.commit()
    return redirect(url_for('admin'))


@app.route("/disableStatus/<userid>", methods=['GET', 'POST'])
def disable_status(userid):
    user_object = User.query.get(userid)
    user_object.approval_status = "False"
    db.session.commit()
    return redirect(url_for('admin'))


"""
@app.route('/deleteopenid/<region>/<appid>/<openid>',methods=['GET','POST'])
def deleteopenid(region,appid,openid):

    if region == 'EU':
        redisdb = connectRedis_EU() 
    elif region == 'JP':
        redisdb = connectRedis_JP() 
    elif region == 'ASIA':
        redisdb = connectRedis_ASIA() 
    elif region == 'ME':
        redisdb = connectRedis_ME() 
    elif region == 'MOS':
        redisdb = connectRedis_MOS() 
 
    redisdb.delete('minorcer::' + appid + '::' + openid)
    return redirect(url_for('index', status = 'success', deletedopenid = openid))
    """
