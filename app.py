from flask import Flask, render_template, redirect, flash
from models import db, connect_db, User
from forms import UserForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
