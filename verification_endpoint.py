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
    
    #First check which platform
    payload = content.get('payload')
    print(payload.keys())
    platform = payload.get('platform')
    print("The platform is {}.\n".format(platform))
    signature = content.get('sig')
    print("The signature is {}.\n".format(signature))
    message = payload.get('message')
    print("The message send in payload is {}.\n".format(message.encode('utf-8')))
    pk = payload.get('pk')
    print("The public key is {}.\n".format(pk))
    
    #When the platform is algorand
    if (platform == 'Algorand'):
        print("Yo!\n")
        result = algosdk.util.verify_bytes(message.encode('utf-8'),signature, pk)
        print("The message and signature verification is {}.\n".format(result))
    else:
        eth_encoded_msg = eth_account.messages.encode_defunct(text=message)
        recovered_pk = eth_account.Account.recover_message(eth_encoded_msg, signature = signature)
        print("The pk recovered is {}.\n".format(recovered_pk))
        result = (recovered_pk == pk)
        print("The verification result is:", result)

    #Check if signature is valid
    #Should only be true if signature validates
    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
