#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF对比问题快速修复脚本
解决常见的PDF对比显示问题
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path


def check_and_install_dependencies():
    """检查并安装必要的依赖"""
    print("📦 检查依赖库...")

    required_packages = [
        "reportlab>=4.0.0",
        "PyPDF2>=3.0.0",
        "pdfplumber>=0.9.0",
        "python-docx>=0.8.11",
        "Pillow>=10.0.0",
    ]

    for package in required_packages:
        try:
            package_name = package.split(">=")[0]
            __import__(package_name)
            print(f"   ✅ {package_name}: 已安装")
        except ImportError:
            print(f"   ❌ {package_name}: 未安装，正在安装...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"   ✅ {package_name}: 安装成功")
            except subprocess.CalledProcessError:
                print(f"   ❌ {package_name}: 安装失败")


def create_test_pdf():
    """创建测试PDF文件"""
    print("\n🧪 创建测试PDF文件...")

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            test_pdf_path = os.path.join(temp_dir, "test.pdf")

            # 创建简单的PDF
            doc = SimpleDocTemplate(test_pdf_path, pagesize=A4)
            story = []

            styles = getSampleStyleSheet()
            story.append(Paragraph("测试PDF", styles["Heading1"]))
            story.append(Spacer(1, 20))
            story.append(
                Paragraph(
                    "这是一个测试PDF文件，用于验证PDF生成功能是否正常。",
                    styles["Normal"],
                )
            )

            doc.build(story)

            if os.path.exists(test_pdf_path) and os.path.getsize(test_pdf_path) > 0:
                print(f"   ✅ 测试PDF创建成功: {test_pdf_path}")
                print(f"   文件大小: {os.path.getsize(test_pdf_path)} 字节")
                return True
            else:
                print("   ❌ 测试PDF创建失败")
                return False

    except Exception as e:
        print(f"   ❌ 测试PDF创建失败: {e}")
        return False


def check_font_support():
    """检查字体支持"""
    print("\n🔤 检查字体支持...")

    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont

        # 测试基本字体
        basic_fonts = ["Helvetica", "Times", "Courier"]
        available_fonts = []

        for font_name in basic_fonts:
            try:
                pdfmetrics.registerFont(TTFont(font_name, font_name))
                available_fonts.append(font_name)
                print(f"   ✅ {font_name}: 可用")
            except Exception:
                print(f"   ❌ {font_name}: 不可用")

        if available_fonts:
            print(f"   📝 可用字体: {', '.join(available_fonts)}")
            return True
        else:
            print("   ⚠️ 没有可用的字体")
            return False

    except Exception as e:
        print(f"   ❌ 字体检查失败: {e}")
        return False


def check_permissions():
    """检查权限"""
    print("\n🔐 检查权限...")

    current_dir = os.getcwd()
    print(f"   当前目录: {current_dir}")

    # 检查读写权限
    can_write = os.access(current_dir, os.W_OK)
    can_read = os.access(current_dir, os.R_OK)

    print(f"   可写: {can_write}")
    print(f"   可读: {can_read}")

    if not can_write:
        print("   ⚠️ 当前目录没有写入权限，这可能导致PDF生成失败")
        return False

    # 测试文件创建
    test_file = os.path.join(current_dir, "test_permission.tmp")
    try:
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print("   ✅ 文件创建测试通过")
        return True
    except Exception as e:
        print(f"   ❌ 文件创建测试失败: {e}")
        return False


def create_output_directory():
    """创建输出目录"""
    print("\n📁 创建输出目录...")

    output_dirs = ["translated_pdfs", "output", "temp"]

    for dir_name in output_dirs:
        dir_path = os.path.join(os.getcwd(), dir_name)
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
                print(f"   ✅ 创建目录: {dir_path}")
            else:
                print(f"   📁 目录已存在: {dir_path}")
        except Exception as e:
            print(f"   ❌ 创建目录失败 {dir_path}: {e}")


def run_diagnostic():
    """运行诊断"""
    print("🔍 运行PDF对比功能诊断...")

    try:
        # 导入必要的模块
        from pdf_processor import PDFProcessor
        from pdf_translator import PDFTranslator

        processor = PDFProcessor()
        translator = PDFTranslator()

        print("   ✅ 模块导入成功")

        # 测试文本
        original_text = "Hello, this is a test."
        translated_text = "你好，这是一个测试。"

        # 创建临时目录进行测试
        with tempfile.TemporaryDirectory() as temp_dir:
            # 测试PDF生成
            pdf_path = os.path.join(temp_dir, "test_comparison.pdf")
            result = processor.create_comparison_pdf(
                original_text, translated_text, pdf_path, "测试对比"
            )

            if result["status"] == "success":
                print("   ✅ PDF对比生成测试通过")
                return True
            else:
                print(f"   ❌ PDF对比生成测试失败: {result.get('error', '未知错误')}")
                return False

    except Exception as e:
        print(f"   ❌ 诊断失败: {e}")
        return False


def main():
    """主函数"""
    print("🔧 PDF对比问题快速修复工具")
    print("=" * 50)

    # 检查并安装依赖
    check_and_install_dependencies()

    # 检查字体支持
    check_font_support()

    # 检查权限
    check_permissions()

    # 创建输出目录
    create_output_directory()

    # 创建测试PDF
    create_test_pdf()

    # 运行诊断
    diagnostic_result = run_diagnostic()

    print("\n" + "=" * 50)
    if diagnostic_result:
        print("🎉 修复完成！PDF对比功能应该可以正常工作了")
        print("\n💡 建议:")
        print("   1. 重新启动Streamlit应用")
        print("   2. 尝试上传PDF文件进行翻译")
        print("   3. 查看PDF对比显示是否正常")
    else:
        print("⚠️ 修复未完全成功，请检查错误信息")
        print("\n🔍 进一步诊断:")
        print("   1. 运行: python test_pdf_comparison.py")
        print("   2. 检查控制台错误日志")
        print("   3. 确保有足够的磁盘空间")

    print("\n📖 如果问题仍然存在，请:")
    print("   1. 检查系统字体配置")
    print("   2. 确保Python环境正确")
    print("   3. 尝试在不同的目录中运行应用")


if __name__ == "__main__":
    main()
