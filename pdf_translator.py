#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF翻译器
整合PDF处理和翻译功能的完整解决方案
"""

import os
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from pdf_processor import PDFProcessor
from agent import TranslationAgent


class PDFTranslator:
    """PDF翻译器主类"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化PDF翻译器

        Args:
            api_key: 阿里云API密钥
        """
        self.pdf_processor = PDFProcessor()
        self.translation_agent = TranslationAgent(api_key)

        # 翻译配置
        self.chunk_size = 1000  # 文本块大小
        self.delay_between_chunks = 1  # 块间延迟（秒）
        self.max_retries = 3  # 最大重试次数

    def translate_pdf_file(
        self, pdf_path: str, context: str = "", output_dir: str = "translated_pdfs"
    ) -> Dict[str, any]:
        """
        翻译整个PDF文件

        Args:
            pdf_path: PDF文件路径
            context: 文档类型或上下文信息
            output_dir: 输出目录

        Returns:
            翻译结果字典
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(pdf_path):
                return {"status": "error", "error": f"文件不存在: {pdf_path}"}

            # 获取PDF信息
            pdf_info = self.pdf_processor.get_pdf_info(pdf_path)
            if pdf_info.get("status") == "error":
                return pdf_info

            # 检查是否为扫描版PDF
            is_scanned = self.pdf_processor.is_scanned_pdf(pdf_path)
            if is_scanned:
                return {
                    "status": "warning",
                    "message": "检测到扫描版PDF，无法提取文本进行翻译",
                    "suggestion": "请使用OCR工具先将扫描版PDF转换为可编辑文本",
                }

            # 提取PDF文本
            print(f"正在提取PDF文本: {pdf_path}")
            extraction_result = self.pdf_processor.extract_text_from_pdf(pdf_path)

            if extraction_result["status"] != "success":
                return extraction_result

            # 分割文本为可翻译的块
            text = extraction_result["total_text"]
            text_chunks = self.pdf_processor.split_text_for_translation(
                text, self.chunk_size
            )

            print(f"文本已分割为 {len(text_chunks)} 个块")

            # 翻译文本块
            print("开始翻译...")
            translation_results = self.translate_pdf_chunks_with_progress(
                text_chunks, context
            )

            # 检查翻译结果
            failed_chunks = [r for r in translation_results if r["status"] != "success"]
            if failed_chunks:
                print(f"警告: {len(failed_chunks)} 个文本块翻译失败")

            # 合并翻译结果
            original_text = text
            translated_text = self._merge_translation_results(translation_results)

            # 导出结果
            output_filename = f"translated_{Path(pdf_path).stem}"
            export_result = self._export_translation_results(
                original_text, translated_text, output_dir, output_filename
            )

            return {
                "status": "success",
                "pdf_info": pdf_info,
                "extraction_result": extraction_result,
                "translation_results": translation_results,
                "total_chunks": len(text_chunks),
                "successful_chunks": len(translation_results) - len(failed_chunks),
                "failed_chunks": len(failed_chunks),
                "export_result": export_result,
                "original_text": original_text,
                "translated_text": translated_text,
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "file_path": pdf_path}

    def translate_pdf_chunks_with_progress(
        self, text_chunks: List[str], context: str = ""
    ) -> List[Dict[str, str]]:
        """
        翻译PDF文本块，带进度显示

        Args:
            text_chunks: 文本块列表
            context: 文档类型或上下文信息

        Returns:
            翻译结果列表
        """
        results = []
        total_chunks = len(text_chunks)

        for i, chunk in enumerate(text_chunks, 1):
            print(f"正在翻译第 {i}/{total_chunks} 个文本块...")

            # 翻译当前块
            result = self._translate_chunk_with_retry(chunk, context, i, total_chunks)
            results.append(result)

            # 显示进度
            progress = self.translation_agent.get_translation_progress(i, total_chunks)
            print(f"进度: {progress['percentage']}% ({i}/{total_chunks})")

            # 块间延迟，避免API限制
            if i < total_chunks:
                time.sleep(self.delay_between_chunks)

        return results

    def _translate_chunk_with_retry(
        self, chunk: str, context: str, chunk_index: int, total_chunks: int
    ) -> Dict[str, str]:
        """
        翻译单个文本块，带重试机制

        Args:
            chunk: 文本块
            context: 文档类型或上下文信息
            chunk_index: 块索引
            total_chunks: 总块数

        Returns:
            翻译结果
        """
        for attempt in range(self.max_retries):
            try:
                result = self.translation_agent.translate_pdf_content(chunk, context)
                result["chunk_index"] = chunk_index
                result["total_chunks"] = total_chunks
                result["attempt"] = attempt + 1

                if result["status"] == "success":
                    return result
                else:
                    print(
                        f"第 {attempt + 1} 次尝试失败: {result.get('error', '未知错误')}"
                    )

            except Exception as e:
                print(f"第 {attempt + 1} 次尝试异常: {str(e)}")

            # 重试前等待
            if attempt < self.max_retries - 1:
                time.sleep(2**attempt)  # 指数退避

        # 所有重试都失败
        return {
            "original": chunk,
            "translation": f"[翻译失败 - 块 {chunk_index}]",
            "status": "error",
            "error": f"经过 {self.max_retries} 次尝试后仍然失败",
            "chunk_index": chunk_index,
            "total_chunks": total_chunks,
        }

    def _merge_translation_results(
        self, translation_results: List[Dict[str, str]]
    ) -> str:
        """
        合并翻译结果

        Args:
            translation_results: 翻译结果列表

        Returns:
            合并后的翻译文本
        """
        merged_text = ""

        for i, result in enumerate(translation_results):
            if result["status"] == "success":
                if i > 0:
                    merged_text += "\n\n"
                merged_text += result["translation"]
            else:
                # 对于失败的块，保留原文
                if i > 0:
                    merged_text += "\n\n"
                merged_text += f"[原文 - 块 {result.get('chunk_index', i+1)}]:\n{result['original']}"

        return merged_text

    def _export_translation_results(
        self, original_text: str, translated_text: str, output_dir: str, filename: str
    ) -> Dict[str, str]:
        """
        导出翻译结果

        Args:
            original_text: 原文
            translated_text: 翻译文本
            output_dir: 输出目录
            filename: 文件名（不含扩展名）

        Returns:
            导出结果
        """
        try:
            # 创建输出目录
            os.makedirs(output_dir, exist_ok=True)

            # 导出为不同格式
            export_results = {}

            # TXT格式
            txt_path = os.path.join(output_dir, f"{filename}.txt")
            txt_result = self.pdf_processor.export_translation_result(
                original_text, translated_text, txt_path, "txt"
            )
            export_results["txt"] = txt_result

            # DOCX格式
            docx_path = os.path.join(output_dir, f"{filename}.docx")
            docx_result = self.pdf_processor.export_translation_result(
                original_text, translated_text, docx_path, "docx"
            )
            export_results["docx"] = docx_result

            # PDF对比格式
            pdf_path = os.path.join(output_dir, f"{filename}_comparison.pdf")
            pdf_result = self.pdf_processor.export_translation_result(
                original_text, translated_text, pdf_path, "pdf"
            )
            export_results["pdf"] = pdf_result

            return {
                "status": "success",
                "output_directory": output_dir,
                "formats": export_results,
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def create_side_by_side_pdf(
        self,
        original_text: str,
        translated_text: str,
        output_path: str,
        title: str = "翻译对比",
    ) -> Dict[str, str]:
        """
        创建左右对比的PDF文档

        Args:
            original_text: 原文
            translated_text: 翻译文本
            output_path: 输出PDF路径
            title: PDF标题

        Returns:
            创建结果
        """
        try:
            from reportlab.lib.pagesizes import A4, landscape
            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                Table,
                TableStyle,
            )
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont

            # 尝试注册中文字体
            try:
                # 对于Windows系统
                pdfmetrics.registerFont(TTFont("SimSun", "C:/Windows/Fonts/simsun.ttc"))
                chinese_font = "SimSun"
            except:
                try:
                    # 对于macOS系统
                    pdfmetrics.registerFont(
                        TTFont("PingFang", "/System/Library/Fonts/PingFang.ttc")
                    )
                    chinese_font = "PingFang"
                except:
                    try:
                        # 对于Linux系统
                        pdfmetrics.registerFont(
                            TTFont(
                                "DejaVuSans",
                                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                            )
                        )
                        chinese_font = "DejaVuSans"
                    except:
                        chinese_font = "Helvetica"  # 默认字体

            # 创建横向PDF文档
            doc = SimpleDocTemplate(output_path, pagesize=landscape(A4))
            story = []

            # 定义样式
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=16,
                spaceAfter=20,
                alignment=1,  # 居中
                fontName=chinese_font,
            )

            subtitle_style = ParagraphStyle(
                "CustomSubtitle",
                parent=styles["Heading2"],
                fontSize=12,
                spaceAfter=15,
                fontName=chinese_font,
            )

            content_style = ParagraphStyle(
                "CustomContent",
                parent=styles["Normal"],
                fontSize=9,
                spaceAfter=8,
                fontName=chinese_font,
                leading=12,
            )

            # 添加标题
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 15))

            # 分割文本为段落
            original_paragraphs = [
                p.strip() for p in original_text.split("\n\n") if p.strip()
            ]
            translated_paragraphs = [
                p.strip() for p in translated_text.split("\n\n") if p.strip()
            ]

            # 确保两个列表长度一致
            max_paragraphs = max(len(original_paragraphs), len(translated_paragraphs))
            original_paragraphs.extend(
                [""] * (max_paragraphs - len(original_paragraphs))
            )
            translated_paragraphs.extend(
                [""] * (max_paragraphs - len(translated_paragraphs))
            )

            # 限制段落数量避免过长
            max_display = min(max_paragraphs, 15)

            # 创建对比表格
            table_data = []

            # 添加表头
            table_data.append(
                [
                    Paragraph("原文 (Original)", subtitle_style),
                    Paragraph("翻译 (Translation)", subtitle_style),
                ]
            )

            # 添加内容行
            for i in range(max_display):
                original_para = (
                    original_paragraphs[i] if i < len(original_paragraphs) else ""
                )
                translated_para = (
                    translated_paragraphs[i] if i < len(translated_paragraphs) else ""
                )

                table_data.append(
                    [
                        Paragraph(original_para, content_style),
                        Paragraph(translated_para, content_style),
                    ]
                )

            # 创建表格
            table = Table(
                table_data, colWidths=[doc.width / 2 - 20, doc.width / 2 - 20]
            )

            # 设置表格样式
            table.setStyle(
                TableStyle(
                    [
                        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("FONTNAME", (0, 0), (-1, 0), chinese_font),  # 表头字体
                        ("FONTSIZE", (0, 0), (-1, 0), 12),  # 表头字号
                        ("FONTNAME", (0, 1), (-1, -1), chinese_font),  # 内容字体
                        ("FONTSIZE", (0, 1), (-1, -1), 9),  # 内容字号
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ("TOPPADDING", (0, 0), (-1, -1), 6),
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ]
                )
            )

            story.append(table)

            # 如果内容被截断，添加提示
            if max_paragraphs > max_display:
                story.append(Spacer(1, 15))
                story.append(
                    Paragraph(
                        f"... (显示前{max_display}段，共{max_paragraphs}段，完整内容请查看完整PDF)",
                        content_style,
                    )
                )

            # 生成PDF
            doc.build(story)

            return {"status": "success", "output_path": output_path, "format": "pdf"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_translation_summary(
        self, translation_results: List[Dict[str, str]]
    ) -> Dict[str, any]:
        """
        获取翻译摘要信息

        Args:
            translation_results: 翻译结果列表

        Returns:
            摘要信息字典
        """
        total_chunks = len(translation_results)
        successful_chunks = len(
            [r for r in translation_results if r["status"] == "success"]
        )
        failed_chunks = total_chunks - successful_chunks

        # 计算总字符数和词数
        total_original_chars = sum(
            len(r.get("original", "")) for r in translation_results
        )
        total_translated_chars = sum(
            len(r.get("translation", ""))
            for r in translation_results
            if r["status"] == "success"
        )

        return {
            "total_chunks": total_chunks,
            "successful_chunks": successful_chunks,
            "failed_chunks": failed_chunks,
            "success_rate": (
                round((successful_chunks / total_chunks) * 100, 2)
                if total_chunks > 0
                else 0
            ),
            "total_original_chars": total_original_chars,
            "total_translated_chars": total_translated_chars,
            "average_chars_per_chunk": (
                round(total_original_chars / total_chunks, 2) if total_chunks > 0 else 0
            ),
        }

    def set_translation_config(
        self, chunk_size: int = None, delay: float = None, max_retries: int = None
    ):
        """
        设置翻译配置参数

        Args:
            chunk_size: 文本块大小
            delay: 块间延迟（秒）
            max_retries: 最大重试次数
        """
        if chunk_size is not None:
            self.chunk_size = chunk_size
        if delay is not None:
            self.delay_between_chunks = delay
        if max_retries is not None:
            self.max_retries = max_retries


# 使用示例
if __name__ == "__main__":
    # 创建PDF翻译器实例
    try:
        translator = PDFTranslator()

        # 设置配置
        translator.set_translation_config(chunk_size=800, delay=1.5, max_retries=2)

        # 翻译PDF文件
        pdf_path = "example.pdf"  # 替换为实际的PDF文件路径
        if os.path.exists(pdf_path):
            result = translator.translate_pdf_file(pdf_path, context="技术文档")

            if result["status"] == "success":
                print("✅ PDF翻译完成！")
                summary = translator.get_translation_summary(
                    result["translation_results"]
                )
                print(f"翻译摘要: {summary}")
            else:
                print(f"❌ 翻译失败: {result.get('error', '未知错误')}")
        else:
            print(f"PDF文件不存在: {pdf_path}")

    except Exception as e:
        print(f"初始化失败: {e}")
        print("请确保设置了DASHSCOPE_API_KEY环境变量")
