from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    # This renders the simple home page we just created
    return render_template('index.html', title='Home')