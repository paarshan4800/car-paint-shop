from api import app
import os

app.config['ENV'] = os.getenv("ENV")

if __name__ == '__main__':

    if app.config['ENV'] == 'DEV':
        app.run(debug=True)
    else:
        app.run(debug=True)

    # app.run(debug=True, ssl_context="adhoc")
