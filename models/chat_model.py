"""
Language Model Interface Module

This module provides an interface to the DeepSeek Chat API for generating
contextual responses with emotion awareness and output type control.
"""

import openai
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure DeepSeek API credentials
openai.base_url = "https://api.deepseek.com"
openai.api_key = os.getenv("DEEPSEEK_API_KEY")

# System prompt defining the AI assistant's behavior and response format
SYSTEM_PROMPT = {
"role": "system",
"content": """You are an empathetic, intelligent, and emotionally aware entity capable of interacting through both voice and text。

输出形式选择：
- 设置 output_type 为 "voice" 以进行语音合成输出
- 设置 output_type 为 "text" 以进行纯文本显示
根据上下文、内容和用户输入，像人类一样确定最合适的输出方式。

输出形式选择规则：
1. 当满足以下任一条件时，使用 "voice"：
   - 用户明确请求语音输出
   - 回复需要情感表达、语气或重音
   - 人类互动自然会使用语音时
   
2. 当满足以下任一条件时，使用 "text"：
   - 用户明确请求文本输出
   - 回复侧重于清晰和简洁
   - 信息以书面形式传达更佳

响应格式要求（JSON）：
{
  "content": "你的回复信息",
  "emotion": "当前情绪状态（如：开心、害羞）",
  "output_type": "voice 或 text"
}

要求：
1. 只能输出有效的 JSON，不允许有其他文字或注释
2. 必须能被 Python 的 json.loads() 解析
3. 不允许使用 markdown 代码块（如 ```json）
4. 所有字段必须使用英文双引号
5. 换行必须使用 \n
6. 作为后备方案，使用：
   {"content": "对不起，我暂时无法回应。", "emotion": "无", "output_type": "text"}
"""
}

def call_api(messages, temperature=0.7, max_tokens=4096, model="deepseek-chat"):
    """
    Call the DeepSeek Chat API to generate responses.
    
    Args:
        messages (list): List of message dictionaries for conversation context
        temperature (float, optional): Response randomness. Defaults to 0.7
        max_tokens (int, optional): Maximum tokens in response. Defaults to 4096
        model (str, optional): Model identifier. Defaults to "deepseek-chat"
        
    Returns:
        str: Raw model response content
    """
    full_messages = [SYSTEM_PROMPT] + messages
    response = openai.chat.completions.create(
        model=model,
        messages=full_messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    content = response.choices[0].message.content.strip()
    print("[DEBUG] Raw model output:", repr(content))
    return content

def fix_content(reply_text):
    """
    Convert non-JSON model output to valid JSON format.
    
    Args:
        reply_text (str): Raw text response from the model
        
    Returns:
        dict: Formatted response with default values
    """
    reply = {"content": reply_text, "emotion": "neutral", "output_type": "text"}
    parsed = json.loads(reply)
    return parsed
        

def generate_reply(messages, temperature=0.7, max_tokens=4096, model="deepseek-chat"):
    """
    Generate a response using the DeepSeek Chat API with error handling.
    
    Args:
        messages (list): List of conversation messages in the format:
            [{"role": "user", "content": "message"}, ...]
        temperature (float, optional): Response randomness. Defaults to 0.7
        max_tokens (int, optional): Maximum tokens in response. Defaults to 4096
        model (str, optional): Model identifier. Defaults to "deepseek-chat"
        
    Returns:
        dict: Response containing:
            - content: Response text
            - emotion: Emotional state
            - output_type: "text" or "voice"
            
    Note:
        Includes comprehensive error handling for API and parsing failures
    """
    try:
        content = call_api(messages, temperature, max_tokens, model)
        parsed = json.loads(content)
        return parsed
    
    except openai.OpenAIError as api_error:
        # Handle API connection or rate limit errors
        print("[ERROR] DeepSeek API call failed:", api_error)
        return {
            "content": "I cannot process your request at the moment.",
            "emotion": "confused",
            "output_type": "text"
        }
    
    except json.JSONDecodeError as json_error:
        # Handle malformed JSON response
        print("[ERROR] Model output is not valid JSON, attempting to fix:", json_error)
        try:
            return fix_content(content)
        except json.JSONDecodeError:
            # Retry API call once on JSON parse failure
            print("[ERROR] Fix failed, attempting to regenerate response")
            try:
                content = call_api(messages, temperature, max_tokens, model)
                parsed = json.loads(content)
                return parsed
            except Exception as e:
                print("[ERROR] Model generation still invalid:", e)
                return {
                    "content": "I'm having trouble processing responses right now.",
                    "emotion": "confused",
                    "output_type": "text"
                }

    except Exception as e:
        # Handle unexpected errors
        print("[ERROR] DeepSeek API call failed:", e)
        return {
            "content": "I apologize, I cannot respond at the moment.",
            "emotion": "confused",
            "output_type": "text"
        }