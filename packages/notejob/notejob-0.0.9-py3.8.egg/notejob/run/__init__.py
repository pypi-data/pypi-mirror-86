import os
import re
import signal

# 要杀死程序名称，最好全名
program_name = "notejob"
# 终端执行的命令
order_str = "ps x | grep %s" % program_name
# 执行
strs_obj = os.popen(order_str)
t_strs = strs_obj.read()
# 通过正则获取pid
print(t_strs)
# pid_list = re.findall(r"(\d+).+chromedriver --port=\d+", t_strs, re.I)
# print(pid_list)
# for j in pid_list:
#     print(j)
#     # 杀死进程
#     # os.kill(int(j), signal.SIGKILL)
