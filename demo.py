import gradio as gr
from qwen2_vl import get_response

def process_image(image):
    response_text = get_response(image)
    return image, response_text

demo = gr.Interface(
    fn=process_image,
    inputs=gr.Image(sources="webcam", streaming=True),
    outputs=[gr.Image(), gr.Textbox()],
    live=False
)

demo.launch()
