## Setting up a Redis-backed Counter with Flask and Python

### Introduction

This tutorial will guide you through the process of setting up a Redis-backed counter using Flask and Python. The tutorial assumes that you have a basic understanding of Python, Nginx, Flask, and Redis.

### Prerequisites

- An AWS account
- Basic understanding of AWS EC2
- Basic understanding of Redis
- Basic understanding of Python and Flask
- Basic understanding of Nignx 

### Steps

1. Launch an Ubuntu EC2 instance(PUBLIC) with ports 80 and 90 open
2. Launch an Ubuntu EC2 instance(PRIVATE) with 8080 and 6379 open
3. Install Apache2 and Nginx in the public ec2 instance 
```bash
sudo apt-get update
sudo apt-get install apache2
sudo apt-get start apache2
sudo apt install nginx
sudo systemctl start nginx
```
4. Set up the frontend HTML in your public instance

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
        fetch("http://your_public_instance_ip:90/get")
        .then(response => response.json())
        .then(data => {
            countElem.innerText = data.count;
        });
    }

    function increaseCount() {
        fetch("http://your_public_instance_ip:90/incr", {
            method: 'POST'
        })
        .then(() => updateCount());
    }

    function decreaseCount() {
        fetch("http://your_public_instance_ip:90/decr", {
            method: 'POST'
        })
        .then(() => updateCount());
    }

    updateCount();

    incrBtn.addEventListener("click", increaseCount);
    decrBtn.addEventListener("click", decreaseCount);
    </script>
</body>
</html>
```
5. Create a nignx proxy file with name `backend.conf` in `/etc/nginx/sites-available/`
```
server {
    listen 90;
    server_name 3.237.242.44;

    location / {
        proxy_pass http://your_private_instance_ip:8080;
    }
}
```
This nginx will forward your requests to your backend server
Replace `your_private_instance_ip` with the ip of your private instance.

Create a symbolic link to enable the site:
```
sudo ln -s /etc/nginx/sites-available/backend.conf /etc/nginx/sites-enabled/
```
Test the configuration with:
```
sudo nginx -t
```
Reload the nginx configuration:
```
sudo systemctl reload nginx
```
6. Now let's setup the backend server
   Install Python, and the Redis Python library in your private instance
```bash
sudo apt-get install python3
sudo apt-get install python3-pip
sudo pip3 install redis
sudo pip3 install flask
```

7. Install Redis server in you private instance
```bash
sudo apt-get install redis-server
```
8. Add this line `bind 0.0.0.0` to the `redis.conf` file inside `/etc/redis/`
```bash
sudo systemctl start redis-server
sudo systemctl enable redis-server
```
8. Now let's setup the backend server
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

Replace `your_public_instance_ip` with the public IP address of your EC2 instance that's hosting the frontend server, and `your_redis_instance_ip_here` with the private IP address of your EC2 instance that has redis.

### Conclusion:
You should now have a basic understanding of how to set up a Redis-backed counter using Flask and Python. This is a simple example, but it can be expanded upon to build more complex applications.
