## Setting up a Redis-backed Counter with Flask and Python

### Introduction

This tutorial will guide you through the process of setting up a Redis-backed counter using Flask and Python. The tutorial assumes that you have a basic understanding of Python, Flask, and Redis.

### Prerequisites

- An AWS account
- Basic understanding of AWS EC2
- Basic understanding of Redis
- Basic understanding of Python and Flask

### Steps

1. Launch an Ubuntu EC2 instance with ports 80, 8080, and 6379 open
2. Install Apache2, Python, and the Redis Python library
```bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get start apache2
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install redis
sudo pip3 install flask
```
3. Set up the frontend HTML and the backend server-side script
4. Launch another EC2 instance
5. Install Redis server and add this line "bind 0.0.0.0" to the redis.conf file inside /etc/redis/
```bash
sudo apt-get install redis-server
sudo systemctl start redis-server
sudo systemctl enable redis-server
```
6. Test it from the frontend hosted on port 80 of your first EC2 instance

#### Frontend script:
`File Path: /var/www/html/index.html`
```html
<!DOCTYPE html>
<html>
<head>
    <title>Redis Test</title>
</head>
<body>
    <h1>Redis Test</h1>
    <p>Current Count: <span id="count"></span></p>
    <button id="incrBtn">Increase</button>
    <button id="decrBtn">Decrease</button>
    <script>
    const countElem = document.getElementById("count");
    const incrBtn = document.getElementById("incrBtn");
    const decrBtn = document.getElementById("decrBtn");

    function updateCount() {
        fetch("http://your_ec2_instance_ip_here:8080/get")
        .then(response => response.json())
        .then(data => {
            countElem.innerText = data.count;
        });
    }

    function increaseCount() {
        fetch("http://your_ec2_instance_ip_here:8080/incr", {method: 'POST'})
        .then(() => updateCount());
    }

    function decreaseCount() {
        fetch("http://your_ec2_instance_ip_here:8080/decr", {method: 'POST'})
        .then(() => updateCount());
    }

    updateCount();

    incrBtn.addEventListener("click", increaseCount);
    decrBtn.addEventListener("click", decreaseCount);
    </script>
</body>
</html>
```

### Backend script:
`Create a python file on Path: /home/ubuntu/app.py`
```python
from flask import Flask, jsonify
import redis

app = Flask(__name__)
r = redis.Redis(host='your_redis_instance_ip_here', port=6379, db=0)

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
```
To run the python script 
```bash
python3 app.py 
```

Replace `your_ec2_instance_ip_here` with the IP address of your EC2 instance that's hosting the backend server, and `your_redis_instance_ip_here` with the IP address of your EC2 instance that has redis.

### Conclusion:
You should now have a basic understanding of how to set up a Redis-backed counter using Flask and Python. This is a simple example, but it can be expanded upon to build more complex applications.
