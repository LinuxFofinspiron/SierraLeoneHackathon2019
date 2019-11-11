
import requests

name = "Fofi"
birth_year = 1997

people = [{"name": "Fofi","birth":"1997"},{"name": "Augie","birth":"1998"},{"name": "Moses","birth":"1998"},{"name": "Mink","birth":"1997"}]


for person in people:
    name = person['name']
    birth_year = person['birth']


    url_ = "http://localhost:5000/greetings/" + name + "/" + str(birth_year)
    response = requests.get(url_)

    data = response.text

    print(data)
