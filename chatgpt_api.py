import requests
import json

"""
该程序用来将chatgpt的api版本嵌入到cmd中进行交互
先定义chatapi()函数，url为发送请求网址，header表头
data为请求体，作用是向url发送一个http请求，获得网页响应。
之后通过循环体获得用户输入，将json格式中的text文本打印显示在cmd窗口。
"""

with open('static.json', 'r') as f:
    key_dic = json.load(f)
with open('token', 'r') as f:
    token = f.read()

def chatapi(content):
    url = 'https://api.openai.com/v1/completions'  # ChatGPT的url
    header = {'authorization': 'Bearer %s' % token}
    # 请求头，规定了api的请求格式，Bearer后是api的token私人链接
    data = {
        'prompt': content,
        'model': key_dic["model"],
        'temperature': key_dic["temperature"],
        'max_tokens': key_dic["max_tokens"]
    }
    # 请求体，temperature为温度选择，较高的温度值会导致更随机的选择，因此生成的文本会更加多样化和不可预测。
    # 较低的温度值会导致更确定的选择，生成的文本会更加可预测和保守
    # max_tokens是必须的，否则会导致响应文本不全
    response = requests.post(url, json=data, headers=header)
    return response


if __name__ == '__main__':  # 只在该文件(主文件)时运行以下语句
    while True:
        content = input('you: ')  # 由用户输入一定的内容赋值给content
        response = chatapi(content)  # 调用函数
        if response.status_code == 200:  # 响应200为成功请求
            message = ''
            for txt in response.json()['choices']:  # 遍历响应json格式中的choices属性，将每一行响应打印至窗口
                message += txt['text']  # txt表示遍历每一个choices的变量，txt['text']
            # generated_text = [choice['text'] for choice in message]  # 另一种全部响应文本显示方法
        else:
            message = f"error: {response.status_code}"
        print('chatGpT:', message.strip('\n'))
