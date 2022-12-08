from threading import Thread
import sys

from web_framework.server_side.manage import run_server

import subprocess
import os

def run_client_side():
    subprocess.Popen(["start", "cmd", "/k", "npm", "start"], cwd="web_framework/client_side", shell=True)
    
def run_npm_install():
    subprocess.call(["npm", "install"], cwd="web_framework/client_side", shell=True)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == '-h':
        print ("Add -n if there is a problem with the node modules or npm.\n")
        return
        
    if len(sys.argv) > 1 and sys.argv[1] == '-n':
        run_npm_install()
        
    if os.environ.get('RUN_MAIN', None) != 'true':
        run_client_side()

    run_server()

if __name__ == "__main__":
    main()
