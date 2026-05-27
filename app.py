from flask import Flask
import sqlite3

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

if __name__ == '__main__':
    app.run(debug=True)