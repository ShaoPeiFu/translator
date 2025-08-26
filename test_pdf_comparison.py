#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF对比功能测试脚本
测试PDF生成、对比显示等功能
"""

import os
import tempfile
import sys
from dotenv import load_dotenv
from pdf_translator import PDFTranslator
from pdf_processor import PDFProcessor


def check_system_info():
    """检查系统信息"""
    print("🖥️ 系统信息:")
    print(f"   操作系统: {sys.platform}")
    print(f"   Python版本: {sys.version}")
    print(f"   当前工作目录: {os.getcwd()}")

    # 检查macOS特定信息
    if sys.platform == "darwin":
        print("   系统: macOS")
        # 检查字体目录
        font_dirs = [
            "/System/Library/Fonts",
            "/Library/Fonts",
            "/Users/" + os.getenv("USER", "unknown") + "/Library/Fonts",
        ]
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                print(f"   字体目录: {font_dir} (存在)")
            else:
                print(f"   字体目录: {font_dir} (不存在)")


def check_dependencies():
    """检查依赖库"""
    print("\n📦 依赖库检查:")

    required_packages = ["reportlab", "PyPDF2", "pdfplumber", "python-docx", "Pillow"]

    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}: 已安装")
        except ImportError:
            print(f"   ❌ {package}: 未安装")


def check_fonts():
    """检查字体可用性"""
    print("\n🔤 字体检查:")

    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        # 测试字体注册
        test_fonts = [
            ("Helvetica", "Helvetica"),
            ("Arial", "Arial"),
            ("Times", "Times"),
        ]

        for font_name, font_path in test_fonts:
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                print(f"   ✅ {font_name}: 可用")
            except Exception as e:
                print(f"   ❌ {font_name}: 不可用 - {e}")

    except ImportError:
        print("   ❌ 无法导入reportlab字体模块")


def test_pdf_generation():
    """测试PDF生成功能"""
    print("\n🧪 测试PDF生成功能...")

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
            print(f"   临时目录: {temp_dir}")

            # 测试普通PDF生成
            pdf_path = os.path.join(temp_dir, "test_comparison.pdf")
            print(f"   测试文件路径: {pdf_path}")

            result = processor.create_comparison_pdf(
                original_text, translated_text, pdf_path, "测试对比文档"
            )

            print(f"   生成结果: {result}")

            if result["status"] == "success":
                print(f"   ✅ 普通PDF生成成功: {result['output_path']}")
                if os.path.exists(pdf_path):
                    print(f"   文件大小: {os.path.getsize(pdf_path)} 字节")
                    print(f"   文件权限: {oct(os.stat(pdf_path).st_mode)[-3:]}")
                else:
                    print("   ⚠️ 文件路径存在但文件不存在")
            else:
                print(f"   ❌ 普通PDF生成失败: {result.get('error', '未知错误')}")

            # 测试左右对比PDF生成
            side_pdf_path = os.path.join(temp_dir, "test_side_by_side.pdf")
            translator = PDFTranslator()
            side_result = translator.create_side_by_side_pdf(
                original_text, translated_text, side_pdf_path, "左右对比测试"
            )

            print(f"   左右对比生成结果: {side_result}")

            if side_result["status"] == "success":
                print(f"   ✅ 左右对比PDF生成成功: {side_result['output_path']}")
                if os.path.exists(side_pdf_path):
                    print(f"   文件大小: {os.path.getsize(side_pdf_path)} 字节")
                    print(f"   文件权限: {oct(os.stat(side_pdf_path).st_mode)[-3:]}")
                else:
                    print("   ⚠️ 文件路径存在但文件不存在")
            else:
                print(
                    f"   ❌ 左右对比PDF生成失败: {side_result.get('error', '未知错误')}"
                )

        print("✅ PDF生成功能测试完成\n")
        return True

    except Exception as e:
        print(f"❌ PDF生成功能测试失败: {e}")
        import traceback

        traceback.print_exc()
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
                    print(f"   ✅ {fmt.upper()} 格式导出成功")
                    if os.path.exists(output_path):
                        print(f"   文件大小: {os.path.getsize(output_path)} 字节")
                else:
                    print(
                        f"   ❌ {fmt.upper()} 格式导出失败: {result.get('error', '未知错误')}"
                    )

        print("✅ PDF导出功能测试完成\n")
        return True

    except Exception as e:
        print(f"❌ PDF导出功能测试失败: {e}")
        return False


def test_permissions():
    """测试权限和目录创建"""
    print("🔐 测试权限和目录创建...")

    try:
        # 测试当前目录权限
        current_dir = os.getcwd()
        print(f"   当前目录: {current_dir}")
        print(f"   可写: {os.access(current_dir, os.W_OK)}")
        print(f"   可读: {os.access(current_dir, os.R_OK)}")

        # 测试临时目录创建
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"   临时目录: {temp_dir}")
            print(f"   可写: {os.access(temp_dir, os.W_OK)}")
            print(f"   可读: {os.access(temp_dir, os.R_OK)}")

            # 测试文件创建
            test_file = os.path.join(temp_dir, "test_permission.txt")
            try:
                with open(test_file, "w") as f:
                    f.write("test")
                print(f"   ✅ 文件创建成功: {test_file}")

                # 测试文件权限
                print(f"   文件权限: {oct(os.stat(test_file).st_mode)[-3:]}")

                # 清理
                os.remove(test_file)
                print("   ✅ 文件删除成功")

            except Exception as e:
                print(f"   ❌ 文件操作失败: {e}")

        print("✅ 权限测试完成\n")
        return True

    except Exception as e:
        print(f"❌ 权限测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🌐 PDF对比功能测试程序")
    print("=" * 50)

    # 加载环境变量
    load_dotenv()

    # 系统信息检查
    check_system_info()

    # 依赖检查
    check_dependencies()

    # 字体检查
    check_fonts()

    # 权限测试
    test_permissions()

    # PDF生成测试
    test_pdf_generation()

    # PDF导出测试
    test_pdf_export()

    print("🎉 所有测试完成！")
    print("\n💡 如果PDF对比功能仍有问题，请检查:")
    print("   1. 确保已安装所有依赖库")
    print("   2. 检查系统字体配置")
    print("   3. 确保有足够的磁盘空间和写入权限")
    print("   4. 查看详细的错误日志")


if __name__ == "__main__":
    main()
