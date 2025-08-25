# 📁 项目结构说明

```
ai_agent_project/
├── 📄 agent.py              # 核心翻译Agent类
├── 📚 pdf_processor.py      # PDF处理模块
├── 📖 pdf_translator.py     # PDF翻译器主类
├── 🌐 streamlit_app.py      # Streamlit Web应用界面
├── 🧪 test_translation.py   # 功能测试脚本
├── 🧪 test_pdf_translation.py # PDF翻译功能测试脚本
├── 🚀 run.py               # 一键启动脚本
├── 📦 requirements.txt      # 项目依赖包
├── 📚 README.md            # 项目说明文档
├── 🔧 env_example.txt      # 环境变量配置示例
└── 📁 PROJECT_STRUCTURE.md # 项目结构说明（本文件）
```

## 📋 文件功能说明

### 🔧 核心文件

- **`agent.py`**: 翻译 Agent 的核心实现

  - `TranslationAgent`类：主要的翻译功能类
  - 支持单句翻译、批量翻译、术语表翻译
  - 集成 Qwen 模型 API 调用
  - 语言检测功能
  - PDF 内容翻译支持

- **`pdf_processor.py`**: PDF 文档处理模块

  - `PDFProcessor`类：PDF 文本提取和处理
  - 支持文本清理、分割和合并
  - 多种格式导出（TXT、DOCX、JSON）
  - 扫描版 PDF 检测

- **`pdf_translator.py`**: PDF 翻译器主类

  - `PDFTranslator`类：整合 PDF 处理和翻译功能
  - 支持大文档分块翻译
  - 进度跟踪和重试机制
  - 翻译结果导出和管理

- **`streamlit_app.py`**: Web 用户界面
  - 五个功能标签页：单句翻译、批量翻译、术语表翻译、PDF 翻译、翻译历史
  - PDF 翻译配置面板
  - 文件上传和下载功能
  - 参数调节面板（模型选择、温度、最大 token 数）

### 🧪 测试和工具

- **`test_translation.py`**: 功能测试脚本

  - 测试所有翻译功能
  - 测试不同模型参数
  - 验证 API 连接和功能

- **`test_pdf_translation.py`**: PDF 翻译功能测试脚本

  - 测试 PDF 处理功能
  - 测试文本提取和翻译
  - 验证文件操作功能

- **`run.py`**: 一键启动脚本
  - 自动检查依赖
  - 验证 API 密钥配置
  - 启动 Streamlit 应用

### 📚 文档和配置

- **`requirements.txt`**: Python 依赖包列表
- **`README.md`**: 详细的使用说明和 API 文档
- **`env_example.txt`**: 环境变量配置示例
- **`PROJECT_STRUCTURE.md`**: 项目结构说明（本文件）

## 🚀 快速开始流程

1. **克隆项目**: 下载所有文件到本地目录
2. **安装依赖**: `pip install -r requirements.txt`
3. **配置 API**: 设置`DASHSCOPE_API_KEY`环境变量
4. **启动应用**: 运行`python run.py`或`streamlit run streamlit_app.py`

## 🔄 开发工作流

1. **修改核心逻辑**: 编辑`agent.py`、`pdf_processor.py`、`pdf_translator.py`
2. **更新界面**: 修改`streamlit_app.py`
3. **测试功能**: 运行`python test_translation.py`和`python test_pdf_translation.py`
4. **启动应用**: 使用`python run.py`验证

## 📁 扩展建议

- 添加更多语言支持
- 集成其他 AI 模型
- 增加翻译质量评估
- 支持更多文档格式（Word、Excel、PowerPoint）
- 添加 OCR 功能支持扫描版 PDF
- 支持批量 PDF 处理
- 添加用户认证系统
- 集成云存储服务

## 🔧 技术架构

### 核心组件关系

```
用户界面 (Streamlit)
    ↓
PDF翻译器 (PDFTranslator)
    ↓
PDF处理器 (PDFProcessor) + 翻译Agent (TranslationAgent)
    ↓
Qwen模型API (DashScope)
```

### 数据流

1. **PDF 上传** → 文件验证和临时存储
2. **文本提取** → PDF 文本提取和清理
3. **文本分割** → 按大小分割为可翻译的块
4. **批量翻译** → 逐块调用翻译 API
5. **结果合并** → 合并所有翻译结果
6. **格式导出** → 导出为多种格式
7. **文件下载** → 提供下载链接

### 性能优化

- 文本块大小可调节（500-2000 字符）
- 块间延迟避免 API 限制
- 重试机制提高成功率
- 进度跟踪和状态显示
- 临时文件自动清理
