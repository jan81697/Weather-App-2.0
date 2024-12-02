from flask import Flask, jsonify
import geocoder

app = Flask(__name__)

@app.route('/get_userCity', methods=['GET'])
def user_city():
    try:
        g = geocoder.ip('me')  # Get user's city using their IP
        user_city = g.city
        if user_city:
            return jsonify({"success": True, "city": user_city})
        else:
            return jsonify({"success": False, "error": "Unable to determine city."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
