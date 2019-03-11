from flask import Flask
from controllers import auth_controller, user_controller

# Step 1.0
app = Flask(__name__)
app.register_blueprint(auth_controller, url_prefix='/api/v1.0/auth')
app.register_blueprint(user_controller, url_prefix='/api/v1.0/users')

if __name__ == '__main__':
    app.run(debug=True, port='5002')