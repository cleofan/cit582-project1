from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False

@app.route('/verify', methods=['GET','POST'])
def verify():
    print("Hello?")
    content = request.get_json(silent=True)
    payload = content.get('payload')
    platform = payload.get('platform')
    print("The platform is {}.\n".format(platform))

    #Check if signature is valid
    result = True #Should only be true if signature validates
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
