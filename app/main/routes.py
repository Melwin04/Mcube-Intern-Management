from flask import render_template
from . import mainBp

@mainBp.get("/")
def home():
    return render_template('login.html')
    

@mainBp.get('/<page>')
def loadPage(page):

    return render_template(f"{page}.html")