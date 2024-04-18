from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"An error occurred: {e}", 500