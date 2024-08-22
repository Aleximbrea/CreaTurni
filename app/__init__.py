from flask import Flask
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = '81fc9ff814cea0c7964daa4142a351cf3321341ac5bf613d'
conn = psycopg2.connect(host='localhost', database="postgres", user="postgres", password="admin", port=5432)
cur = conn.cursor()

from app import routes