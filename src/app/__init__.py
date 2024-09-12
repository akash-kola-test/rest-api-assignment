from flask import Flask
from .customer_routes import blue_print


app = Flask(__name__)
app.register_blueprint(blue_print, url_prefix="/v1")
