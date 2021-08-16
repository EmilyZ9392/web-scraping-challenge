from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo 
import scrape_mars

# create instance of Flask
app= Flask(__name__)

#set up mongo connection with flask_pymongo
mongo = PyMongo(app, uri= 'mongodb://localhost:27017/mars_app')

#route to render index.html template using mongo data
@app.route("/")
def home():

    #find record from mongo db
    mars_dict = mongo.db.mars_dict.find_one()
    # return data
    return render_template('index.html', mars=mars_dict)

@app.route("/scrape")
def scrape():

    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape()

    #update mongo db
    mars_dict.update({}, mars_data, upsert=True)
    return redirect ("/")

if __name__ == "__main__":
    app.run(debug=True)
