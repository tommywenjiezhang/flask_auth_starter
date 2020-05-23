from flask import Blueprint , render_template

home_bp = Blueprint('home_bp',__name__,template_folder='templates')

@home_bp.route('/',methods=['GET'])
def index():
    return render_template("body.html")
@home_bp.route('/profile')
def profile():
    return 'Profile'