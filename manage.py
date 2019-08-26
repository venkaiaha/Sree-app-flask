import app
import os, subprocess

from flask import redirect
from flask_socketio import SocketIO

application = app.App.create_app(flask_config_name='development')

@application.route("/")
def index():
    return redirect('/api/v1')

@application.before_first_request
def init_ext_socket():
    path = os.getcwd()
    cmd = os.path.join(path,'search_whoosh.py')
    path_env = os.environ['VIRTUAL_ENV']
    path_env = os.path.join(path_env,'bin','python')
    # [print(doc,"\n") for doc in os.environ]
    print(path_env, cmd)
    os.system(f'{path_env} {cmd}')
    # subprocess.run(path_env, cmd)
    print('hi')    

if __name__ == '__main__':
    application.run(debug=True,host='0.0.0.0',port = 5002)
    
    