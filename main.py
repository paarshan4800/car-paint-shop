from api import app
import os

app.config['ENV'] = os.getenv("ENV")

if __name__ == '__main__':

    if app.config['ENV'] == 'DEV':
        app.run()
    else:
        app.run()
