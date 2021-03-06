from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_cors import cross_origin
from core import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/post')
@cross_origin()
def post(input):
    try:
        input = request.args.get('url', verify=False)
        scrappy()

        return render_template("index.html")
      
    except:
        return redirect("/") # If block the crawl, redirect to index page

    

if __name__ == "__main__":
    app.run(port=5050, debug=True)