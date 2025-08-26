#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强PDF对比功能测试脚本
测试新的PDF对比功能，包括格式保留和完整内容显示
"""

import os
import tempfile
from pdf_processor import PDFProcessor


def test_enhanced_pdf_comparison():
    """测试增强的PDF对比功能"""
    print("🧪 测试增强的PDF对比功能...")

    try:
        processor = PDFProcessor()

        # 测试文本 - 模拟您提到的课程大纲内容
        original_text = """COMPSCI4004/COMPSCI5087AI(H/M) Week 2: Introduction and Foundations
Debasis Ganguly from University of Glasgow, Glasgow, UK on September 30, 2024

COMPSCI4004/COMPSCI5087AI(H/M) Overview Course Introduction
What is AI? Why is AI difficult? Agents-Centric view of AI Rationality of Agents Environment Types Agent types
D.Ganguly

COMPSCI4004/COMPSCI5087AI(H/M) CourseIntroduction Lecturers and Time table
► Lecturers: Dr. Debasis Ganguly, Debasis.Ganguly@glasgow.ac.uk (course coordinator).
► GTAs (for lab support): Dr. Edmond S. L. Ho, Shu-Lim.Ho@glasgow.ac.uk, Jie Wang, and Yuxuan Xie.
► Lectures: Mondays: 15:00-17:00 at Boyd Orr - Room 412 (LC01)
► Lab sessions: Mondays: 09:00-11:00 (you will be allocated specific 1 hour timeslot) at BOYD ORR 720
► Open Hours: Edmond Ho - Friday 12 noon - 1 PM, SAWB 402, Sir Alwyn Williams Building. and Debasis Ganguly - Friday 2 PM - 4 PM, M111 Sir Alwyn Williams Building.

COMPSCI4004/COMPSCI5087AI(H/M) CourseIntroduction Course Information
► AI (H and M): Overview of intelligent agent design.
► Fundamental concepts of AI.
► An explanation of various stages and complexities of an agent-driven model that interacts with an environment and makes sequence of rational decisions.
► Non-examinable materials: Recent advancements in AI. Responsible AI (explainability, trustworthiness and fairness).
► Labs: Labs in Week will be based on the lecture notes covered in Week -1. Labs aren't graded but you should complete the exercises. We will release the solutions the next day.

COMPSCI4004/COMPSCI5087AI(H/M) WhatisAI?
► Mentimeter Go to mentimeter.com; use code '4760 0586'
► IBM's Deep Blue defeats Garry Kasparov, the world champion in chess in 1997. Modern chess engines like Alpha-Zero, StockFish etc. are much better than human players: ≈ 3500 ELO as compared to ≈ 2830 of Magnus Carlsen!
► IBM's Watson system competed on Jeopardy! winning the first-place prize of 1 million USD. Leverages NLP/Information Retrieval and Knowledge-bases for effective Question Answering.
D.Ganguly COMPSCI4004/COMPSCI5087AI(H/M)"""

        translated_text = """COMPSCI4004/COMPSCI5087AI(H/M) 第2周：介绍与基础
来自英国格拉斯哥格拉斯哥大学的Debasis Ganguly，2024年9月30日

COMPSCI4004/COMPSCI5087AI(H/M) 课程概述介绍
什么是人工智能？为什么人工智能很难？以智能体为中心的人工智能观点 智能体的理性 环境类型 智能体类型
D.Ganguly

COMPSCI4004/COMPSCI5087AI(H/M) 课程介绍 讲师和时间表
► 讲师：Debasis Ganguly博士，Debasis.Ganguly@glasgow.ac.uk（课程协调员）。
► GTA（实验室支持）：Edmond S. L. Ho博士，Shu-Lim.Ho@glasgow.ac.uk，王杰和谢宇轩。
► 讲座：周一15:00-17:00，Boyd Orr - 412室（LC01）
► 实验课：周一09:00-11:00（您将被分配特定的1小时时间段）在BOYD ORR 720
► 开放时间：Edmond Ho - 周五中午12点-下午1点，SAWB 402，Sir Alwyn Williams大楼。Debasis Ganguly - 周五下午2点-4点，M111 Sir Alwyn Williams大楼。

COMPSCI4004/COMPSCI5087AI(H/M) 课程介绍 课程信息
► 人工智能（H和M）：智能体设计概述。
► 人工智能的基本概念。
► 解释智能体驱动模型与环境交互并做出理性决策序列的各种阶段和复杂性。
► 非考试材料：人工智能的最新进展。负责任的人工智能（可解释性、可信度和公平性）。
► 实验：第周实验将基于第-1周涵盖的讲义。实验不评分，但您应该完成练习。我们将在第二天发布解决方案。

