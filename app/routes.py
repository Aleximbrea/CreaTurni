from app import app
from flask import render_template, url_for
import psycopg2

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/employees")
def employees():
    return render_template('employees.html')

@app.route("/add_employee")
def add_employee():
    return render_template('add_employee.html')