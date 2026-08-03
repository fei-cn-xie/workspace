from transformers import pipeline
from flask import Flask, request, jsonify
import json

# 创建一个web应用
app = Flask(__name__)
# 提前创建文本分类pipeline
classifier = pipeline("text-classification",
                     model='distilbert/distilbert-base-uncased-finetuned-sst-2-english',
                     top_k=None
                     )


def emotion_inference(text):

    # 分析文本情感
    result = classifier(text)
    return result


@app.route('/emotion')
def emotion():
    # 获取单个查询参数
    keyword = request.args.get('text', '')
    
    res = emotion_inference(keyword)
    
    return jsonify(res)

if __name__ == '__main__':
    print("服务器启动...")
    app.run(debug=True, host='0.0.0.0', port=5000)