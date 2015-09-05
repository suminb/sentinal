from flask import Blueprint

main_module = Blueprint('main', __name__)


@main_module.route('/')
def index():
    return 'Index page'