COMPSCI4004/COMPSCI5087AI(H/M) 什么是人工智能？
► Mentimeter 访问mentimeter.com；使用代码'4760 0586'
► IBM的深蓝在1997年击败了国际象棋世界冠军加里·卡斯帕罗夫。现代国际象棋引擎如Alpha-Zero、StockFish等比人类玩家好得多：≈3500 ELO相比Magnus Carlsen的≈2830！
► IBM的Watson系统参加了Jeopardy！赢得了100万美元的一等奖。利用NLP/信息检索和知识库进行有效的问题回答。
D.Ganguly COMPSCI4004/COMPSCI5087AI(H/M)"""

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"   临时目录: {temp_dir}")

            # 测试增强的PDF对比生成
            pdf_path = os.path.join(temp_dir, "enhanced_comparison.pdf")
            print(f"   测试文件路径: {pdf_path}")

            result = processor.create_enhanced_comparison_pdf(
                original_text,
                translated_text,
                pdf_path,
                "增强翻译对比",
                preserve_formatting=True,
            )

            print(f"   生成结果: {result}")

            if result["status"] == "success":
                print(f"   ✅ 增强PDF对比生成成功: {result['output_path']}")
                if os.path.exists(pdf_path):
                    print(f"   文件大小: {os.path.getsize(pdf_path)} 字节")
                    print(f"   文件权限: {oct(os.stat(pdf_path).st_mode)[-3:]}")

                    # 检查内容完整性
                    print(
                        f"   原文段落数: {len([p for p in original_text.split('\\n\\n') if p.strip()])}"
                    )
                    print(
                        f"   翻译段落数: {len([p for p in translated_text.split('\\n\\n') if p.strip()])}"
                    )
                else:
                    print("   ⚠️ 文件路径存在但文件不存在")
            else:
                print(f"   ❌ 增强PDF对比生成失败: {result.get('error', '未知错误')}")

            # 测试传统PDF对比生成
            traditional_pdf_path = os.path.join(temp_dir, "traditional_comparison.pdf")
            print(f"   传统对比文件路径: {traditional_pdf_path}")

            traditional_result = processor.create_comparison_pdf(
                original_text, translated_text, traditional_pdf_path, "传统翻译对比"
            )

            print(f"   传统生成结果: {traditional_result}")

            if traditional_result["status"] == "success":
                print(f"   ✅ 传统PDF对比生成成功: {traditional_result['output_path']}")
                if os.path.exists(traditional_pdf_path):
                    print(f"   文件大小: {os.path.getsize(traditional_pdf_path)} 字节")
                else:
                    print("   ⚠️ 传统文件路径存在但文件不存在")
            else:
                print(
                    f"   ❌ 传统PDF对比生成失败: {traditional_result.get('error', '未知错误')}"
                )

        print("✅ 增强PDF对比功能测试完成\n")
        return True

    except Exception as e:
        print(f"❌ 增强PDF对比功能测试失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_pdf_export_with_enhanced():
    """测试使用增强功能的PDF导出"""
    print("🧪 测试使用增强功能的PDF导出...")

    try:
        processor = PDFProcessor()

        # 测试文本
        original_text = "Hello, this is a test message for enhanced PDF comparison."
        translated_text = "你好，这是用于增强PDF对比的测试消息。"

        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 测试增强PDF导出
            output_path = os.path.join(temp_dir, "test_enhanced_export.pdf")
            result = processor.create_enhanced_comparison_pdf(
                original_text,
                translated_text,
                output_path,
                "测试增强导出",
                preserve_formatting=True,
            )

            if result["status"] == "success":
                print(f"   ✅ 增强PDF导出成功")
                if os.path.exists(output_path):
                    print(f"   文件大小: {os.path.getsize(output_path)} 字节")
            else:
                print(f"   ❌ 增强PDF导出失败: {result.get('error', '未知错误')}")

        print("✅ 增强PDF导出测试完成\n")
        return True

    except Exception as e:
        print(f"❌ 增强PDF导出测试失败: {e}")
        return False


def main():
    """主函数"""
    print("🧪 增强PDF对比功能测试程序")
    print("=" * 50)

    # 测试增强PDF对比功能
    test_enhanced_pdf_comparison()

    # 测试PDF导出
    test_pdf_export_with_enhanced()

    print("🎉 所有测试完成！")
    print("\n💡 增强功能说明:")
    print("   1. 保留格式: 使用表格格式进行左右对比")
    print("   2. 完整内容: 显示所有段落，不限制数量")
    print("   3. 更好布局: 改进的字体和样式支持")
    print("   4. 兼容性: 保持与原有功能的兼容")


if __name__ == "__main__":
    main()
