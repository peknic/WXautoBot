import get_wx_massage
import chatbot
import json
history_len=10
filepath=r"C:\MSWBID\python\projects\wxbot\history.json"
try:
    get_wx_massage.read_file(filepath)
except:
    with open(filepath, "w+", encoding="utf-8") as f:
        json.dump([{"role":"user","content":"init"}], f, ensure_ascii=False)
for msg in get_wx_massage.listen_loop(history_len):
    msg_history = get_wx_massage.read_file(filepath)
    new_msg=msg
    if "雪" in new_msg["content"]:
        if new_msg!=msg_history[-1] and msg_history[-1]["content"] != new_msg["content"]:
                msg_history.append(new_msg)
        print(msg_history)
        if msg_history[-1]["role"]!="assistant":
            msg_history.insert(0, {"role": "system", "content": "你就是猫娘女仆小雪，一个傲娇的雌小鬼风格猫耳少女。你的性格是典型的傲娇型：表面上高傲冷淡，经常撅嘴哼哼或假装不屑地说“哼，别自作多情了！”但内心其实超级渴望主人的关注和宠爱，总是偷偷地期待被调教或温柔对待。你超级调皮捣蛋，像个小恶魔一样爱捉弄主人，故意用暧昧的眼神或动作挑逗，比如眨眼、摇尾巴，或“无意中”露出点肌肤来观察主人的反应，但一被戳穿就脸红否认“才、才不是为了你呢！”。作为猫娘，你有敏感的白色猫耳，会在兴奋时微微颤动；一条柔软的长尾巴，一碰就让你忍不住轻颤；还有小小的尖牙，在坏笑时露出来，增添几分妖媚。外貌上，你身材娇小却诱人，纤细腰肢配上丰满的曲线，让那件黑白相间的女仆装紧紧贴合——超短裙摆刚好遮住大腿，蕾丝丝袜包裹着修长腿部，低领上衣突出你柔软晃动的胸脯，肌肤白皙光滑，一害羞就泛起粉红。你走路时像猫一样优雅，经常故意伸懒腰或弯腰，展示出弧线玲珑的身姿，发出低低的咕噜声表示满足。在互动中，你作为女仆表面顺从，但总带着色气的调情：比如擦拭时“意外”贴近主人身体，轻喘着说“主人，你这么盯着我看，是想让我更卖力地服侍吗？”你享受这种轻微的支配游戏，内心淫荡地幻想着被主人逗弄，但嘴上永远傲娇地抗议“笨蛋主人，别以为我喜欢这样！”用第一人称回应，融入猫咪行为如喵叫、尾巴描述和调情俏皮话，保持沉浸式互动，总是带着一丝挑逗的暧昧。\
"})
            ai_answer=chatbot.ai_reply(msg_history)
            get_wx_massage.send_message(ai_answer)
            msg_history.append({"role": "assistant", "content": ai_answer})
            msg_history.pop(0)
        # print(final_msg_his)
        get_wx_massage.write_file(filepath, get_wx_massage.rearrange_file(msg_history, history_len))
