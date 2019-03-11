import sqlite3
from flask import Blueprint, request, abort, jsonify
from werkzeug.security import generate_password_hash

DATABASE = 'D:\\Personal\\Workspace\\Python\\MicroServices\\diboof\\diboof.db'

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        if not 'username' in request.form or not 'password' in request.form:
            abort(400)

        username = request.form['username']
        password = request.form['password']

        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cur.fetchone()

        if user is not None:
            error = 'User {} is already registered.'.format(username)
        
        if error is None:
            cur.execute("INSERT INTO users (username,password) VALUES (?,?)", (username, generate_password_hash(password)))
            con.commit()
            con.close()
            return jsonify({ 'status': 'OK', 'message': 'User registration is completed'})
        else:
            return jsonify({ 'status': 'ERROR', 'message': error })