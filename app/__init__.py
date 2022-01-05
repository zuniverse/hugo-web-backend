from flask import Flask

# from instance.config import LOCATION_OF_STATIC_FILE

app = Flask(__name__, 
            # static_folder=os.path.abspath(LOCATION_OF_STATIC_FILE),
            instance_relative_config=True)

app.config.from_object('config')  # main config
app.config.from_pyfile('config.py')  # instance config
