# PDF 对比显示问题修复指南

## 🚨 问题描述

在使用英语翻译 Agent 时，可能会遇到以下错误：

```
⚠️ PDF对比文档生成失败
请检查PDF生成权限或重新尝试翻译
```

## 🔍 问题原因分析

PDF 对比显示失败的主要原因包括：

1. **依赖库缺失** - 缺少必要的 PDF 生成库
2. **字体配置问题** - 系统缺少中文字体支持
3. **权限问题** - 输出目录没有写入权限
4. **系统兼容性** - macOS 系统的字体路径问题

## 🛠️ 快速修复方案

### 方案 1：运行自动修复脚本

```bash
python fix_pdf_comparison.py
```

这个脚本会自动：

- 检查并安装缺失的依赖库
- 验证字体支持
- 检查权限设置
- 创建必要的输出目录
- 运行功能测试

### 方案 2：手动安装依赖

```bash
pip install -r requirements.txt
```

确保以下关键依赖已安装：

- `reportlab>=4.0.0` - PDF 生成核心库
- `PyPDF2>=3.0.0` - PDF 处理库
- `pdfplumber>=0.9.0` - PDF 文本提取
- `python-docx>=0.8.11` - Word 文档支持
- `Pillow>=10.0.0` - 图像处理

### 方案 3：权限修复

```bash
# 创建输出目录
mkdir -p translated_pdfs output temp

# 检查目录权限
ls -la translated_pdfs/
```

确保应用有写入这些目录的权限。

## 🧪 功能测试

运行测试脚本验证修复效果：

```bash
python test_pdf_comparison.py
```

测试内容包括：

- 系统环境检查
- 依赖库验证
- 字体支持测试
- 权限检查
- PDF 生成功能测试
- 导出功能测试

## 🔧 高级修复

### 字体问题解决

如果遇到字体相关错误，可以：

1. **使用系统默认字体**：

   - 代码已自动回退到 Helvetica 字体
   - 支持英文和基本符号显示

2. **安装中文字体**：
   - macOS: 系统自带 PingFang、STHeiti 等字体
   - Windows: 安装 SimSun 字体
   - Linux: 安装 DejaVu 字体

### 输出目录配置

在`pdf_processor.py`中可以修改输出目录：

```python
# 默认输出目录
output_dirs = ["translated_pdfs", "output", "temp"]
```

## 📱 使用说明

修复完成后：

1. **重新启动应用**：

   ```bash
   streamlit run streamlit_app.py
   ```

2. **测试 PDF 翻译**：

   - 上传 PDF 文件
   - 执行翻译
   - 查看 PDF 对比显示

3. **检查输出文件**：
   - 查看`translated_pdfs/`目录
   - 确认 PDF 文件已生成
   - 验证文件大小和内容

## 🚀 预防措施

为避免类似问题：

1. **定期更新依赖**：

   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **环境一致性**：

   - 使用虚拟环境
   - 记录 Python 版本
   - 备份 requirements.txt

3. **权限管理**：
   - 定期检查目录权限
   - 避免在系统目录运行
   - 使用用户目录作为工作目录

## 📞 故障排除

如果问题仍然存在：

1. **查看详细日志**：

   - 运行测试脚本获取错误信息
   - 检查控制台输出
   - 查看 Streamlit 错误日志

2. **系统信息收集**：

   - 操作系统版本
   - Python 版本
   - 依赖库版本
   - 字体配置状态

3. **替代方案**：
   - 使用 TXT 格式导出
   - 使用 DOCX 格式导出
   - 手动复制翻译结果

## 🎯 成功标准

修复成功的标志：

- ✅ 所有依赖库正确安装
- ✅ PDF 生成功能正常
- ✅ 文件权限正确
- ✅ 输出目录可写
- ✅ 测试脚本全部通过
- ✅ Streamlit 应用正常运行
- ✅ PDF 对比显示正常

## 📚 相关资源

- [ReportLab 官方文档](https://www.reportlab.com/docs/reportlab-userguide.pdf)
- [PyPDF2 文档](https://pypdf2.readthedocs.io/)
- [Streamlit PDF 组件](https://docs.streamlit.io/library/api-reference/media/st.pdf_viewer)
- [macOS 字体管理](https://support.apple.com/guide/mac-help/use-fonts-mchlp1140/mac)

---

**注意**: 如果按照本指南操作后问题仍未解决，请提供详细的错误信息和系统环境信息，以便进一步诊断。
