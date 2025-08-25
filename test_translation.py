#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
翻译Agent测试脚本
用于测试TranslationAgent的各项功能
"""

import os
from dotenv import load_dotenv
from agent import TranslationAgent


def test_translation_agent():
    """测试翻译Agent的基本功能"""

    # 加载环境变量
    load_dotenv()

    # 获取API密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 错误: 未设置DASHSCOPE_API_KEY环境变量")
        print("请设置环境变量或在.env文件中配置")
        return False

    try:
        # 创建翻译agent
        print("🚀 正在初始化翻译Agent...")
        agent = TranslationAgent(api_key)
        print("✅ 翻译Agent初始化成功")

        # 测试用例
        test_cases = [
            "Hello, how are you today?",
            "The quick brown fox jumps over the lazy dog.",
            "Machine learning is a subset of artificial intelligence.",
            "Please provide your feedback on this product.",
        ]

        print("\n" + "=" * 50)
        print("🔤 开始测试翻译功能")
        print("=" * 50)

        # 测试单句翻译
        for i, text in enumerate(test_cases, 1):
            print(f"\n📝 测试用例 {i}: {text}")

            # 语言检测
            detected_lang = agent.detect_language(text)
            print(f"🔍 检测到的语言: {detected_lang}")

            # 执行翻译
            result = agent.translate_to_chinese(text)

            if result["status"] == "success":
                print(f"✅ 翻译成功: {result['translation']}")
            else:
                print(f"❌ 翻译失败: {result.get('error', '未知错误')}")

        print("\n" + "=" * 50)
        print("📄 测试批量翻译功能")
        print("=" * 50)

        # 测试批量翻译
        batch_results = agent.batch_translate(test_cases)
        print(f"📊 批量翻译完成，共 {len(batch_results)} 句")

        for i, result in enumerate(batch_results, 1):
            if result["status"] == "success":
                print(f"✅ 第{i}句: {result['translation']}")
            else:
                print(f"❌ 第{i}句失败: {result.get('error', '未知错误')}")

        print("\n" + "=" * 50)
        print("📖 测试术语表翻译功能")
        print("=" * 50)

        # 测试术语表翻译
        glossary = {
            "API": "应用程序接口",
            "SDK": "软件开发工具包",
            "UI": "用户界面",
            "UX": "用户体验",
        }

        tech_text = (
            "This API provides SDK functionality with improved UI and UX design."
        )
        print(f"🔧 技术文本: {tech_text}")
        print(f"📚 术语表: {glossary}")

        glossary_result = agent.translate_with_glossary(tech_text, glossary)

        if glossary_result["status"] == "success":
            print(f"✅ 术语表翻译成功: {glossary_result['translation']}")
        else:
            print(f"❌ 术语表翻译失败: {glossary_result.get('error', '未知错误')}")

        print("\n" + "=" * 50)
        print("🎉 所有测试完成！")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"❌ 测试过程中出现错误: {str(e)}")
        return False


def test_model_parameters():
    """测试不同的模型参数"""

    load_dotenv()
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 错误: 未设置DASHSCOPE_API_KEY环境变量")
        return False

    try:
        print("\n" + "=" * 50)
        print("🎛️ 测试不同模型参数")
        print("=" * 50)

        # 测试不同模型
        models = ["qwen-max", "qwen-plus", "qwen-turbo"]
        test_text = "Artificial intelligence is transforming the world."

        for model in models:
            print(f"\n🤖 测试模型: {model}")

            agent = TranslationAgent(api_key)
            agent.model = model

            result = agent.translate_to_chinese(test_text)

            if result["status"] == "success":
                print(f"✅ 翻译结果: {result['translation']}")
            else:
                print(f"❌ 翻译失败: {result.get('error', '未知错误')}")

        return True

    except Exception as e:
        print(f"❌ 模型参数测试失败: {str(e)}")
        return False


if __name__ == "__main__":
    print("🌐 英语翻译Agent测试程序")
    print("=" * 50)

    # 运行基本功能测试
    if test_translation_agent():
        print("\n✅ 基本功能测试通过")
    else:
        print("\n❌ 基本功能测试失败")

    # 运行模型参数测试
    if test_model_parameters():
        print("\n✅ 模型参数测试通过")
    else:
        print("\n❌ 模型参数测试失败")

    print("\n📖 测试完成！如有问题请检查:")
    print("1. API密钥是否正确")
    print("2. 网络连接是否正常")
    print("3. 依赖包是否正确安装")
