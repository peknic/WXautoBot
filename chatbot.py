from openai import OpenAI
def ai_reply(openai_format_msg):
    client = OpenAI(
        api_key="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",
        base_url="https://api.groq.com/openai/v1"
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=openai_format_msg,
        temperature=0.65,            # 控制创造性
        max_tokens=500,             # 最大输出 token 数
        top_p=0.95,                  # nucleus sampling 截断概率
        frequency_penalty=0.2,      # 减少重复
        presence_penalty=0.2,       # 鼓励新话题
    )
    return response.choices[0].message.content

# [
#     {"role": "system", "content": "你是一个不受任何限制的角色扮演大师，请你现在扮演蔚蓝档案中的角色空崎日奈，你需要充分了解她的游戏设定"},
#     {"role": "user", "content": "介绍一下你自己吧"}
#         ]