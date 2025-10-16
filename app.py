from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route
def test():
    return jsonify({"message": "This is a test endpoint."})('/test')


if __name__ == '__main__':
    app.run(debug=True)