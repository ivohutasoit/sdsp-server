import sqlite3
from flask import Blueprint, request, abort, jsonify
from werkzeug.security import check_password_hash, generate_password_hash

DATABASE = 'D:\\Personal\\Workspace\\Python\\MicroServices\\diboof\\diboof.db'

auth_controller = Blueprint('auth_controller', __name__)

@auth_controller.route('/signup', methods=['POST'])
def signup():
    username = None
    password = None
    if request.form:
        if not 'username' in request.form or not 'password' in request.form:
            abort(400)

        username = request.form['username']
        password = request.form['password']
    elif request.json:
        if not 'username' in request.json or not 'password' in request.json:
            abort(400)

        username = request.json['username']
        password = request.json['password']
    else: abort(400)

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
        return jsonify({ 'status': 'OK', 'message': 'User registration is completed' })
    else:
        return jsonify({ 'status': 'ERROR', 'message': error })


@auth_controller.route('/signin', methods=['POST'])
def signin():
    userid = None
    password = None
    if request.form:
        if not 'userid' in request.form or not 'password' in request.form:
            abort(400)
        userid = request.form['userid']
        password = request.form['password'] 

    error = None
    user  = None
    if not userid:
        error = 'Username is required'
    elif not password:
        error = 'Password is required'
    else:
        con = sqlite3.connect(DATABASE)
        cur = con.cursor()
        cur.execute('SELECT username, password, administrator FROM users WHERE username = ?', (userid,))
        user = cur.fetchone()

        if user is None:
            cur.execute('SELECT username, password, administrator FROM users WHERE email = ?', (userid,))
            user = cur.fetchone()
    
        if user is None:
            error = 'Invalid user or password'
        elif not check_password_hash(user[1], password):
            error = 'Invalid user or password'

    if error is None:
        if user[2] == 1:
            return jsonify({ 'status': 'OK', 'message': 'Authentication successful as administrator' })
        else:
            return jsonify({ 'status': 'OK', 'message': 'Authentication successful' })
    else:
        return jsonify({ 'status': 'ERROR', 'message': error })

@auth_controller.route('/signout', methods=['POST'])
def signout():
    return jsonify({ 'status': 'OK', 'message': 'Sign out successful' })