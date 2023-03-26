from flask import Flask, request
from robot import Robot

app = Flask(__name__)
robot = Robot(58)

@app.route('/rotate', methods=['GET'])
def rotate():
    request_data = request.get_json()
    robot.rotate(request_data.magnitude)   
    return 'OK'

@app.route('/traverse', methods=['GET'])
def traverse():
    request_data = request.get_json()
    robot.traverse(request_data.magnitude)   
    return 'OK'

@app.route('/stop', methods=['GET'])
def stop():
    request_data = request.get_json()
    robot.stop()
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')