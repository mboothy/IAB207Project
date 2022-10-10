from flask import Blueprint
from matplotlib.pyplot import get
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("website"),
    autoescape=select_autoescape()
)

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    template = env.get_template("login.html")
    print(template.render())
