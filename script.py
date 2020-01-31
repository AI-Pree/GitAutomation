import logging 
import logging.config
import os
import json
import argparse
import subprocess
from pathlib import Path
import requestHandler


logger = logging.getLogger(__name__)
req = requestHandler.requestHandler(api_token = "api_token")

#setting up the logging system 
def setupLogging(default_path = "logging.json", default_level = logging.INFO):
    if os.path.exists(default_path):
        with open(default_path, 'rb') as file:
            config = json.load(file)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level = default_level)

def initializeGit(path):
    subprocess.run(["git", "init", path])


#creating a command line program
def run(args):
    dirPath = args.dir_path
    req.connect()
    if os.path.exists(dirPath):
        logger.info("path exists...")
        logger.info("Checking gits repos for {dir}.....".format(dir = os.path.abspath(dirPath)))
        for dirs in Path(dirPath).iterdir():
            if not any(folder.startswith('.git') for folder in os.listdir(dirs)):
                initializeGit(dirs)
                logger.info("git initialised")
                req.create_new_repo(os.path.basename(dirs),os.path.abspath(dirs))
            else:
                logger.info("git already initialised for %s", dirs)
    else:
        logger.error("Not found")

def main():
    setupLogging()
    logger.info("Testing..")
    parser = argparse.ArgumentParser("Initialize the git repo and upload it to the ")
    parser.add_argument("-p", help = "folder path to initialize git", dest = "dir_path", type = str, required=True)
    parser.set_defaults(func = run)
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
        main()
