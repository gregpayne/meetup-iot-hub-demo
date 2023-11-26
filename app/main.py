from flask import Blueprint, render_template, request

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def main():
    return render_template('index.html')