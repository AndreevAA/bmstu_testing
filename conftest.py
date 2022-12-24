import sqlite3
import subprocess

import pytest
from django.db import connections

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# def run_sql(sql):
#     conn = psycopg2.connect(database='sqlite')
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     cur = conn.cursor()
#     cur.execute(sql)
#     conn.close()
#
#
# @pytest.fixture(scope='session')
# def django_db_setup():
#     print("HERE")
#     assert 1
#     # from django.conf import settings
#     #
#     # settings.DATABASES['default']['NAME'] = 'test_db'
#     #
#     # conn = psycopg2.connect(database='sqlite')
#     # conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     # cur = conn.cursor()
#     #
#     # # run_sql('DROP DATABASE IF EXISTS test_db')
#     # cur.execute('DROP DATABASE IF EXISTS test_db')
#     #
#     # # run_sql('CREATE DATABASE test_db TEMPLATE database')
#     # cur.execute('CREATE DATABASE test_db')
#
#     subprocess.call(['./secret_init'])
#
#     # conn = sqlite3.connect("test_db.sqlite")
#     # cursor = conn.cursor()
#     # cursor.execute(str(open("construct.sql").read()))
#     #
#     # run_sql("insert into api_keys values ('valid_key');")
#
#     # yield
#     #
#     # for connection in connections.all():
#     #     connection.close()
#
#     # cur.execute('DROP DATABASE test_db')
#
#     # conn.close()

@pytest.fixture # 1
def session():
    connection = sqlite3.connect('test_db.sqlite') # 2
    db_session = connection.cursor()
    db_session.execute('''drop table if exists wardrobe_user;
drop table if exists invites;
drop table if exists wardrobe_look;
drop table if exists look_clothes;
drop table if exists look;
drop table if exists clothes;
drop table if exists wardrobe;
drop table if exists user;
drop table if exists image;
drop table if exists api_keys;

PRAGMA foreign_keys = ON;

CREATE TABLE wardrobe (
    wardrobe_id INTEGER PRIMARY KEY,
    wardrobe_description varchar(500),
    wardrobe_name varchar(100) NOT NULL,
    wardrobe_image_id INT,
    wardrobe_owner VARCHAR(100) NOT NULL,
    FOREIGN KEY (wardrobe_owner) REFERENCES user(user_login)
);

CREATE TABLE image (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    data BLOB
);

CREATE TABLE user (
    user_login VARCHAR(100) PRIMARY KEY NOT NULL,
    user_name VARCHAR(100),
    password VARCHAR(100),
    image_id INTEGER,
    FOREIGN KEY (image_id) REFERENCES image(image_id)
);

CREATE TABLE look (
    look_id INTEGER PRIMARY KEY,
    look_image_id INTEGER,
    look_name varchar(100),
    FOREIGN KEY (look_image_id) REFERENCES image(image_id)
);

CREATE TABLE clothes (
    clothes_id INTEGER PRIMARY KEY NOT NULL,
    clothes_name varchar(100),
    type varchar(100),
    image_id INTEGER,
    owner_login TEXT NOT NULL,
    FOREIGN KEY (image_id) REFERENCES image(image_id),
    FOREIGN KEY (owner_login) REFERENCES user(user_login)
);

create table wardrobe_user (
    wardrobe_id INTEGER,
    user_login VARCHAR(100),
    FOREIGN KEY (wardrobe_id) REFERENCES wardrobe(wardrobe_id),
    FOREIGN KEY (user_login) REFERENCES user(user_login)
);

create table look_clothes (
    look_id INTEGER,
    clothes_id INTEGER,
    FOREIGN KEY (clothes_id) REFERENCES clothes(clothes_id),
    FOREIGN KEY (look_id) REFERENCES look(look_id)
);

create table wardrobe_look (
    wardrobe_id INTEGER,
    look_id INTEGER,
    FOREIGN KEY (wardrobe_id) REFERENCES wardrobe(wardrobe_id),
    FOREIGN KEY (look_id) REFERENCES look(look_id)
);

CREATE TABLE api_keys (
    api_key TEXT
);

create table invites (
    invite_id INTEGER PRIMARY KEY,
    login_that_invites VARCHAR(100) NOT NULL,
    login_whom_invites VARCHAR(100) NOT NULL,
    wardrobe_id INTEGER NOT NULL,
    FOREIGN KEY (login_that_invites) REFERENCES user(user_login),
    FOREIGN KEY (login_whom_invites) REFERENCES user(user_login),
    FOREIGN KEY (wardrobe_id) REFERENCES wardrobe(wardrobe_id),
    UNIQUE(login_that_invites, login_whom_invites, wardrobe_id)
);

''') # 3
    db_session.execute("insert into api_keys values ('e602f929e7a31b2c7ec1f5c7a9ddd927');") # 4
    connection.commit()
    yield db_session # 5
    connection.close()
