import streamlit as st
import json
from agent import TranslationAgent
from pdf_translator import PDFTranslator
from pdf_viewer import PDFViewer
import os
from dotenv import load_dotenv
import tempfile
import time

# 加载环境变量
load_dotenv()

# 页面配置
st.set_page_config(page_title="英语翻译Agent", page_icon="🌐", layout="wide")

# 页面标题
st.title("🌐 英语翻译Agent")
st.markdown("基于Qwen模型的智能英语翻译工具")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")

    # API密钥输入
    # api_key = st.text_input(
    #     "DASHSCOPE API密钥",
    #     value=os.getenv("DASHSCOPE_API_KEY", ""),
    #     type="password",
    #     help="请输入你的阿里云DashScope API密钥",
    # )
    api_key = os.getenv("DASHSCOPE_API_KEY")

    # 模型选择
    model_options = ["qwen-max", "qwen-plus", "qwen-turbo"]
    selected_model = st.selectbox("选择模型", model_options, index=0)

    # 温度设置
    temperature = st.slider("创造性 (Temperature)", 0.0, 1.0, 0.1, 0.1)

    # 最大token数
    max_tokens = st.slider("最大输出长度", 500, 4000, 2000, 100)

    # st.markdown("---")
    # st.markdown("### 📚 功能特性")
    # st.markdown("- ✨ 智能英语翻译")
    # st.markdown("- 🔍 语言自动检测")
    # st.markdown("- 📝 批量翻译支持")
    # st.markdown("- 📖 术语表翻译")
    # st.markdown("- 📄 PDF文档翻译")
    # st.markdown("- 💾 翻译历史记录")

# 主界面
if not api_key:
    st.warning("⚠️ 请在侧边栏输入DASHSCOPE_API_KEY以开始使用")
    st.stop()

