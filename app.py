from flask import Flask, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='10.12.2.108', port=6379, db=0)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/incr', methods=['POST'])
def incr():
    r.incr('counter')
    return '', 204, {'Access-Control-Allow-Origin': '*'}

@app.route('/decr', methods=['POST'])
def decr():
    r.decr('counter')
    return '', 204, {'Access-Control-Allow-Origin': '*'}

@app.route('/get', methods=['GET'])
def get():
    count = int(r.get('counter') or 0)
    return jsonify(count=count), 200, {'Access-Control-Allow-Origin': '*'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
