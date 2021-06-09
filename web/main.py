from threading import Thread
from flask import Flask
from flask import render_template


app = Flask(__name__)
    
@app.route("/")
def home():
    return render_template("index.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

app.register_error_handler(404, not_found)

@app.route("/commands")
def commands():
    return render_template("commmands.html")

def flask_thread(func):
    thread = Thread(target=func)
    thread.start()

def run():
    app.run(port="8000")
    
