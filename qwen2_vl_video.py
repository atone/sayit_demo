import time
import dashscope
from http import HTTPStatus

def get_response(picture_list):
    messages = [
        {
            "role": "user",
            "content": [
                {"video": picture_list},
                {"text": "你是一个机器人，输入的视频是你的眼睛看到的内容，描述一下你看到了什么？"}
            ]
        }
    ]
    start = time.time()
    response = dashscope.MultiModalConversation.call(
        model='qwen-vl-max',
        messages=messages
    )
    end = time.time()
    print(f'获得response，耗时{end-start}秒')
    if response.status_code == HTTPStatus.OK:
        text = response.output.choices[0].message.content[0]['text']
        return text
    else:
        return response.message
