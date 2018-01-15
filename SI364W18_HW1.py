## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".
# Worked by myself
#Used w3Schools and Google Geocoding API reference to complete problem 4 direct links below:
#https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_form_checkbox
#https://developers.google.com/maps/documentation/geocoding/start


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"
import requests
from flask import Flask, request
app = Flask(__name__)
app.debug = True

@app.route('/class')
def hello_to_you():
    return 'Welcome to SI 364!'




## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:


# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!
@app.route('/movie/<movie>')
def movie(movie):
    url = "https://itunes.apple.com/search?term=" + movie + "&entity=movie"
    data = requests.get(url)
    string = data.json()
    return "<p>{}</p>".format(string)



## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.
@app.route('/question')
def question():
    s = """<!DOCTYPE html>
<html>
<body>
<form action="/result" method="GET">
  Enter Your Favorite Number:<br>
  <input type="text" name="number">
  <br>
  <input type="submit" value="Submit">
</form>
</body>
</html>"""
    return s


@app.route('/result', methods = ["POST", "GET"])
def result():
    number = int(request.form["number"])
    double = number * 2
    return "<h3>Double your favorite number is {}</h3>".format(double)


## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
@app.route('/problem4form',methods=["GET","POST"])
def form():
    formstring = """<br>
    <form method='POST'>
    Please enter your name: <br>
        <input action="./problem4form" type="text" name="name"> <br>
    What is your favorite city: <br>
        <input type="text" name="city"> <br>
    Do you like cats or dogs? <br>
        <input type="checkbox" name="pet" value="dogs">Dogs<br>
        <input type="checkbox" name="pet" value="cats">Cats<br>
    <input type="submit" value="Submit">
"""
    if request.method == "POST":
        city = request.form["city"]
        name = request.form["name"]
        pets = request.form.getlist("pet")
        key = "AIzaSyB1txrkdXQ4P35f22DoVMZDmaovPwnuxxk"
        results = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+ city + "&key=" + key)
        jsonResults = results.json()
        coordinates = jsonResults['results'][0]['geometry']['location']
        lat = str(coordinates["lat"])
        lng =str(coordinates["lng"])
        if len(pets) == 2:
             pet = "cats and dogs"
        elif len(pets) == 1:
            pet = pets[0]
        else:
            pet = "neither cats nor dogs"
        greeting = " <br><h3> Hello {}, you like {}, and your favorite city's coordinates are: {}, {} </h3>".format(name,pet,lat,lng)
        return formstring + greeting

    else:
        return formstring


if __name__ == '__main__':
    app.run()
