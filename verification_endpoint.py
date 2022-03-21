from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True

@app.route('/verify', methods=['GET','POST'])
def verify():
    content = request.get_json(silent=True)
    payload = content.get('payload')
    platform = payload.get('platform')
    signature = content.get('sig')
    message = json.dumps(payload)
    pk = payload.get('pk')
    result = False
    
    #When the platform is algorand
    if platform == 'Algorand':
        result = algosdk.util.verify_bytes(message.encode('utf-8'),signature, pk)
    else:
        eth_encoded_msg = eth_account.messages.encode_defunct(text=message)
        recovered_pk = eth_account.Account.recover_message(eth_encoded_msg, signature = signature)
        result = (recovered_pk == pk)
         

    #Check if signature is valid
    #Should only be true if signature validates
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
