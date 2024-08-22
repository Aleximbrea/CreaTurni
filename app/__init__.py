from flask import Flask
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(host='localhost', database="postgres", user="postgres", password="admin", port=5432)
cur = conn.cursor()

from app import routes