from flask import Flask
from github import Github
from settings import USERNAME, PASSWORD
import pymongo
import requests
import json

'''
mongoimport -h localhost --port 27017 -d git -c users --drop --jsonArray --stopOnError --file users.json
'''
g = Github(USERNAME, PASSWORD)
user_list_count = 17.0
expected_list_count = 14.0
expected_branches = 3.0

client = pymongo.MongoClient('localhost', 27017)
db = client.git
users = db.users

def get_course_repo():
    return g.get_repo('manufacturedba/git-course')
    
repo = get_course_repo()

def fetch_users():
    c = users.find()
    for user in c:
       u = g.get_user(user['username'])
       users.update({"username":user['username']}, {"$set":{"verified":True}})

def save_forks():
    forks_url = repo.forks_url
    forks = requests.get(forks_url).json()
    for fork in forks:
        users.update({"username":fork['owner']['login']}, {'$set':{'fork':fork['html_url']}}) 
                
''' TASK TWO '''    
def check_fork_count():
    expected_count = repo.forks_count / expected_list_count
    user_count = repo.forks_count / user_list_count
    return {"expected":expected_count * 100.0, "real":user_count * 100.0}
    
''' TASK THREE '''
def save_branch_count():
    c = users.find()
    for user in c:
        branches = request.get(user['html_url']+'/branches').json()
        users.update({"username":fork['owner']['login']}, {'$set':{'branches':len(branches)}})
        
def get_branch_count():
    c = users.find()
    count = 0
    user_count = 0
    for user in c:
        branch = user['branches']
        count = count + branch
        user_count = user_count + 1
    all_users = user_count * expected_branches
    return 100.0 * (count / all_users)
