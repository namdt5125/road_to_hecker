from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return """
    <html>
    <body>
    hello world!
    </body>
    </html>
    """

@app.route('/submit', methods=['POST'])
def handle_post():

    data = request.form.get('data')

    print(f"""data:
================================================
{data}
================================================""")

    if data:
        return jsonify({
            "status": "chao em nha",
            "message": f"{data}"
        })
    else:
        return jsonify({
            "status": "bruh",
            "message": "hello chao em"
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)

