from flask import Flask, jsonify, request
app = Flask(__name__)

count = {}

@app.route('/', methods=['GET'])
def get_tasks():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        ip = str(request.environ['REMOTE_ADDR'])
        if ip in count:
            count[str(ip)] += 1
        else:
            count[str(ip)] = 1
        return jsonify({'User Address': request.environ['REMOTE_ADDR'], 'Hits': count[str(ip)]}), 200
    else:
        return jsonify({'User Address': request.environ['HTTP_X_FORWARDED_FOR']}), 200

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8000)