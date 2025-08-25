import os
from dotenv import load_dotenv
from dashscope import Generation

load_dotenv()
api_key = os.getenv("QWEN_API")

response = Generation.call(
    model = "qwen2.5-32b-instruct",
    prompt = "我可以如何使用lora微调你",
    api_key = api_key,
)
print(response.output)

