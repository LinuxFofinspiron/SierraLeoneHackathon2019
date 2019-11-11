
from flask import Flask

app = Flask(__name__)

@app.route('/')
def Home():
    return "Hello World"



@app.route('/greetings/<name>/<year>')
def Greetings(name,year):
    return "Hello {} you are {} years old!".format(name,getAge(year))


def getAge(year):
    return 2019 - int(year)

if __name__ == "__main__":
    app.run(debug=True)