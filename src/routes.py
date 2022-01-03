from flask import Flask
from flask import render_template

app = Flask(__name__)

""" index """
@app.route("/", methods = ["GET"] )
def index() -> None :
    message = "Hello, World"
    return render_template('page/index.html', message=message)

""" product """
@app.route("/product/<product_name>", methods = ["GET"] )
def product(product_name) -> None :

    return render_template('page/product.html', message = product_name)

""" order """
@app.route("/order/<product_name>", methods = ["GET", "POST"] )
def order(product_name) -> None :

    return render_template('page/product.html', message = product_name)

""" purchace """
@app.route("/purchace/<token>", methods = ["GET"] )
def purchace(token) -> None :

    return render_template('page/product.html', message = token)

""" order check """
@app.route("/ordercheck", methods = ["GET"] )
def ordercheck(token) -> None :

    return render_template('page/product.html', message = token)

"""

 template <- route <- controller <- model <- api

"""

