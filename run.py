#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语翻译Agent启动脚本
"""

import os
import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """检查依赖是否安装"""
    try:
        import streamlit
        import dashscope
        import dotenv

        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        return False


def check_api_key():
    """检查API密钥是否配置"""
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("⚠️  警告: 未设置DASHSCOPE_API_KEY环境变量")
        print("请在.env文件中配置或设置环境变量")
        return False
    return True


def main():
    """主函数"""
    print("🌐 英语翻译Agent启动程序")
    print("=" * 40)

    # 检查依赖
    if not check_dependencies():
        print("\n📦 正在安装依赖...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
            )
            print("✅ 依赖安装完成")
        except subprocess.CalledProcessError:
            print("❌ 依赖安装失败，请手动运行: pip install -r requirements.txt")
            return

    # 检查API密钥
    if not check_api_key():
        print("\n📝 请按以下步骤配置API密钥:")
        print("1. 访问 https://dashscope.aliyun.com/ 获取API密钥")
        print("2. 在项目根目录创建.env文件")
        print("3. 在.env文件中添加: DASHSCOPE_API_KEY=your_key_here")
        print("\n或者直接设置环境变量:")
        print("export DASHSCOPE_API_KEY=your_key_here")

        # 询问是否继续
        choice = input("\n是否继续启动应用? (y/n): ").lower().strip()
        if choice != "y":
            return

    # 启动应用
    print("\n🚀 正在启动Streamlit应用...")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")


if __name__ == "__main__":
    main()
