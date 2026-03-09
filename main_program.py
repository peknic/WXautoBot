import get_wx_massage
import chatbot
for msg_his in get_wx_massage.listen_loop(10):
    print(msg_his)
