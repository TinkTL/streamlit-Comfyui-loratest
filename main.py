import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
import json
import uuid
import re
import threading
import time
from datetime import datetime
from module.free_creativity import Free_Creativity


# 配置常量
HISTORY_IMG_DIR = "history_img"
HISTORY_FILE = os.path.join(HISTORY_IMG_DIR, "history.json")


def ensure_dir():
    """确保目录存在"""
    os.makedirs(HISTORY_IMG_DIR, exist_ok=True)


def run_with_progress(text_input, result_container):
    """后台运行Free_Creativity函数"""
    try:
        result_container['result'] = Free_Creativity(text_input)
    except Exception as e:
        result_container['error'] = str(e)
    finally:
        result_container['done'] = True


def save_and_show_image(url, text=None):
    """保存并显示图片"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))

        # 保存图片
        filename = f"{uuid.uuid4()}.png"
        image.save(os.path.join(HISTORY_IMG_DIR, filename), "PNG")

        # 保存记录
        if not isinstance(st.session_state.history, list):
            st.session_state.history = []

        st.session_state.history.append({
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'text': text,
            'image_path': filename,
            'original_url': url
        })

        # 保存历史记录
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.history, f, ensure_ascii=False, indent=2)

        # 显示图片
        st.image(image, caption=text, width='stretch')
        return True
    except Exception as e:
        st.error(f"图片处理失败: {e}")
        return False


def show_history():
    """显示历史记录"""
    st.markdown("### 历史记录")
    if st.button("清空历史", type="secondary", key="clear_history"):
        st.session_state.history = []
        for file in os.listdir(HISTORY_IMG_DIR):
            if file != '.gitkeep':
                os.remove(os.path.join(HISTORY_IMG_DIR, file))
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        st.rerun()

    if st.session_state.history:
        for record in reversed(st.session_state.history):
            try:
                img_path = os.path.join(HISTORY_IMG_DIR, record['image_path'])
                if os.path.exists(img_path):
                    with st.expander(f"生成时间: {record['timestamp']}"):
                        st.image(
                            Image.open(img_path),
                            caption=record['text'],
                            width='stretch'
                        )
            except Exception as e:
                st.error(f"加载历史图片失败: {e}")
    else:
        st.info("暂无历史记录")


def handle_input(text_input):
    """处理用户输入"""
    if not text_input.strip():
        st.warning("请输入一些文本内容")
        return

    st.write(f"您输入的文本是: {text_input}")

    # 显示状态和进度条
    status = st.empty()
    status.warning('正在处理中，请稍等...')
    progress_bar = st.progress(0)

    # 启动后台处理
    result_container = {'result': None, 'error': None, 'done': False}
    threading.Thread(
        target=run_with_progress,
        args=(text_input, result_container)
    ).start()

    # 更新进度条
    progress = 0
    while not result_container['done'] and progress < 100:
        progress += 1
        progress_bar.progress(progress)
        time.sleep(0.22)
    progress_bar.progress(100)
    status.empty()

    # 处理结果
    if result_container['error']:
        st.error(f"处理失败: {result_container['error']}")
        return

    # 提取并处理URL
    urls = re.findall(r'https?://[^\s\'"]+', result_container['result']) \
           if isinstance(result_container['result'], str) else \
           result_container['result'] if isinstance(result_container['result'], list) else []

    if urls:
        st.success("图片生成成功！")
        for url in urls:
            save_and_show_image(url, text_input)
    else:
        st.error("未能获取有效的图片URL")


def main():
    """主函数"""
    ensure_dir()

    # 初始化session state
    if 'history' not in st.session_state:
        st.session_state.history = []
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    st.session_state.history = json.load(f)
            except:
                pass

    st.title("自由创意设计")

    # 创建左右两列布局
    left_col, right_col = st.columns([2, 1])

    with left_col:
        text_input = st.text_area(
            label="在这里输入你想要的创意：",
            placeholder="例如：一个简约少女系的爽肤水...",
            height=100
        )

        if st.button("开始生成"):
            handle_input(text_input)

        st.markdown("---")
        st.markdown("### 使用说明")
        st.markdown("1. 在文本框中输入任意内容")
        st.markdown("2. 点击'开始生成'按钮")
        st.markdown("3. 系统将返回生成的图片")
        st.markdown("4. 历史记录将显示在右侧面板中")
        st.markdown("5. 所有历史图片都保存在history_img文件夹中")
        st.markdown("6. 可以使用'清空历史'按钮删除所有历史记录")

    with right_col:
        show_history()


if __name__ == "__main__":
    main()