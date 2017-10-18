#coding:utf-8

from flask import Flask
from flask import request
from flask import render_template
from model import Resource

app = Flask(__name__)

@app.route("/index",methods = ["GET","POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        href = request.form["href"]
        money = request.form["money"]

        resource = Resource()
        resource.name = name
        resource.href = href
        resource.Money = money
        resource.save()
    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    app.run()