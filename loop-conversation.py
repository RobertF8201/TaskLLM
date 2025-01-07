from deep_seek_chat_model import DeepSeekChatModel

# 循环对话示例
if __name__ == "__main__":
    # 初始化模型
    api_key = "sk-53ec9f4371e245bc978c5c1a96b2a374"  # 替换为你的DeepSeek API密钥
    chat_model = DeepSeekChatModel(api_key=api_key)

    # 添加系统消息
    chat_model.add_system_message("You are a helpful assistant.")

    print("Chat with DeepSeek! Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # 获取用户输入
        user_input = input("You: ")

        # 检查退出指令
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat. Goodbye!")
            break

        # 添加用户消息到对话历史
        chat_model.add_user_message(user_input)

        # 获取模型响应（非流式）
        # print("\nDeepSeek: ", end="", flush=True)
        # response = chat_model.get_response(stream=False)
        # print(response + "\n")

        # 如果需要流式响应，可以改为以下代码：
        print("\nDeepSeek: ", end="", flush=True)
        response_stream = chat_model.get_response(stream=True)
        for chunk in response_stream:
            print(chunk, end="", flush=True)  # 逐块打印流式响应
        print("\n")