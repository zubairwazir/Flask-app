from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minorcer.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


def connectRedis_EU():
    redisdb = redis.StrictRedis(
        host = "eu-flask-aov-redis-test.lvyehz.ng.0001.apn3.cache.amazonaws.com",
        port = '6379',
        charset = 'utf-8',
        decode_responses = True
        )
    return redisdb

def connectRedis_JP():
    redisdb = redis.StrictRedis(
        host = "jp-flask-aov-redis-test.lvyehz.ng.0001.apn3.cache.amazonaws.com",
        port = '6379',
        charset = 'utf-8',
        decode_responses = True
        )
    return redisdb


def connectRedis_ASIA():
    redisdb = redis.StrictRedis(
        host = "asia-flask-aov-redis-test.lvyehz.ng.0001.apn3.cache.amazonaws.com",
        port = '6379',
        charset = 'utf-8',
        decode_responses = True
        )
    return redisdb


def connectRedis_ME():
    redisdb = redis.StrictRedis(
        host = "me-flask-aov-redis-test.lvyehz.ng.0001.apn3.cache.amazonaws.com",
        port = '6379',
        charset = 'utf-8',
        decode_responses = True
        )
    return redisdb

def connectRedis_MOS():
    redisdb = redis.StrictRedis(
        host = "mos-flask-aov-redis-test.lvyehz.ng.0001.apn3.cache.amazonaws.com",
        port = '6379',
        charset = 'utf-8',
        decode_responses = True
        )
    return redisdb


from minorcer_playerid_resetter import routes