import json
import sqlite3
from openai import OpenAI
from datetime import datetime

# 初始化 SQLite 数据库
def init_db():
    """初始化数据库，创建待办事项表"""
    conn = sqlite3.connect("todos.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            todo TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Agent 类
class TodoAgent:
    def __init__(self, api_key):
        """初始化 Agent，设置大模型 API 密钥"""
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        self.conn = sqlite3.connect("todos.db")
        self.cursor = self.conn.cursor()
        self.today_date = datetime.now().strftime('%Y-%m-%d')

    def close(self):
        """关闭数据库连接"""
        self.conn.close()

    def parse_action(self, user_input):
        """使用大模型解析用户输入，判断需要执行的操作"""
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个待办事项管理助手，根据用户输入判断需要执行的操作。"
                    "支持的操作：添加待办、删除待办、查看待办、退出。"
                    "请将结果以 JSON 格式返回，包含以下字段："
                    "1. 'action': 操作类型（add/delete/view/exit）。"
                    "2. 'date': 日期，格式为 'YYYY-MM-DD'（仅对添加和删除操作有效）。"
                    "3. 'task': 任务内容（仅对添加和删除操作有效）。"
                    f"今天的日期是：{self.today_date}。"
                },
                {"role": "user", "content": user_input},
            ],
        )
        return response.choices[0].message.content

    def add_todo(self, date, todo):
        """添加待办事项到数据库"""
        self.cursor.execute("INSERT INTO todos (date, todo) VALUES (?, ?)", (date, todo))
        self.conn.commit()
        print(f"已添加待办事项：{date} - {todo}")

    def delete_todo(self, todo_id):
        """根据 ID 删除待办事项"""
        self.cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        self.conn.commit()
        print(f"已删除待办事项 ID: {todo_id}")

    def show_todos(self, date):
        """显示某一天的待办事项"""
        self.cursor.execute("SELECT id, todo FROM todos WHERE date = ?", (date,))
        todos = self.cursor.fetchall()
        if todos:
            print(f"{date}的待办事项：")
            for todo_id, todo in todos:
                print(f"{todo_id}. {todo}")
        else:
            print(f"{date}没有待办事项。")

    def run(self):
        """运行 Agent，与用户交互"""
        print("欢迎使用待办事项管理 Agent！")
        while True:
            user_input = input("\n你: ").strip()

            # 退出
            if user_input.lower() in ["退出", "exit"]:
                print("Agent: 再见！")
                break

            # 解析用户输入
            action = self.parse_action(user_input)
            print(action)
            action = json.loads('\n'.join(action.strip().split('\n')[1:-1]))    # 按行分割并去除首尾空白;去掉第一行和最后一行;重新组合为字符串;转化为字典
            print(f"Agent: 解析的操作 - {action}")            
            # 执行操作
            if action["action"] == "add":
                print("添加待办")
                try:
                    # 假设用户输入格式为“在YYYY年MM月DD日添加待办：XXX”
                    date = action["date"]
                    todo = action["task"]
                    print(date, todo)
                    self.add_todo(date, todo)
                except (ValueError, IndexError):
                    print("Agent: 输入格式不正确，请使用 '在YYYY年MM月DD日添加待办：XXX' 格式。")

            elif action["action"] == "delete":
                print("删除待办")
                # try:
                #     # 假设用户输入格式为“删除待办 ID”
                #     todo_id = int(user_input.split("删除待办")[1].strip())
                #     self.delete_todo(todo_id)
                # except (ValueError, IndexError):
                #     print("Agent: 输入格式不正确，请使用 '删除待办 ID' 格式。")

            elif action["action"] == "view":
                print("查看待办")
                try:
                    # 假设用户输入格式为“查看YYYY年MM月DD日的待办”
                    date = action["date"]
                    self.show_todos(date)
                except ValueError:
                    print("Agent: 输入格式不正确，请使用 '查看YYYY年MM月DD日的待办' 格式。")

            else:
                print("Agent: 未知操作，请尝试添加、删除或查看待办事项。")

# 使用示例
if __name__ == "__main__":
    # 初始化数据库
    init_db()

    # 初始化 Agent
    api_key = "sk-53ec9f4371e245bc978c5c1a96b2a374"  # 替换为你的 OpenAI API 密钥
    agent = TodoAgent(api_key)

    # 运行 Agent
    try:
        agent.run()
    finally:
        agent.close()