from dotenv import load_dotenv
from openai import OpenAI
from speech_synthesis import speak_text_async
import os
import base64
import io
from PIL import Image


load_dotenv()

def encode_image(image):
    buffered = io.BytesIO()
    Image.fromarray(image).save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")

def get_response(image):
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        base_url="http://10.0.100.7:8000/v1"
    )

    base64_image = encode_image(image)

    completion = client.chat.completions.create(
        # model="qwen-vl-max-0809",
        model="Qwen/Qwen2-VL-7B-Instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "你是一个机器人，输入的图片是你的眼睛看到的内容，描述一下你看到了什么？"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        top_p=0.8,
        stream=False,
    )

    response_text = completion.choices[0].message.content
    speak_text_async(response_text)
    return response_text


if __name__ == "__main__":
    get_response()
