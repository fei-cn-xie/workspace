from flask import Flask, jsonify

# 创建一个web应用
app = Flask(__name__)


# 映射请求
@app.route('/')
def hello_world():
    person = {
        "name": "Claude",
        "age": 25
    }
    return jsonify(person)

if __name__ == '__main__':
    print("服务器启动...")
    app.run(debug=True, host='0.0.0.0', port=5000)