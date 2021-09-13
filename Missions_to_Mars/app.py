# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create Flask
# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find records from mongo
    planet_data = mongo.db.collection.find_one()

    # Return template + data
    return render_template("index.html", mars=planet_data)



# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run data scrape function
    mars_data = scrape_mars.scrape_mars_info()

    # Update mongo db
    mongo.db.collection.update({}, mars_data, upsert=True)

    # Return to home page with new data loaded
    return redirect("/")



if __name__ == "__main__":
    app.run(debug=True)