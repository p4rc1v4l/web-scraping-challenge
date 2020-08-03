# import necessary libraries
from flask import Flask, render_template
import scrape_mars

# create instance of Flask app
app = Flask(__name__)


# create route that renders index.html template
@app.route("/")
def home():
    mars_data = scrape_mars.load_mars_data()
    return render_template("index.html", data=mars_data)


# create route that renders index.html template
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    scrape_mars.persist_mars_data(mars_data)
    return render_template("scrape_confirmation.html")


if __name__ == "__main__":
    app.run(debug=True)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
