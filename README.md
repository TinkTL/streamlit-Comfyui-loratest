# 图片生成展示应用

一个简单的 Streamlit 应用，用于展示文本输入和图片生成功能。

## 功能特点

- 文本输入界面
- 5秒延迟模拟处理过程
- 图片展示功能
- 历史记录保存
- 响应式布局设计

## 安装说明

1. 克隆项目到本地：
```bash
git clone [你的仓库地址]
cd Northbell_Comfyui_loratest
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行方式

```bash
streamlit run main.py
```

## 项目结构

```
Northbell_Comfyui_loratest/
├── main.py              # 主应用程序
├── requirements.txt     # 项目依赖
└── README.md           # 项目说明文档
```

## 使用说明

1. 在文本框中输入任意内容
2. 点击"提交并获取图片"按钮
3. 等待5秒后查看生成的图片
4. 历史记录会显示在右侧面板中

## 依赖版本

- Python >= 3.7
- streamlit >= 1.28.0
- requests >= 2.31.0
- Pillow >= 10.0.0

## 注意事项

- 确保网络连接正常，因为需要从外部获取图片
- 历史记录保存在会话中，刷新页面后会清空