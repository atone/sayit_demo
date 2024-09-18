from dotenv import load_dotenv
load_dotenv()


from http import HTTPStatus
from speech_synthesis import speak_text_async
import dashscope
import time


def get_response(video):
    messages = [
        {
            "role": "user",
            "content": [
                # 以视频文件传入
                {"video": f"file://{video}"},
                # 或以图片列表形式传入
                # {"video":[
                #     "https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg",
                #     "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
                #     ]},
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
        speak_text_async(text)
        return text
    else:
        return response.message
