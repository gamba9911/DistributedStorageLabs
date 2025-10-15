from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello World!'


app.run(host="localhost", port=9000)
# # needs to run in terminal: python rest-server-task-6.py
# # and call: curl 'http://localhost:9000/' -v
