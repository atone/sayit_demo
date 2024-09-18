import gradio as gr
from qwen2_vl_video import get_response

def process_video(video):
    if video is not None:
        response = get_response(video)
        return response
    else:
        return "Please capture video first"

# 创建Gradio界面
with gr.Blocks() as demo:
    gr.Markdown("## Video Demo")

    with gr.Row():
        with gr.Column():
            video_input = gr.Video(sources=["webcam"], format="mp4", label="Video Input")
            save_button = gr.Button("Send")
        output_text = gr.Textbox(label="Result")

    save_button.click(process_video, inputs=video_input, outputs=output_text)


# 运行Gradio应用
if __name__ == '__main__':
    demo.launch()
