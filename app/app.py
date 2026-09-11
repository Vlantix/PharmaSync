from flask import Flask, jsonify


app = Flask(__name__)

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "status": "Running...",
        "message": "PharmaSync is healthy"
    }), 200

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True)