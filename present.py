import time
import os
import sys
import select
from multiprocessing import Process
from dotenv import load_dotenv
from speech_synthesis import speak_text

load_dotenv()

def load_script(script_file):
    with open(script_file, 'r') as f:
        return f.read().strip().split('\n')


def main():
    if len(sys.argv) < 2:
        print("usage: python present.py <script_file>")
        exit(1)

    script_file = sys.argv[1]
    if not os.path.exists(script_file):
        print(f"script file {script_file} not found")
        exit(1)

    print("按 's' 开始播放脚本，按 'q' 退出程序")
    text_list = load_script(script_file)

    idx = 0
    while True:
		# 非阻塞方式检查键盘输入
        if select.select([sys.stdin], [], [], 0.0)[0]:
            key = sys.stdin.read(1)
            if key == 'q':
                print("exit")
                break
            elif key == 's':
                if idx < len(text_list):
                    text = text_list[idx]
                    process = Process(target=speak_text, args=(text,))
                    process.start()
                    idx += 1
                else:
                    print("script end")
                    break
        time.sleep(0.1)


if __name__ == "__main__":
    main()