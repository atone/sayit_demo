import os
import time
import tempfile
import cv2
from collections import deque
from datetime import datetime
from multiprocessing import Process
from qwen2_vl_video import get_response
from speech_synthesis import speak_text

SAVE_DIR = os.path.join(os.path.dirname(__file__), "saved_videos")

# 执行预定动作
def make_action(frame_buffer, fps, width, height, work_dir):
    temp_dir = tempfile.mkdtemp()
    frame_list = list(frame_buffer)


    # 从缓冲区中每隔fps/2帧选择一帧（每秒2帧）
    frames_to_save = frame_list[::fps//2]
    picture_list = []

    # 保存选中的帧为图片
    for i, frame in enumerate(frames_to_save):
        image_path = os.path.join(temp_dir, f'frame_{i:03d}.jpg')
        cv2.imwrite(image_path, frame)
        picture_list.append(f'file://{image_path}')

    text = get_response(picture_list)
    print(text)
    speak_text(text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    text_file = os.path.join(work_dir, f'segment_{timestamp}.txt')
    with open(text_file, 'w') as f:
        f.write(text)

    video_file = os.path.join(work_dir, f'segment_{timestamp}.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_file, fourcc, fps, (width, height))
    for frame in frame_list:
        out.write(frame)
    out.release()

# 定义保存原始视频的函数
def get_raw_video_writer(frame_buffer, fps, width, height, work_dir):
    raw_video_file = os.path.join(work_dir, 'raw_video.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(raw_video_file, fourcc, fps, (width, height))
    return out

def main():
    work_dir = os.path.join(SAVE_DIR, datetime.now().strftime("%Y%m%d_%H%M%S"))

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    # 初始化摄像头
    cap = cv2.VideoCapture(0)

    # 设置视频的宽度和高度
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # 获取视频的帧率和尺寸
    read_fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"fps: {read_fps}, width: {width}, height: {height}")

    # 在开始录制之前，先测量实际帧率
    frame_count = 0
    start_time = time.time()
    while frame_count < 60:  # 收集60帧来计算实际帧率
        ret, _ = cap.read()
        if ret:
            frame_count += 1
    actual_fps = frame_count / (time.time() - start_time)
    print(f"实际帧率: {actual_fps}")
    fps = int(actual_fps)

    # 创建一个双端队列来存储最近5秒的帧
    frame_buffer = deque(maxlen=5 * fps)

    try:
        out_raw = get_raw_video_writer(frame_buffer, fps, width, height, work_dir)
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
                # 开启一个新进程运行预定动作
                process = Process(target=make_action, args=(frame_buffer, fps, width, height, work_dir))
                process.start()
    finally:
        cap.release()
        out_raw.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()