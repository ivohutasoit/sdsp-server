from flask import Blueprint

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/', methods=['GET'])
def userListing():
    return 'User listing'

@user_controller.route('/activation', methods=['GET'])
def activate():
    return 'User activation'

@user_controller.route('/1', methods=['GET'])
def userDetail():
    return 'User detail'