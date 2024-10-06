from flask import Blueprint

bp = Blueprint('accounts', __name__)

from app.accounts import routes
