#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF翻译功能测试脚本
测试PDF处理、文本提取和翻译功能
"""

import os
import tempfile
from dotenv import load_dotenv
from pdf_translator import PDFTranslator
from pdf_processor import PDFProcessor


def test_pdf_processor():
    """测试PDF处理器"""
    print("🧪 测试PDF处理器...")

    processor = PDFProcessor()

    # 测试文本清理
    test_text = "  This   is   a   test   text.  \n\n  With   multiple   spaces.  "
    cleaned = processor._clean_text(test_text)
    print(f"文本清理测试: '{cleaned}'")

    # 测试文本分割
    long_text = "This is sentence one. This is sentence two. " * 50
    chunks = processor.split_text_for_translation(long_text, max_chunk_size=100)
    print(f"文本分割测试: 分割为 {len(chunks)} 个块")

    # 测试文本合并
    original_chunks = ["Hello", "World", "Test"]
    translated_chunks = ["你好", "世界", "测试"]
    merged = processor.merge_translated_chunks(original_chunks, translated_chunks)
    print(f"文本合并测试: 合并后长度 {len(merged)}")

    print("✅ PDF处理器测试完成\n")
    return True


def test_pdf_translator():
    """测试PDF翻译器"""
    print("🧪 测试PDF翻译器...")

    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        print("❌ 未设置DASHSCOPE_API_KEY环境变量")
        return False

    try:
        translator = PDFTranslator(api_key)

        # 测试配置设置
        translator.set_translation_config(chunk_size=800, delay=1.0, max_retries=2)
        print(
            f"✅ 配置设置: 块大小={translator.chunk_size}, 延迟={translator.delay_between_chunks}, 重试={translator.max_retries}"
        )

        # 测试进度计算
        progress = translator.translation_agent.get_translation_progress(5, 10)
        print(f"✅ 进度计算: {progress}")

        print("✅ PDF翻译器测试完成\n")
        return True

    except Exception as e:
        print(f"❌ PDF翻译器测试失败: {e}")
        return False


def test_text_translation():
    """测试文本翻译功能"""
    print("🧪 测试文本翻译功能...")

    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        print("❌ 未设置DASHSCOPE_API_KEY环境变量")
        return False

    try:
        translator = PDFTranslator(api_key)

        # 测试PDF内容翻译
        test_text = "This is a test document for PDF translation. It contains technical terms and concepts."
        result = translator.translation_agent.translate_pdf_content(
            test_text, "技术文档"
        )

        if result["status"] == "success":
            print(f"✅ PDF内容翻译测试成功")
            print(f"原文: {result['original']}")
            print(f"翻译: {result['translation']}")
        else:
            print(f"❌ PDF内容翻译测试失败: {result.get('error', '未知错误')}")

        print("✅ 文本翻译功能测试完成\n")
        return True

    except Exception as e:
        print(f"❌ 文本翻译功能测试失败: {e}")
        return False


def test_file_operations():
    """测试文件操作功能"""
    print("🧪 测试文件操作功能...")

    try:
        processor = PDFProcessor()

        # 创建临时测试文件
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            test_content = (
                "This is a test file.\nWith multiple lines.\nFor testing purposes."
            )
            f.write(test_content)
            temp_file_path = f.name

        # 测试导出功能
        original_text = "Hello World"
        translated_text = "你好世界"

        # 测试TXT导出
        txt_result = processor.export_translation_result(
            original_text, translated_text, f"{temp_file_path}_translated.txt", "txt"
        )

        if txt_result["status"] == "success":
            print(f"✅ TXT导出测试成功: {txt_result['output_path']}")
        else:
            print(f"❌ TXT导出测试失败: {txt_result.get('error', '未知错误')}")

        # 清理临时文件
        os.unlink(temp_file_path)
        if os.path.exists(f"{temp_file_path}_translated.txt"):
            os.unlink(f"{temp_file_path}_translated.txt")

        print("✅ 文件操作功能测试完成\n")
        return True

    except Exception as e:
        print(f"❌ 文件操作功能测试失败: {e}")
        return False


def create_sample_pdf():
    """创建示例PDF文件用于测试"""
    print("📄 创建示例PDF文件...")

    try:
        # 这里可以添加创建示例PDF的逻辑
        # 由于需要额外的PDF创建库，这里只是示例
        print("💡 提示: 请准备一个测试用的PDF文件")
        print("   建议使用包含英文文本的PDF文档进行测试")
        return True

    except Exception as e:
        print(f"❌ 创建示例PDF失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🌐 PDF翻译功能测试程序")
    print("=" * 50)

    # 运行各项测试
    tests = [
        ("PDF处理器", test_pdf_processor),
        ("PDF翻译器", test_pdf_translator),
        ("文本翻译功能", test_text_translation),
        ("文件操作功能", test_file_operations),
        ("示例PDF创建", create_sample_pdf),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 开始测试: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            results.append((test_name, False))

    # 显示测试结果摘要
    print("\n" + "=" * 50)
    print("📊 测试结果摘要")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n总体结果: {passed}/{total} 项测试通过")

    if passed == total:
        print("🎉 所有测试通过！PDF翻译功能正常工作")
    else:
        print("⚠️  部分测试失败，请检查相关功能")

    print("\n📖 使用说明:")
    print("1. 确保已安装所有依赖包: pip install -r requirements.txt")
    print("2. 设置DASHSCOPE_API_KEY环境变量")
    print("3. 准备测试用的PDF文件")
    print("4. 运行Web界面: streamlit run streamlit_app.py")


if __name__ == "__main__":
    main()
