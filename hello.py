import os
from flask import Flask
from github import Github

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World.'
