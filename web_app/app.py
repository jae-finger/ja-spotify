from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'JA-SPOTIFY FLASK APP COMING SOON'


if __name__ == '__main__':
    app.run()