try:
    # 初始化翻译agent
    agent = TranslationAgent(api_key)
    agent.model = selected_model
    agent.temperature = temperature
    agent.max_tokens = max_tokens

    # 初始化PDF翻译器
    pdf_translator = PDFTranslator(api_key)

    # 创建标签页
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🔤 单句翻译", "📄 批量翻译", "📖 术语表翻译", "📚 PDF翻译", "📊 翻译历史"]
    )

    # 标签页1: 单句翻译
    with tab1:
        st.header("🔤 单句翻译")

        # 输入区域
        col1, col2 = st.columns(2)

        with col1:
            input_text = st.text_area(
                "输入英文文本", height=200, placeholder="请输入要翻译的英文文本..."
            )

            # 上下文信息
            context = st.text_input(
                "上下文信息 (可选)", placeholder="例如：技术文档、商务邮件、文学作品等"
            )

            # 翻译按钮
            if st.button("开始翻译", type="primary", use_container_width=True):
                if input_text.strip():
                    with st.spinner("正在翻译中..."):
                        # 语言检测
                        detected_lang = agent.detect_language(input_text)

                        # 执行翻译
                        result = agent.translate_to_chinese(input_text, context)

                        # 显示结果
                        with col2:
                            st.subheader("翻译结果")

                            # 语言检测结果
                            st.info(f"检测到的语言: {detected_lang}")

                            if result["status"] == "success":
                                st.success("✅ 翻译完成")
                                st.text_area(
                                    "中文翻译",
                                    result["translation"],
                                    height=200,
                                    disabled=True,
                                )

                                # 保存到历史记录
                                if "translation_history" not in st.session_state:
                                    st.session_state.translation_history = []

                                history_item = {
                                    "original": input_text,
                                    "translation": result["translation"],
                                    "context": context,
                                    "model": result["model"],
                                    "timestamp": st.session_state.get(
                                        "current_time", "未知"
                                    ),
                                }
                                st.session_state.translation_history.append(
                                    history_item
                                )

                            else:
                                st.error(
                                    f"❌ 翻译失败: {result.get('error', '未知错误')}"
                                )
                else:
                    st.warning("请输入要翻译的文本")

    # 标签页2: 批量翻译
    with tab2:
        st.header("📄 批量翻译")

        batch_input = st.text_area(
            "输入多行英文文本 (每行一句)",
            height=300,
            placeholder="请输入多行英文文本，每行一句...\n例如：\nHello world\nHow are you?\nNice to meet you",
        )

        if st.button("🚀 批量翻译", type="primary", use_container_width=True):
            if batch_input.strip():
                texts = [
                    line.strip() for line in batch_input.split("\n") if line.strip()
                ]

                if texts:
                    with st.spinner(f"正在批量翻译 {len(texts)} 句文本..."):
                        results = agent.batch_translate(texts)

                        # 显示结果
                        st.subheader("批量翻译结果")

                        for i, result in enumerate(results):
                            with st.expander(f"第 {i+1} 句", expanded=True):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown("**原文:**")
                                    st.text(result["original"])
                                with col2:
                                    if result["status"] == "success":
                                        st.markdown("**翻译:**")
                                        st.success(result["translation"])
                                    else:
                                        st.markdown("**错误:**")
                                        st.error(result.get("error", "翻译失败"))
            else:
                st.warning("请输入要翻译的文本")

    # 标签页3: 术语表翻译
    with tab3:
        st.header("📖 术语表翻译")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("术语表设置")

            # 术语表输入
            glossary_input = st.text_area(
                "术语表 (格式: 英文=中文，每行一个)",
                height=200,
                placeholder="例如：\nAPI=应用程序接口\nSDK=软件开发工具包\nUI=用户界面",
            )

            # 解析术语表
            glossary = {}
            if glossary_input.strip():
                for line in glossary_input.split("\n"):
                    if "=" in line:
                        en, zh = line.split("=", 1)
                        glossary[en.strip()] = zh.strip()

            if glossary:
                st.success(f"✅ 已加载 {len(glossary)} 个术语")
                st.json(glossary)

            # 要翻译的文本
            glossary_text = st.text_area(
                "要翻译的文本",
                height=150,
                placeholder="请输入要使用术语表翻译的英文文本...",
            )

            if st.button("🚀 术语表翻译", type="primary", use_container_width=True):
                if glossary_text.strip() and glossary:
                    with st.spinner("正在使用术语表翻译..."):
                        result = agent.translate_with_glossary(glossary_text, glossary)

                        with col2:
                            st.subheader("术语表翻译结果")

                            if result["status"] == "success":
                                st.success("✅ 翻译完成")
                                st.text_area(
                                    "中文翻译",
                                    result["translation"],
                                    height=200,
                                    disabled=True,
                                )
                                st.info("使用了术语表进行翻译")
                            else:
                                st.error(
                                    f"❌ 翻译失败: {result.get('error', '未知错误')}"
                                )
                else:
                    st.warning("请确保输入了文本和术语表")

    # 标签页4: PDF翻译
    with tab4:
        st.header("📚 PDF文档翻译")
        st.markdown("上传PDF文档，自动提取文本并进行翻译")

        # PDF翻译配置
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📋 翻译配置")

            # 文本块大小
            chunk_size = st.slider(
                "文本块大小",
                500,
                2000,
                1000,
                100,
                help="较大的块保持上下文，较小的块翻译更快",
            )

            # 块间延迟
            delay = st.slider(
                "块间延迟 (秒)", 0.5, 3.0, 1.0, 0.1, help="避免API限制，建议1-2秒"
            )

            # 最大重试次数
            max_retries = st.slider(
                "最大重试次数", 1, 5, 3, 1, help="翻译失败时的重试次数"
            )

            # 文档类型
            doc_context = st.selectbox(
                "文档类型",
                [
                    "",
                    "技术文档",
                    "学术论文",
                    "商务报告",
                    "用户手册",
                    "合同文件",
                    "其他",
                ],
                help="选择文档类型以获得更准确的翻译",
            )

            # 应用配置
            if st.button("⚙️ 应用配置", type="secondary"):
                pdf_translator.set_translation_config(chunk_size, delay, max_retries)
                st.success("✅ 配置已应用")

        with col2:
            st.subheader("📁 文件上传")

            # 文件上传
            uploaded_file = st.file_uploader(
                "选择PDF文件", type=["pdf"], help="支持PDF格式，文件大小建议不超过50MB"
            )

            if uploaded_file is not None:
                # 显示文件信息
                file_details = {
                    "文件名": uploaded_file.name,
                    "文件大小": f"{uploaded_file.size / 1024 / 1024:.2f} MB",
                    "文件类型": uploaded_file.type,
                }
                st.json(file_details)

                # 翻译按钮
                if st.button(
                    "🚀 开始翻译PDF", type="primary", use_container_width=True
                ):
                    # 保存上传的文件到临时目录
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".pdf"
                    ) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    try:
                        # 开始翻译
                        with st.spinner("正在处理PDF文档..."):
                            # 显示进度条
                            progress_bar = st.progress(0)
                            status_text = st.empty()

                            # 翻译PDF
                            result = pdf_translator.translate_pdf_file(
                                tmp_file_path,
                                context=doc_context,
                                output_dir="translated_pdfs",
                            )

                            # 清理临时文件
                            os.unlink(tmp_file_path)

                            if result["status"] == "success":
                                st.success("✅ PDF翻译完成！")

                                # 显示翻译摘要
                                summary = pdf_translator.get_translation_summary(
                                    result["translation_results"]
                                )

                                col_summary1, col_summary2 = st.columns(2)
                                with col_summary1:
                                    st.metric("总文本块", summary["total_chunks"])
                                    st.metric("成功翻译", summary["successful_chunks"])
                                    st.metric("成功率", f"{summary['success_rate']}%")

                                with col_summary2:
                                    st.metric(
                                        "原文字符数",
                                        f"{summary['total_original_chars']:,}",
                                    )
                                    st.metric(
                                        "翻译字符数",
                                        f"{summary['total_translated_chars']:,}",
                                    )
                                    st.metric(
                                        "平均块大小",
                                        f"{summary['average_chars_per_chunk']:.0f}",
                                    )

                                # 显示翻译结果
                                st.subheader("📖 翻译结果预览")

                                # 原文和翻译对比
                                col_orig, col_trans = st.columns(2)

                                with col_orig:
                                    st.markdown("**原文预览**")
                                    st.text_area(
                                        "原文",
                                        result["original_text"][:1000] + "...",
                                        height=200,
                                        disabled=True,
                                    )

                                with col_trans:
                                    st.markdown("**翻译预览**")
                                    st.text_area(
                                        "翻译",
                                        result["translated_text"][:1000] + "...",
                                        height=200,
                                        disabled=True,
                                    )

                                # PDF对比显示
                                st.subheader("📄 PDF对比显示")

                                # 检查是否有PDF格式的导出结果
                                pdf_export_result = None
                                if (
                                    result.get("export_result", {})
                                    .get("formats", {})
                                    .get("pdf", {})
                                    .get("status")
                                    == "success"
                                ):
                                    pdf_export_result = result["export_result"][
                                        "formats"
                                    ]["pdf"]

                                if pdf_export_result:
                                    st.success("✅ PDF对比文档已生成")

                                    # 使用PDF查看器显示对比文档
                                    pdf_path = pdf_export_result["output_path"]
                                    PDFViewer.create_comparison_viewer(
                                        pdf_path, width=100, height=600
                                    )

                                else:
                                    st.warning("⚠️ PDF对比文档生成失败")

                                    # 显示详细的错误信息
                                    pdf_error = (
                                        result.get("export_result", {})
                                        .get("formats", {})
                                        .get("pdf", {})
                                    )
                                    if pdf_error and pdf_error.get("error"):
                                        st.error(f"错误详情: {pdf_error['error']}")

                                    # 提供调试信息
                                    with st.expander("🔍 调试信息"):
                                        st.write("**导出结果状态:**")
                                        st.json(result.get("export_result", {}))

                                        st.write("**PDF格式状态:**")
                                        st.json(
                                            result.get("export_result", {})
                                            .get("formats", {})
                                            .get("pdf", {})
                                        )

                                    # 提供解决方案建议
                                    st.info("💡 解决方案建议:")
                                    st.markdown(
                                        """
                                    1. **检查权限**: 确保应用有写入输出目录的权限
                                    2. **检查依赖**: 确保已安装reportlab库 (`pip install reportlab`)
                                    3. **检查字体**: 系统可能缺少中文字体支持
                                    4. **重新尝试**: 点击翻译按钮重新生成
                                    5. **查看日志**: 检查控制台输出的详细错误信息
                                    """
                                    )

                                    # 提供手动重试按钮
                                    if st.button(
                                        "🔄 重新生成PDF对比", type="secondary"
                                    ):
                                        st.rerun()

                                # 下载链接
                                st.subheader("💾 下载翻译结果")

                                if (
                                    result.get("export_result", {}).get("status")
                                    == "success"
                                ):
                                    output_dir = result["export_result"][
                                        "output_directory"
                                    ]

                                    # 创建下载按钮
                                    for format_type, format_result in result[
                                        "export_result"
                                    ]["formats"].items():
                                        if format_result["status"] == "success":
                                            file_path = format_result["output_path"]
                                            file_name = os.path.basename(file_path)

                                            with open(file_path, "rb") as f:
                                                st.download_button(
                                                    label=f"📥 下载 {format_type.upper()} 格式",
                                                    data=f.read(),
                                                    file_name=file_name,
                                                    mime="application/octet-stream",
                                                )
                                else:
                                    st.warning("导出失败，请检查输出目录权限")

                                # 保存到历史记录
                                if "translation_history" not in st.session_state:
                                    st.session_state.translation_history = []

                                history_item = {
                                    "type": "PDF翻译",
                                    "file_name": uploaded_file.name,
                                    "original_length": len(result["original_text"]),
                                    "translated_length": len(result["translated_text"]),
                                    "chunks": summary["total_chunks"],
                                    "success_rate": summary["success_rate"],
                                    "model": agent.model,
                                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                                }
                                st.session_state.translation_history.append(
                                    history_item
                                )

                            elif result["status"] == "warning":
                                st.warning(f"⚠️ {result['message']}")
                                st.info(f"💡 建议: {result['suggestion']}")

                            else:
                                st.error(
                                    f"❌ 翻译失败: {result.get('error', '未知错误')}"
                                )

                    except Exception as e:
                        st.error(f"❌ 处理过程中出现错误: {str(e)}")
                        # 清理临时文件
                        if os.path.exists(tmp_file_path):
                            os.unlink(tmp_file_path)
            else:
                st.info("📁 请上传PDF文件开始翻译")

    # 标签页5: 翻译历史
    with tab5:
        st.header("📊 翻译历史")

        if (
            "translation_history" in st.session_state
            and st.session_state.translation_history
        ):
            # 显示历史记录
            for i, item in enumerate(reversed(st.session_state.translation_history)):
                with st.expander(
                    f"翻译记录 {len(st.session_state.translation_history) - i}",
                    expanded=False,
                ):
                    if item.get("type") == "PDF翻译":
                        # PDF翻译记录
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**文件:** {item['file_name']}")
                            st.markdown(f"**类型:** {item['type']}")
                            st.markdown(f"**文本块:** {item['chunks']}")
                        with col2:
                            st.markdown(f"**成功率:** {item['success_rate']}%")
                            st.markdown(f"**模型:** {item['model']}")
                            st.markdown(f"**时间:** {item['timestamp']}")
                    else:
                        # 普通翻译记录
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**原文:**")
                            st.text(item["original"])
                            if item.get("context"):
                                st.caption(f"上下文: {item['context']}")
                        with col2:
                            st.markdown("**翻译:**")
                            st.text(item["translation"])
                            st.caption(f"模型: {item['model']}")

            # 清空历史记录按钮
            if st.button("🗑️ 清空历史记录", type="secondary"):
                st.session_state.translation_history = []
                st.rerun()
        else:
            st.info("📝 暂无翻译历史记录")

    # 底部信息


except Exception as e:
    st.error(f"❌ 初始化失败: {str(e)}")
    st.info("请检查API密钥是否正确，或查看错误信息")
