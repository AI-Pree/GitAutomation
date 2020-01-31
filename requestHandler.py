import requests
import logging
import json
import subprocess
import os
from contextlib import contextmanager

class requestHandler():
    def __init__(self, **config):
        self.__dict__.update(**config)
        self.git_api = "https://api.github.com"
        self.response = requests.get(self.git_api)
        self.logger = logging.getLogger()
        self.session = requests.Session()

    def connect(self):
        if hasattr(self,"api_token"):
            self.session.headers['Authorization'] = "token {key}".format(key = self.api_token)
        connect = self.session.post(self.git_api)
        self.logger.info("authenticated successfully") if connect == 200 else self.logger.error(self.session.get(self.git_api).status_code)
    
    @contextmanager
    def cd(self,newdir):
        prevDir = os.getcwd()
        os.chdir(os.path.expanduser(newdir))
        try:
            yield
        finally:
            os.chdir(prevDir)


    #push the whole project in the dir to the github
    def push_project_github(self,username, reponame, path):
        with self.cd(path):
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/" + username + "/" + reponame + ".git"])
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "'Initial commit'"])
            subprocess.run(["git", "push", "-u", "origin", "master"])
            self.logger.info(os.getcwd())
        
    #create a new repo for the projects
    def create_new_repo(self,*args):
        #creating a config dict to create a new repo 
        repo = {
            "name":args[0],
            "description":"New repo for "+ args[0], 
            "homepage":"https://github.com",
            "private":False,
            "has_issues":True,
            "has_projects":True,
            "has_wiki":True
        }
        url = self.git_api+"/user/repos"
        create = self.session.post(url, json = repo)
        if create.status_code == 201:
            self.logger.info("successfully created repo %s....", args[0])
        else:
            self.logger.warning("Repo already exists for %s....", args[0])
        self.push_project_github("username",args[0],args[1])
        self.logger.info(args[1]+ " checking.....")
        self.logger.info("Project pushed to the repository for {name}...".format(name = args[0]))

    
