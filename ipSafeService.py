from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/ipSafety', methods=['POST'])
def ip_safe():
    # Extract user consent from the request
    consent = request.json.get('approved')  # Expecting JSON payload
    if consent == 'yes':
        return jsonify({"consent": "yes"})
    else:
        # If consent is not given, respond accordingly
        return jsonify({
            "success": False,
            "error": "User declined to provide IP consent."
        }), 403

if __name__ == '__main__':
    # Run the microservice on port 5003
    app.run(host='0.0.0.0', port=5003, debug=True)
