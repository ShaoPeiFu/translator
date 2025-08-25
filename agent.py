import os
import json
from typing import Dict, List, Optional
from dashscope import Generation
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class TranslationAgent:
    """英语翻译Agent，使用Qwen模型"""

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化翻译Agent

        Args:
            api_key: 阿里云API密钥，如果不提供则从环境变量获取
        """
        self.api_key = api_key or os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置DASHSCOPE_API_KEY环境变量或在初始化时提供API密钥")

        # 设置模型参数
        self.model = "qwen-max"
        self.max_tokens = 2000
        self.temperature = 0.1  # 低温度确保翻译准确性

        # 翻译提示词模板
        self.translation_prompt_template = """
你是一个专业的英语翻译专家。请将以下文本翻译成中文，要求：
1. 保持原文的意思和语气
2. 使用自然流畅的中文表达
3. 保持专业术语的准确性
4. 如果是技术文档，请保持技术准确性

原文：
{text}

请直接输出翻译结果，不要添加任何解释：
"""

        # 语言检测提示词
        self.language_detection_prompt = """
请检测以下文本的语言，只回答语言名称（如：英语、中文、法语等）：

{text}

语言：
"""

        # PDF翻译提示词模板
        self.pdf_translation_prompt_template = """
你是一个专业的PDF文档翻译专家。请将以下PDF文本内容翻译成中文，要求：
1. 保持原文的段落结构和格式
2. 准确翻译专业术语和技术内容
3. 保持文档的逻辑性和可读性
4. 对于标题、章节名等，保持清晰的层次结构
5. 对于表格、列表等内容，保持原有的格式信息

PDF文本内容：
{text}

请直接输出翻译结果，保持原文的段落结构：
"""

    def detect_language(self, text: str) -> str:
        """
        检测文本语言

        Args:
            text: 待检测的文本

        Returns:
            检测到的语言名称
        """
        try:
            response = Generation.call(
                model=self.model,
                prompt=self.language_detection_prompt.format(text=text),
                api_key=self.api_key,
                max_tokens=50,
                temperature=0.1,
            )

            if response.status_code == 200:
                return response.output.text.strip()
            else:
                return "未知语言"

        except Exception as e:
            print(f"语言检测失败: {e}")
            return "未知语言"

    def translate_to_chinese(self, text: str, context: str = "") -> Dict[str, str]:
        """
        将文本翻译成中文

        Args:
            text: 待翻译的文本
            context: 上下文信息（可选）

        Returns:
            包含翻译结果的字典
        """
        try:
            # 构建翻译提示词
            if context:
                prompt = f"{self.translation_prompt_template.format(text=text)}\n\n上下文信息：{context}"
            else:
                prompt = self.translation_prompt_template.format(text=text)

            response = Generation.call(
                model=self.model,
                prompt=prompt,
                api_key=self.api_key,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            if response.status_code == 200:
                translation = response.output.text.strip()
                return {
                    "original": text,
                    "translation": translation,
                    "status": "success",
                    "model": self.model,
                }
            else:
                return {
                    "original": text,
                    "translation": "",
                    "status": "error",
                    "error": f"API调用失败: {response.message}",
                }

        except Exception as e:
            return {
                "original": text,
                "translation": "",
                "status": "error",
                "error": str(e),
            }

    def batch_translate(self, texts: List[str]) -> List[Dict[str, str]]:
        """
        批量翻译文本

        Args:
            texts: 待翻译的文本列表

        Returns:
            翻译结果列表
        """
        results = []
        for text in texts:
            if text.strip():
                result = self.translate_to_chinese(text)
                results.append(result)
        return results

    def translate_with_glossary(
        self, text: str, glossary: Dict[str, str]
    ) -> Dict[str, str]:
        """
        使用术语表进行翻译

        Args:
            text: 待翻译的文本
            glossary: 术语表，格式为 {英文: 中文}

        Returns:
            翻译结果
        """
        # 构建包含术语表的提示词
        glossary_text = "\n".join([f"{en}: {zh}" for en, zh in glossary.items()])
        enhanced_prompt = f"""
你是一个专业的英语翻译专家。请使用以下术语表进行翻译：

术语表：
{glossary_text}

{self.translation_prompt_template.format(text=text)}

请严格按照术语表进行翻译：
"""

        try:
            response = Generation.call(
                model=self.model,
                prompt=enhanced_prompt,
                api_key=self.api_key,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            if response.status_code == 200:
                translation = response.output.text.strip()
                return {
                    "original": text,
                    "translation": translation,
                    "status": "success",
                    "model": self.model,
                    "glossary_used": True,
                }
            else:
                return {
                    "original": text,
                    "translation": "",
                    "status": "error",
                    "error": f"API调用失败: {response.message}",
                }

        except Exception as e:
            return {
                "original": text,
                "translation": "",
                "status": "error",
                "error": str(e),
            }

    def translate_pdf_content(self, text: str, context: str = "") -> Dict[str, str]:
        """
        翻译PDF文档内容

        Args:
            text: PDF文本内容
            context: 文档类型或上下文信息

        Returns:
            翻译结果
        """
        try:
            # 使用PDF专用的翻译提示词
            if context:
                prompt = f"{self.pdf_translation_prompt_template.format(text=text)}\n\n文档类型：{context}"
            else:
                prompt = self.pdf_translation_prompt_template.format(text=text)

            response = Generation.call(
                model=self.model,
                prompt=prompt,
                api_key=self.api_key,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            if response.status_code == 200:
                translation = response.output.text.strip()
                return {
                    "original": text,
                    "translation": translation,
                    "status": "success",
                    "model": self.model,
                    "type": "pdf_translation",
                }
            else:
                return {
                    "original": text,
                    "translation": "",
                    "status": "error",
                    "error": f"API调用失败: {response.message}",
                }

        except Exception as e:
            return {
                "original": text,
                "translation": "",
                "status": "error",
                "error": str(e),
            }

    def translate_pdf_chunks(
        self, text_chunks: List[str], context: str = ""
    ) -> List[Dict[str, str]]:
        """
        翻译PDF文本块

        Args:
            text_chunks: 文本块列表
            context: 文档类型或上下文信息

        Returns:
            翻译结果列表
        """
        results = []
        total_chunks = len(text_chunks)

        for i, chunk in enumerate(text_chunks, 1):
            if chunk.strip():
                print(f"正在翻译第 {i}/{total_chunks} 个文本块...")
                result = self.translate_pdf_content(chunk, context)
                result["chunk_index"] = i
                result["total_chunks"] = total_chunks
                results.append(result)

        return results

    def get_translation_progress(self, current: int, total: int) -> Dict[str, any]:
        """
        获取翻译进度信息

        Args:
            current: 当前进度
            total: 总数

        Returns:
            进度信息字典
        """
        percentage = round((current / total) * 100, 2) if total > 0 else 0

        return {
            "current": current,
            "total": total,
            "percentage": percentage,
            "remaining": total - current,
            "status": "in_progress" if current < total else "completed",
        }


# 使用示例
if __name__ == "__main__":
    # 创建翻译agent实例
    try:
        agent = TranslationAgent()

        # 测试翻译
        test_text = "Hello, how are you today? I hope you're doing well."
        result = agent.translate_to_chinese(test_text)
        print("翻译结果:", result)

        # 测试语言检测
        detected_lang = agent.detect_language(test_text)
        print("检测到的语言:", detected_lang)

    except Exception as e:
        print(f"初始化失败: {e}")
        print("请确保设置了DASHSCOPE_API_KEY环境变量")
