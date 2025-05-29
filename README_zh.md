# 🧠 Lyra: 多模态 AI 助手

Lyra 是一个支持**语音和文字双模态交互**的智能助手。  
她集成了 OpenAI Whisper 语音识别、DeepSeek Chat API 对话生成和 Microsoft Edge TTS 语音合成技术，旨在提供流畅自然的对话体验。

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/Leon-Xie-2022/Lyra.git
cd Lyra
```

### 2. 创建环境

确保已安装 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)。

```bash
conda env create -f environment.yml
conda activate lyra
```

### 3. 配置 DeepSeek API 密钥

在项目根目录创建 `.env` 文件并设置：

```plaintext
DEEPSEEK_API_KEY=your_api_key_here
```

### 4. 启动应用

```bash
python web_app.py
```

访问 [http://127.0.0.1:5000](http://127.0.0.1:5000) 开始对话。

---

## 💡 核心功能

- **多模态交互**
  - 支持文字和语音输入
  - **基于上下文智能选择文字或语音输出**
  - 语音消息支持播放和文字转写

- **个性化设置**
  - 可配置的用户偏好
  - 可调节的输出模式（文字/语音）
  - 个人信息设置

- **情感智能**（实现中）
  - 情感感知的对话响应
  - 动态情绪状态显示
  - 上下文敏感的互动方式

---

## 📍 项目结构

```
lyra/
├── web_app.py              # Flask 应用入口
├── environment.yml         # Conda 环境配置
├── history.txt            # 对话历史记录
├── README.md              # 英文文档
├── README_zh.md           # 中文文档
│
├── models/                # 核心功能模块
│   ├── asr_model.py      # 语音识别模块
│   ├── chat_model.py     # 对话模型接口
│   └── tts_model.py      # 语音合成模块
│
├── static/               # 静态资源
│   ├── audio/           # 语音文件存储
│   ├── css/
│   │   └── style.css   # 应用样式
│   └── js/
│       └── main.js     # 前端功能
│
└── templates/           # 模板文件
    └── index.html      # 主应用模板
```

---

## 🛠️ 开发说明

### 后端模块

#### 核心应用 (`web_app.py`)
Flask 应用主程序，负责路由分发和请求处理。提供以下 API 端点：
- `POST /api/chat`
  - 功能：处理对话请求，生成 AI 响应
  - 输入：用户消息、输出偏好等
  - 输出：AI 响应内容、情感状态、音频 URL（如适用）

- `POST /api/speech-to-text`
  - 功能：语音输入转文字
  - 输入：音频文件（WebM 格式）
  - 输出：识别后的文本内容

- `GET /api/get-memory`
  - 功能：获取历史对话记录
  - 输出：按时间顺序的对话列表

#### 模型模块 (`models/`)
- `asr_model.py`: 集成 Whisper 的语音识别模块，支持多语言转写
- `chat_model.py`: DeepSeek Chat API 对话接口，处理上下文和情感
- `tts_model.py`: Edge TTS 语音合成模块，提供自然的语音输出

### 前端结构

#### 静态资源 (`static/`)
- `js/main.js`: 前端核心逻辑
  - 语音录制和播放控制
  - WebSocket 通信管理
  - UI 状态管理和动画
  - 消息发送和接收处理
- `css/style.css`: 响应式布局和主题样式
- `audio/`: 语音文件缓存目录
  - 存储用户语音输入（WebM）
  - 存储 AI 语音回复（WAV）

#### 页面模板 (`templates/`)
- `index.html`: 主界面模板，包含聊天界面和设置面板

---

## 📢 免责声明

Lyra 是一个实验性的开源项目，目的是初步探索多模态交互技术。  
欢迎根据您的需求进行扩展和定制。