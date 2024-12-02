from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

@app.route('/get_image', methods=['GET'])
def get_image():
    description = request.args.get('description', '').lower()

    keyword_mapping = {
        "clear": "clear.png",
        "sun": "clear.png",
        "rain": "rain.png",
        "storm": "rain.png",
        "snow": "snow.png",
        "blizzard": "snow.png",
        "mist": "fog.png",
        "fog": "fog.png",
        "cloud": "cloud.png"
    }

    image_filename = "default.png"
    for keyword, filename in keyword_mapping.items():
        if keyword in description:
            image_filename = filename
            break

    image_url = url_for('static', filename=f"images/{image_filename}", _external=True)
    return jsonify({"image_url": image_url})

if __name__ == "__main__":
    app.run(port=5001, debug=True)