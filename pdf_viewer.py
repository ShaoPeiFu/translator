#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF查看器组件
支持在Streamlit页面上显示PDF文档
"""

import streamlit as st
import base64
import os
from typing import Optional, Dict, Any


class PDFViewer:
    """PDF查看器类"""

    @staticmethod
    def display_pdf(pdf_path: str, width: int = 100, height: int = 600) -> bool:
        """
        在页面上显示PDF文档

        Args:
            pdf_path: PDF文件路径
            width: 显示宽度（百分比）
            height: 显示高度（像素）

        Returns:
            是否成功显示
        """
        try:
            if not os.path.exists(pdf_path):
                st.error(f"PDF文件不存在: {pdf_path}")
                return False

            # 读取PDF文件
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            # 转换为base64编码
            pdf_base64 = base64.b64encode(pdf_bytes).decode()

            # 创建PDF查看器HTML
            pdf_display = f"""
            <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin: 10px 0;">
                <iframe src="data:application/pdf;base64,{pdf_base64}" 
                        width="{width}%" 
                        height="{height}px" 
                        style="border: none;">
                </iframe>
            </div>
            """

            st.markdown(pdf_display, unsafe_allow_html=True)
            return True

        except Exception as e:
            st.error(f"PDF显示失败: {str(e)}")
            return False

    @staticmethod
    def create_download_button(pdf_path: str, button_label: str = "📥 下载PDF") -> bool:
        """
        创建PDF下载按钮

        Args:
            pdf_path: PDF文件路径
            button_label: 按钮标签

        Returns:
            是否成功创建
        """
        try:
            if not os.path.exists(pdf_path):
                st.error(f"PDF文件不存在: {pdf_path}")
                return False

            # 读取PDF文件
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            # 创建下载按钮
            file_name = os.path.basename(pdf_path)
            st.download_button(
                label=button_label,
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf",
            )
            return True

        except Exception as e:
            st.error(f"下载按钮创建失败: {str(e)}")
            return False

    @staticmethod
    def display_pdf_info(pdf_path: str) -> Dict[str, Any]:
        """
        显示PDF文件信息

        Args:
            pdf_path: PDF文件路径

        Returns:
            PDF信息字典
        """
        try:
            if not os.path.exists(pdf_path):
                return {"status": "error", "error": "文件不存在"}

            # 获取文件信息
            file_size = os.path.getsize(pdf_path)
            file_size_kb = file_size / 1024
            file_size_mb = file_size_kb / 1024

            # 尝试获取PDF页数
            try:
                import PyPDF2

                with open(pdf_path, "rb") as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    page_count = len(pdf_reader.pages)
            except:
                page_count = "未知"

            info = {
                "status": "success",
                "file_name": os.path.basename(pdf_path),
                "file_size_bytes": file_size,
                "file_size_kb": round(file_size_kb, 2),
                "file_size_mb": round(file_size_mb, 2),
                "page_count": page_count,
                "file_path": pdf_path,
            }

            return info

        except Exception as e:
            return {"status": "error", "error": str(e)}

    @staticmethod
    def create_side_by_side_viewer(
        original_pdf_path: str,
        translated_pdf_path: str,
        width: int = 100,
        height: int = 500,
    ) -> bool:
        """
        创建左右对比的PDF查看器

        Args:
            original_pdf_path: 原文PDF路径
            translated_pdf_path: 翻译PDF路径
            width: 显示宽度（百分比）
            height: 显示高度（像素）

        Returns:
            是否成功创建
        """
        try:
            # 检查文件是否存在
            if not os.path.exists(original_pdf_path):
                st.error(f"原文PDF不存在: {original_pdf_path}")
                return False

            if not os.path.exists(translated_pdf_path):
                st.error(f"翻译PDF不存在: {translated_pdf_path}")
                return False

            # 创建两列布局
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**📄 原文PDF**")
                PDFViewer.display_pdf(original_pdf_path, width=90, height=height)
                PDFViewer.create_download_button(original_pdf_path, "📥 下载原文")

            with col2:
                st.markdown("**📖 翻译PDF**")
                PDFViewer.display_pdf(translated_pdf_path, width=90, height=height)
                PDFViewer.create_download_button(translated_pdf_path, "📥 下载翻译")

            return True

        except Exception as e:
            st.error(f"对比查看器创建失败: {str(e)}")
            return False

    @staticmethod
    def create_comparison_viewer(
        comparison_pdf_path: str, width: int = 100, height: int = 600
    ) -> bool:
        """
        创建对比PDF查看器

        Args:
            comparison_pdf_path: 对比PDF路径
            width: 显示宽度（百分比）
            height: 显示高度（像素）

        Returns:
            是否成功创建
        """
        try:
            if not os.path.exists(comparison_pdf_path):
                st.error(f"对比PDF不存在: {comparison_pdf_path}")
                return False

            st.markdown("**📊 PDF对比文档**")

            # 显示PDF信息
            info = PDFViewer.display_pdf_info(comparison_pdf_path)
            if info["status"] == "success":
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("文件大小", f"{info['file_size_kb']:.1f} KB")
                with col2:
                    st.metric("页数", info["page_count"])
                with col3:
                    st.metric("文件名", info["file_name"])

            # 显示PDF
            PDFViewer.display_pdf(comparison_pdf_path, width, height)

            # 创建下载按钮
            PDFViewer.create_download_button(comparison_pdf_path, "📥 下载对比PDF")

            return True

        except Exception as e:
            st.error(f"对比查看器创建失败: {str(e)}")
            return False


# 使用示例
if __name__ == "__main__":
    st.title("PDF查看器测试")

    # 测试PDF显示
    test_pdf = "test.pdf"
    if os.path.exists(test_pdf):
        PDFViewer.display_pdf(test_pdf)
    else:
        st.info("请准备一个测试PDF文件")
