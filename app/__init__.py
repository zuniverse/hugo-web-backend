'''
Inits the app and loads config files.

instance_relative_config=True tells the app that configuration files are 
relative to the instance folder. The instance folder is located outside the 
flaskr package and can hold local data that shouldn't be committed to version 
control, such as configuration secrets and the database file.
'''

from flask import Flask

# from instance.config import LOCATION_OF_STATIC_FILE

app = Flask(__name__, 
            # static_folder=os.path.abspath(LOCATION_OF_STATIC_FILE),
            instance_relative_config=True  # set this to have app.config.from_ object & pyfile below
            ) 

app.config.from_object('config')  # main config in bundle: ../../config.py
app.config.from_pyfile('config.py')  # instance config (local): ../../instance/config.py
