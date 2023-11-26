from flask import (
    Blueprint, flash, current_app, g, redirect, render_template, request, url_for
)

bp = Blueprint('main', __name__)