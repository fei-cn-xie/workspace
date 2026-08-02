from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# 1. URL 路径参数 (Path Parameters)
@app.route('/user/<int:user_id>')
def get_user_by_id(user_id):
    return jsonify({
        "method": "GET",
        "user_id": user_id,
        "type": type(user_id).__name__,
        "message": f"获取用户 ID: {user_id}"
    })

@app.route('/user/<string:username>')
def get_user_by_name(username):
    return jsonify({
        "method": "GET",
        "username": username,
        "type": type(username).__name__,
        "message": f"获取用户名: {username}"
    })

# 支持多个路径参数
@app.route('/user/<int:user_id>/posts/<int:post_id>')
def get_user_post(user_id, post_id):
    return jsonify({
        "user_id": user_id,
        "post_id": post_id,
        "message": f"获取用户 {user_id} 的帖子 {post_id}"
    })

# 2. 查询参数 (Query Parameters)
@app.route('/search')
def search():
    # 获取单个查询参数
    keyword = request.args.get('keyword', '')
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # 获取所有查询参数
    all_args = request.args.to_dict()
    
    # 获取列表类型的查询参数 (如: ?tags=python&tags=flask)
    tags = request.args.getlist('tags')
    
    return jsonify({
        "keyword": keyword,
        "page": page,
        "limit": limit,
        "tags": tags,
        "all_args": all_args,
        "message": "查询参数演示"
    })

# 3. 表单数据 (Form Data)
@app.route('/form', methods=['POST'])
def handle_form():
    # 获取表单数据
    name = request.form.get('name')
    email = request.form.get('email')
    age = request.form.get('age', type=int)
    
    # 获取所有表单数据
    all_form_data = request.form.to_dict()
    
    # 获取列表类型的表单数据
    hobbies = request.form.getlist('hobbies')
    
    return jsonify({
        "name": name,
        "email": email,
        "age": age,
        "hobbies": hobbies,
        "all_form_data": all_form_data,
        "content_type": request.content_type,
        "message": "表单数据接收成功"
    })

# 4. JSON 数据
@app.route('/json', methods=['POST'])
def handle_json():
    try:
        # 获取 JSON 数据
        json_data = request.get_json()
        
        # 检查是否有 JSON 数据
        if json_data is None:
            return jsonify({"error": "没有 JSON 数据"}), 400
        
        # 获取特定字段
        name = json_data.get('name')
        age = json_data.get('age')
        
        return jsonify({
            "received_data": json_data,
            "name": name,
            "age": age,
            "content_type": request.content_type,
            "message": "JSON 数据接收成功"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 5. 文件上传
@app.route('/upload', methods=['POST'])
def handle_file_upload():
    # 检查是否有文件
    if 'file' not in request.files:
        return jsonify({"error": "没有文件"}), 400
    
    file = request.files['file']
    
    # 检查文件是否为空
    if file.filename == '':
        return jsonify({"error": "没有选择文件"}), 400
    
    # 获取其他表单数据
    description = request.form.get('description', '')
    
    return jsonify({
        "filename": file.filename,
        "content_type": file.content_type,
        "description": description,
        "file_size": len(file.read()),
        "message": "文件上传成功"
    })

# 6. 请求头 (Headers)
@app.route('/headers')
def handle_headers():
    # 获取特定请求头
    user_agent = request.headers.get('User-Agent')
    authorization = request.headers.get('Authorization')
    content_type = request.headers.get('Content-Type')
    
    # 获取所有请求头
    all_headers = dict(request.headers)
    
    return jsonify({
        "user_agent": user_agent,
        "authorization": authorization,
        "content_type": content_type,
        "all_headers": all_headers,
        "message": "请求头获取成功"
    })

# 7. Cookie 数据
@app.route('/cookies')
def handle_cookies():
    # 获取特定 Cookie
    session_id = request.cookies.get('session_id')
    user_pref = request.cookies.get('user_preference')
    
    # 获取所有 Cookie
    all_cookies = request.cookies.to_dict()
    
    return jsonify({
        "session_id": session_id,
        "user_preference": user_pref,
        "all_cookies": all_cookies,
        "message": "Cookie 数据获取成功"
    })

# 8. 原始请求数据
@app.route('/raw', methods=['POST'])
def handle_raw_data():
    # 获取原始请求体数据
    raw_data = request.get_data()
    
    # 尝试解码为文本
    try:
        text_data = raw_data.decode('utf-8')
    except:
        text_data = "无法解码为文本"
    
    return jsonify({
        "raw_data_length": len(raw_data),
        "raw_data_preview": str(raw_data)[:100],
        "text_data": text_data,
        "content_type": request.content_type,
        "message": "原始数据接收成功"
    })

# 9. 综合示例 - 处理多种参数类型
@app.route('/comprehensive/<int:id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def comprehensive_handler(id):
    result = {
        "method": request.method,
        "path_parameter": {"id": id},
        "query_parameters": request.args.to_dict(),
        "headers": dict(request.headers),
        "cookies": request.cookies.to_dict(),
    }
    
    # 根据请求方法处理不同类型的数据
    if request.method in ['POST', 'PUT']:
        if request.is_json:
            result["json_data"] = request.get_json()
        elif request.form:
            result["form_data"] = request.form.to_dict()
            result["files"] = [f.filename for f in request.files.values()]
        else:
            result["raw_data"] = request.get_data().decode('utf-8', errors='ignore')[:100]
    
    return jsonify(result)

# 10. 请求信息总览
@app.route('/request-info', methods=['GET', 'POST', 'PUT', 'DELETE'])
def request_info():
    return jsonify({
        "method": request.method,
        "url": request.url,
        "base_url": request.base_url,
        "path": request.path,
        "query_string": request.query_string.decode(),
        "remote_addr": request.remote_addr,
        "user_agent": request.user_agent.string,
        "content_type": request.content_type,
        "content_length": request.content_length,
        "is_json": request.is_json,
        "is_secure": request.is_secure,
        "scheme": request.scheme,
        "host": request.host,
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
