from flask import Flask

# Step 1.0
app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, port='5002')