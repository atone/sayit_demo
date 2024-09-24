import cv2
from collections import deque
import os
import tempfile
from qwen2_vl_video import get_response
from datetime import datetime

# 设置原始视频保存的目录
SAVE_DIR = "/home/orin/ynt/saved_videos"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 设置视频的宽度和高度
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 获取视频的帧率和尺寸
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"fps: {fps}, width: {width}, height: {height}")

# 创建一个双端队列来存储最近5秒的帧
frame_buffer = deque(maxlen=5 * fps)

# 定义保存视频的函数
def save_video():
    # 创建一个临时文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    output_file = temp_file.name
    temp_file.close()

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # 将保存视频文件的fps修改为1
    out = cv2.VideoWriter(output_file, fourcc, 1, (width, height))

    # 从缓冲区中每隔fps帧选择一帧
    frames_to_save = list(frame_buffer)[::fps]

    for frame in frames_to_save:
        out.write(frame)

    out.release()
    return output_file

# 定义保存原始视频的函数
def save_raw_video():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_video_file = os.path.join(SAVE_DIR, f"raw_video_{timestamp}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(raw_video_file, fourcc, fps, (width, height))
    return out

try:
    out_raw = save_raw_video()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 将当前帧添加到缓冲区
        frame_buffer.append(frame)

        # 写入原始视频
        out_raw.write(frame)

        # 显示当前帧（可选）
        cv2.imshow('Camera', frame)

        # 检查键盘输入
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            saved_mp4_path = save_video()
            text = get_response(saved_mp4_path)
            print(text)
finally:
    cap.release()
    out_raw.release()
    cv2.destroyAllWindows()
