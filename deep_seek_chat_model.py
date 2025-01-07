from openai import OpenAI

class DeepSeekChatModel:
    def __init__(self, api_key, base_url="https://api.deepseek.com", model="deepseek-chat"):
        """
        初始化DeepSeek聊天模型。

        :param api_key: DeepSeek API密钥
        :param base_url: DeepSeek API的基础URL
        :param model: 使用的模型名称
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.conversation_history = []  # 保存对话历史

    def add_system_message(self, content):
        """
        添加系统消息到对话历史。

        :param content: 系统消息内容
        """
        self.conversation_history.append({"role": "system", "content": content})

    def add_user_message(self, content):
        """
        添加用户消息到对话历史。

        :param content: 用户消息内容
        """
        self.conversation_history.append({"role": "user", "content": content})

    def get_response(self, stream=False):
        """
        调用DeepSeek API获取模型响应。

        :param stream: 是否使用流式响应
        :return: 如果 stream=False，返回完整响应内容；如果 stream=True，返回生成器
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.conversation_history,
            stream=stream
        )

        if stream:
            # 如果是流式响应，返回生成器
            return self._handle_stream_response(response)
        else:
            # 如果是非流式响应，返回完整内容
            return response.choices[0].message.content

    def _handle_stream_response(self, response):
        """
        处理流式响应，逐块生成内容。

        :param response: 流式响应对象
        :return: 生成器，逐块生成响应内容
        """
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    def reset_conversation(self):
        """
        重置对话历史。
        """
        self.conversation_history = []

