import main

from flask import Flask, jsonify
from flask_cors import CORS


app = Flask(__name__)

@app.route("/networth", methods=["GET"])
def get_networth():
    networth = main.main()
    return jsonify({'networth': networth})

if __name__ == '__main__':
    app.run(port=11111)