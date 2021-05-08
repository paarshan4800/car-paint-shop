from api import app
from decouple import config
import os

app.config['ENV'] = os.getenv("ENV")

if __name__ == '__main__':

    if app.config['ENV'] == 'DEV':
        app.run(debug=True)
    else:
        app.run()

    # app.run(debug=True, ssl_context="adhoc")
