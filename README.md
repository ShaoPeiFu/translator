# 🌐 英语翻译 Agent

基于 Qwen 模型的智能英语翻译工具，提供准确、流畅的中文翻译服务。

## ✨ 功能特性

- 🔤 **智能翻译**: 使用 Qwen 模型进行高质量的英语到中文翻译
- 🔍 **语言检测**: 自动检测输入文本的语言类型
- 📝 **批量翻译**: 支持一次翻译多句文本，提高效率
- 📖 **术语表翻译**: 使用自定义术语表，确保专业术语翻译准确性
- 📄 **PDF 文档翻译**: 自动提取 PDF 文本并进行翻译，支持多种导出格式
- 💾 **翻译历史**: 保存和管理所有翻译记录
- 🎛️ **参数调节**: 可调节模型参数以获得最佳翻译效果
- 🌐 **Web 界面**: 基于 Streamlit 的友好用户界面

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- 阿里云 DashScope API 密钥

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥

#### 方法 1: 环境变量 (推荐)

```bash
export DASHSCOPE_API_KEY="your_api_key_here"
```

#### 方法 2: .env 文件

在项目根目录创建`.env`文件：

```
DASHSCOPE_API_KEY=your_api_key_here
```

### 4. 运行应用

#### Web 界面 (推荐)

```bash
streamlit run streamlit_app.py
```

#### 命令行测试

```bash
python agent.py
```

#### PDF 翻译测试

```bash
python test_pdf_translation.py
```

## 📖 使用方法

### Web 界面使用

1. **启动应用**: 运行`streamlit run streamlit_app.py`
2. **输入 API 密钥**: 在侧边栏输入你的 DashScope API 密钥
3. **选择功能**: 使用不同的标签页进行不同类型的翻译
4. **开始翻译**: 输入英文文本，点击翻译按钮

### PDF 翻译功能

#### 基本使用流程

1. **上传 PDF 文件**: 在"PDF 翻译"标签页上传 PDF 文档
2. **配置参数**: 调整文本块大小、延迟时间、重试次数等
3. **选择文档类型**: 选择文档类型以获得更准确的翻译
4. **开始翻译**: 点击"开始翻译 PDF"按钮
5. **查看结果**: 查看翻译摘要和预览结果
6. **下载结果**: 下载 TXT 或 DOCX 格式的翻译结果

#### 高级配置选项

- **文本块大小**: 控制每次翻译的文本长度（500-2000 字符）
- **块间延迟**: 避免 API 限制的延迟时间（0.5-3 秒）
- **最大重试次数**: 翻译失败时的重试次数（1-5 次）
- **文档类型**: 技术文档、学术论文、商务报告等

#### 支持的文件格式

- **输入**: PDF 文档
- **输出**: TXT 文本文件、DOCX 文档、JSON 数据

### 编程接口使用

```python
from agent import TranslationAgent
from pdf_translator import PDFTranslator

# 创建翻译agent
agent = TranslationAgent(api_key="你的API密钥")

# 单句翻译
result = agent.translate_to_chinese("Hello, how are you?")
print(result["translation"])

# 语言检测
lang = agent.detect_language("Hello world")
print(lang)

# 批量翻译
texts = ["Hello", "How are you?", "Nice to meet you"]
results = agent.batch_translate(texts)

# 术语表翻译
glossary = {"API": "应用程序接口", "SDK": "软件开发工具包"}
result = agent.translate_with_glossary("This API provides SDK functionality", glossary)

# PDF翻译
pdf_translator = PDFTranslator(api_key="你的API密钥")
result = pdf_translator.translate_pdf_file("document.pdf", context="技术文档")
```

## 🔧 配置选项

### 模型选择

- `qwen-max`: 最高质量，适合重要文档翻译
- `qwen-plus`: 平衡质量和速度
- `qwen-turbo`: 最快速度，适合实时翻译

### 参数调节

- **Temperature**: 控制翻译的创造性 (0.0-1.0)
- **Max Tokens**: 控制输出文本的最大长度
- **Context**: 提供上下文信息以获得更准确的翻译

### PDF 翻译配置

- **Chunk Size**: 文本块大小，影响翻译质量和速度
- **Delay**: 块间延迟，避免 API 限制
- **Retries**: 重试次数，提高成功率

## 📚 API 参考

### TranslationAgent 类

#### 主要方法

- `translate_to_chinese(text, context="")`: 将英文翻译成中文
- `detect_language(text)`: 检测文本语言
- `batch_translate(texts)`: 批量翻译文本列表
- `translate_with_glossary(text, glossary)`: 使用术语表翻译
- `translate_pdf_content(text, context="")`: 翻译 PDF 内容
- `translate_pdf_chunks(text_chunks, context="")`: 翻译 PDF 文本块

### PDFTranslator 类

#### 主要方法

- `translate_pdf_file(pdf_path, context="", output_dir="")`: 翻译整个 PDF 文件
- `set_translation_config(chunk_size, delay, max_retries)`: 设置翻译配置
- `get_translation_summary(translation_results)`: 获取翻译摘要

### PDFProcessor 类

#### 主要方法

- `extract_text_from_pdf(pdf_path)`: 从 PDF 提取文本
- `split_text_for_translation(text, max_chunk_size)`: 分割文本为翻译块
- `export_translation_result(original, translated, output_path, format)`: 导出翻译结果

#### 参数说明

- `text`: 要翻译的英文文本
- `context`: 可选的上下文信息
- `glossary`: 术语表字典，格式为{英文: 中文}
- `pdf_path`: PDF 文件路径
- `chunk_size`: 文本块大小

#### 返回值

所有翻译方法都返回包含以下字段的字典：

- `original`: 原文
- `translation`: 翻译结果
- `status`: 状态 ("success" 或 "error")
- `model`: 使用的模型名称
- `error`: 错误信息 (如果失败)

## 🌟 使用场景

- 📧 **商务邮件翻译**: 快速翻译英文商务邮件
- 📄 **技术文档翻译**: 使用术语表确保技术准确性
- 📚 **学术论文翻译**: 高质量学术内容翻译
- 💬 **日常对话翻译**: 实时对话翻译
- 📱 **应用界面翻译**: 软件界面文本翻译
- 📋 **PDF 文档翻译**: 技术手册、用户指南、合同文件等

## 🔒 安全说明

- API 密钥仅存储在本地环境变量中
- 不会将翻译内容发送到第三方服务
- 支持本地部署，保护数据隐私
- PDF 文件仅临时处理，不会永久存储

## 🐛 故障排除

### 常见问题

1. **API 密钥错误**

   - 检查 API 密钥是否正确
   - 确认 API 密钥有足够的配额

2. **翻译失败**

   - 检查网络连接
   - 确认输入文本格式正确
   - 查看错误信息进行调试

3. **模型响应慢**

   - 尝试使用`qwen-turbo`模型
   - 减少`max_tokens`参数值
   - 检查网络延迟

4. **PDF 翻译问题**

   - 确认 PDF 不是扫描版（无法提取文本）
   - 检查 PDF 文件大小（建议<50MB）
   - 调整文本块大小和延迟参数

5. **依赖包安装失败**

   - 更新 pip: `pip install --upgrade pip`
   - 使用虚拟环境: `python -m venv venv && source venv/bin/activate`
   - 手动安装: `pip install PyPDF2 pdfplumber python-docx`

## 📄 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 📞 支持

如果遇到问题，请：

1. 查看本文档的故障排除部分
2. 提交 GitHub Issue
3. 联系项目维护者

---

**享受智能翻译的便利！** 🎉
