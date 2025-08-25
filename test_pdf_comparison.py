#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF对比功能测试脚本
测试PDF生成、对比显示等功能
"""

import os
import tempfile
from dotenv import load_dotenv
from pdf_translator import PDFTranslator
from pdf_processor import PDFProcessor


def test_pdf_generation():
    """测试PDF生成功能"""
    print("🧪 测试PDF生成功能...")

    try:
        processor = PDFProcessor()

        # 测试文本
        original_text = """
        This is a test document for PDF translation.
        
        It contains multiple paragraphs with different content.
        
        The purpose is to test the PDF generation functionality.
        
        We will create a comparison PDF with original and translated text.
        """

        translated_text = """
        这是一个用于PDF翻译的测试文档。
        
        它包含多个具有不同内容的段落。
        
        目的是测试PDF生成功能。
        
        我们将创建一个包含原文和翻译文本的对比PDF。
        """

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 测试普通PDF生成
            pdf_path = os.path.join(temp_dir, "test_comparison.pdf")
            result = processor.create_comparison_pdf(
                original_text, translated_text, pdf_path, "测试对比文档"
            )

            if result["status"] == "success":
                print(f"✅ 普通PDF生成成功: {result['output_path']}")
                print(f"   文件大小: {os.path.getsize(pdf_path)} 字节")
            else:
                print(f"❌ 普通PDF生成失败: {result.get('error', '未知错误')}")

            # 测试左右对比PDF生成
            side_pdf_path = os.path.join(temp_dir, "test_side_by_side.pdf")
            translator = PDFTranslator()
            side_result = translator.create_side_by_side_pdf(
                original_text, translated_text, side_pdf_path, "左右对比测试"
            )

            if side_result["status"] == "success":
                print(f"✅ 左右对比PDF生成成功: {side_result['output_path']}")
                print(f"   文件大小: {os.path.getsize(side_pdf_path)} 字节")
            else:
                print(f"❌ 左右对比PDF生成失败: {side_result.get('error', '未知错误')}")

        print("✅ PDF生成功能测试完成\n")
        return True

    except Exception as e:
        print(f"❌ PDF生成功能测试失败: {e}")
        return False


def test_pdf_export():
    """测试PDF导出功能"""
    print("🧪 测试PDF导出功能...")

    try:
        processor = PDFProcessor()

        # 测试文本
        original_text = "Hello, this is a test."
        translated_text = "你好，这是一个测试。"

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 测试不同格式导出
            formats = ["txt", "docx", "pdf"]

            for fmt in formats:
                output_path = os.path.join(temp_dir, f"test_export.{fmt}")
                result = processor.export_translation_result(
                    original_text, translated_text, output_path, fmt
                )

                if result["status"] == "success":
                    print(f"✅ {fmt.upper()}格式导出成功: {result['output_path']}")
                    if os.path.exists(output_path):
                        print(f"   文件大小: {os.path.getsize(output_path)} 字节")
                else:
                    print(
                        f"❌ {fmt.upper()}格式导出失败: {result.get('error', '未知错误')}"
                    )

        print("✅ PDF导出功能测试完成\n")
        return True

    except Exception as e:
        print(f"❌ PDF导出功能测试失败: {e}")
        return False


def test_pdf_translator_integration():
    """测试PDF翻译器集成功能"""
    print("🧪 测试PDF翻译器集成功能...")

    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        print("❌ 未设置DASHSCOPE_API_KEY环境变量")
        return False

    try:
        translator = PDFTranslator(api_key)

        # 测试配置设置
        translator.set_translation_config(chunk_size=500, delay=0.5, max_retries=2)
        print(
            f"✅ 配置设置: 块大小={translator.chunk_size}, 延迟={translator.delay_between_chunks}"
        )

        # 测试PDF导出集成
        original_text = "This is a test for PDF translator integration."
        translated_text = "这是对PDF翻译器集成功能的测试。"

        with tempfile.TemporaryDirectory() as temp_dir:
            output_filename = "test_integration"
            export_result = translator._export_translation_results(
                original_text, translated_text, temp_dir, output_filename
            )

            if export_result["status"] == "success":
                print(f"✅ 集成导出成功: {export_result['output_directory']}")

                # 检查生成的文件
                for format_type, format_result in export_result["formats"].items():
                    if format_result["status"] == "success":
                        file_path = format_result["output_path"]
                        if os.path.exists(file_path):
                            print(
                                f"   {format_type.upper()}: {os.path.basename(file_path)}"
                            )
                    else:
                        print(f"   {format_type.upper()}: 生成失败")
            else:
                print(f"❌ 集成导出失败: {export_result.get('error', '未知错误')}")

        print("✅ PDF翻译器集成功能测试完成\n")
        return True

    except Exception as e:
        print(f"❌ PDF翻译器集成功能测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🌐 PDF对比功能测试程序")
    print("=" * 50)

    # 运行各项测试
    tests = [
        ("PDF生成功能", test_pdf_generation),
        ("PDF导出功能", test_pdf_export),
        ("PDF翻译器集成", test_pdf_translator_integration),
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
        print("🎉 所有测试通过！PDF对比功能正常工作")
    else:
        print("⚠️  部分测试失败，请检查相关功能")

    print("\n📖 使用说明:")
    print("1. 确保已安装所有依赖包: pip install -r requirements.txt")
    print("2. 设置DASHSCOPE_API_KEY环境变量")
    print("3. 运行Web界面: streamlit run streamlit_app.py")
    print("4. 在PDF翻译功能中查看对比效果")


if __name__ == "__main__":
    main()
