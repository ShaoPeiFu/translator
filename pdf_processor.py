#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF处理模块
支持PDF文本提取、翻译和导出功能
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import PyPDF2
import pdfplumber
from PIL import Image
import io
import base64


class PDFProcessor:
    """PDF文档处理器"""

    def __init__(self):
        """初始化PDF处理器"""
        self.supported_formats = [".pdf", ".docx", ".txt"]

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[str, any]:
        """
        从PDF文件提取文本

        Args:
            pdf_path: PDF文件路径

        Returns:
            包含提取结果的字典
        """
        try:
            text_content = []
            page_info = []

            # 使用pdfplumber提取文本（更好的文本保持）
            with pdfplumber.open(pdf_path) as pdf:
                total_pages = len(pdf.pages)

                for page_num, page in enumerate(pdf.pages, 1):
                    # 提取文本
                    text = page.extract_text()
                    if text:
                        # 清理文本
                        cleaned_text = self._clean_text(text)
                        text_content.append(cleaned_text)

                        page_info.append(
                            {
                                "page": page_num,
                                "text": cleaned_text,
                                "char_count": len(cleaned_text),
                                "word_count": len(cleaned_text.split()),
                            }
                        )
                    else:
                        # 如果无法提取文本，可能是扫描版PDF
                        text_content.append(
                            f"[第{page_num}页 - 无法提取文本，可能是扫描版PDF]"
                        )
                        page_info.append(
                            {
                                "page": page_num,
                                "text": "",
                                "char_count": 0,
                                "word_count": 0,
                                "note": "可能是扫描版PDF",
                            }
                        )

            return {
                "status": "success",
                "total_pages": total_pages,
                "total_text": "\n\n".join(text_content),
                "page_info": page_info,
                "file_path": pdf_path,
                "file_name": os.path.basename(pdf_path),
            }

        except Exception as e:
            return {"status": "error", "error": str(e), "file_path": pdf_path}

    def _clean_text(self, text: str) -> str:
        """
        清理提取的文本

        Args:
            text: 原始文本

        Returns:
            清理后的文本
        """
        if not text:
            return ""

        # 移除多余的空白字符
        text = re.sub(r"\s+", " ", text)

        # 移除页眉页脚（通常包含页码等）
        text = re.sub(r"^\s*\d+\s*$", "", text, flags=re.MULTILINE)

        # 移除孤立的字符
        text = re.sub(r"\s+[a-zA-Z]\s+", " ", text)

        # 清理段落分隔
        text = re.sub(r"\n\s*\n", "\n\n", text)

        return text.strip()

    def split_text_for_translation(
        self, text: str, max_chunk_size: int = 1000
    ) -> List[str]:
        """
        将长文本分割成适合翻译的块

        Args:
            text: 要分割的文本
            max_chunk_size: 每个块的最大字符数

        Returns:
            文本块列表
        """
        if len(text) <= max_chunk_size:
            return [text]

        chunks = []
        sentences = re.split(r"[.!?。！？]\s*", text)

        current_chunk = ""
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # 如果当前块加上新句子超过限制，保存当前块并开始新块
            if len(current_chunk) + len(sentence) > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += ". " + sentence
                else:
                    current_chunk = sentence

        # 添加最后一个块
        if current_chunk:
            chunks.append(current_chunk.strip())

        return chunks

    def merge_translated_chunks(
        self, original_chunks: List[str], translated_chunks: List[str]
    ) -> str:
        """
        合并翻译后的文本块

        Args:
            original_chunks: 原始文本块列表
            translated_chunks: 翻译后的文本块列表

        Returns:
            合并后的完整翻译文本
        """
        if len(original_chunks) != len(translated_chunks):
            return "翻译块数量不匹配，请检查翻译结果"

        merged_text = ""
        for i, (orig, trans) in enumerate(zip(original_chunks, translated_chunks)):
            if i > 0:
                merged_text += "\n\n"
            merged_text += f"原文 (块 {i+1}):\n{orig}\n\n翻译:\n{trans}"

        return merged_text

    def create_comparison_pdf(
        self,
        original_text: str,
        translated_text: str,
        output_path: str,
        title: str = "翻译对比",
    ) -> Dict[str, str]:
        """
        创建原文和翻译的对比PDF

        Args:
            original_text: 原文
            translated_text: 翻译文本
            output_path: 输出PDF路径
            title: PDF标题

        Returns:
            创建结果
        """
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                PageBreak,
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

            # 创建PDF文档
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []

            # 定义样式
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "CustomTitle",
                parent=styles["Heading1"],
                fontSize=18,
                spaceAfter=30,
                alignment=1,  # 居中
                fontName=chinese_font,
            )

            subtitle_style = ParagraphStyle(
                "CustomSubtitle",
                parent=styles["Heading2"],
                fontSize=14,
                spaceAfter=20,
                fontName=chinese_font,
            )

            content_style = ParagraphStyle(
                "CustomContent",
                parent=styles["Normal"],
                fontSize=10,
                spaceAfter=12,
                fontName=chinese_font,
                leading=14,
            )

            # 添加标题
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))

            # 添加原文
            story.append(Paragraph("原文 (Original Text)", subtitle_style))
            story.append(Spacer(1, 10))

            # 处理原文，分段显示
            original_paragraphs = original_text.split("\n\n")
            for para in original_paragraphs[:10]:  # 限制段落数量避免过长
                if para.strip():
                    story.append(Paragraph(para.strip(), content_style))
                    story.append(Spacer(1, 8))

            if len(original_paragraphs) > 10:
                story.append(Paragraph("... (更多内容请查看完整PDF)", content_style))

            story.append(PageBreak())

            # 添加翻译
            story.append(Paragraph("翻译 (Translation)", subtitle_style))
            story.append(Spacer(1, 10))

            # 处理翻译文本，分段显示
            translated_paragraphs = translated_text.split("\n\n")
            for para in translated_paragraphs[:10]:  # 限制段落数量避免过长
                if para.strip():
                    story.append(Paragraph(para.strip(), content_style))
                    story.append(Spacer(1, 8))

            if len(translated_paragraphs) > 10:
                story.append(Paragraph("... (更多内容请查看完整PDF)", content_style))

            # 生成PDF
            doc.build(story)

            return {"status": "success", "output_path": output_path, "format": "pdf"}

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def export_translation_result(
        self,
        original_text: str,
        translated_text: str,
        output_path: str,
        format_type: str = "txt",
    ) -> Dict[str, str]:
        """
        导出翻译结果

        Args:
            original_text: 原文
            translated_text: 翻译文本
            output_path: 输出文件路径
            format_type: 输出格式 ('txt', 'docx', 'json', 'pdf')

        Returns:
            导出结果
        """
        try:
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if format_type == "txt":
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write("=== 原文 ===\n")
                    f.write(original_text)
                    f.write("\n\n=== 翻译 ===\n")
                    f.write(translated_text)

            elif format_type == "json":
                import json

                result_data = {
                    "original_text": original_text,
                    "translated_text": translated_text,
                    "timestamp": str(pd.Timestamp.now()),
                    "language": "en_to_zh",
                }
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(result_data, f, ensure_ascii=False, indent=2)

            elif format_type == "docx":
                from docx import Document

                doc = Document()
                doc.add_heading("翻译结果", 0)

                doc.add_heading("原文", level=1)
                doc.add_paragraph(original_text)

                doc.add_heading("翻译", level=1)
                doc.add_paragraph(translated_text)

                doc.save(output_path)

            elif format_type == "pdf":
                # 使用新的对比PDF生成方法
                return self.create_comparison_pdf(
                    original_text, translated_text, output_path
                )

            return {
                "status": "success",
                "output_path": output_path,
                "format": format_type,
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_pdf_info(self, pdf_path: str) -> Dict[str, any]:
        """
        获取PDF文件信息

        Args:
            pdf_path: PDF文件路径

        Returns:
            PDF信息字典
        """
        try:
            with open(pdf_path, "rb") as file:
                pdf_reader = PyPDF2.PdfReader(file)

                info = {
                    "file_path": pdf_path,
                    "file_name": os.path.basename(pdf_path),
                    "total_pages": len(pdf_reader.pages),
                    "file_size": os.path.getsize(pdf_path),
                    "file_size_mb": round(os.path.getsize(pdf_path) / (1024 * 1024), 2),
                }

                # 尝试获取PDF元数据
                if pdf_reader.metadata:
                    info["title"] = pdf_reader.metadata.get("/Title", "未知")
                    info["author"] = pdf_reader.metadata.get("/Author", "未知")
                    info["subject"] = pdf_reader.metadata.get("/Subject", "未知")
                    info["creator"] = pdf_reader.metadata.get("/Creator", "未知")

                return info

        except Exception as e:
            return {"status": "error", "error": str(e), "file_path": pdf_path}

    def is_scanned_pdf(self, pdf_path: str) -> bool:
        """
        判断是否为扫描版PDF

        Args:
            pdf_path: PDF文件路径

        Returns:
            是否为扫描版PDF
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                # 检查前几页的文本提取情况
                text_count = 0
                for i in range(min(3, len(pdf.pages))):
                    text = pdf.pages[i].extract_text()
                    if text and len(text.strip()) > 50:  # 如果提取到足够多的文本
                        text_count += 1

                # 如果大部分页面都无法提取到足够文本，可能是扫描版
                return text_count < 2

        except Exception:
            return True

        return False
