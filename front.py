import os
from flask import Flask, render_template
import hub
import pymongo
import json

app = Flask(__name__)
app.debug = True

import os
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


client = pymongo.MongoClient('localhost', 27017)
db = client.git
users = db.users

c = users.find()
user_obj = []
for user in c:
    user_obj.append(user)
        
@app.route('/one')
def task_one():
    return render_template('greet_users.html', users=user_obj)
    
@app.route('/one/verify')
def task_one_verify():
    forks = hub.fetch_users()
    return "Success"
    
@app.route('/two')
def task_two():
    return render_template('show_forks.html', users=user_obj, task="Checking Forks")
    
@app.route('/two/count')
def task_two_count():
    count = hub.check_fork_count()
    return render_template('show_progress.html', progress=count, task="Checking Forks")
    
@app.route('/two/verify')
def task_two_verify():
    hub.save_forks()
    return "Success"
    
@app.route('/three')
def task_three():
    count = get_branch_count()
    return render_template('show_progress.html', task="Checking Branches", progress=count)
    
@app.route('/three/verify')
def task_three_verify():
    count = hub.save_branches()
    return ""
    
if __name__ == '__main__':
    app.run()
