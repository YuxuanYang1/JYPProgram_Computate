# utils.py(V1.2-0918)
import time
import random
import string
import sys
import config
from data import save_data

t = time.sleep
r = random.randint

def wp(word, sec):
    print(word)
    t(sec)

def wpa(word):
    wp(word, 1)

def floatinput(question):
    while True:
        answer = input(question)
        if answer in config.Specificians:
            return answer
        if len(answer) == 0:
            print("输入不能为空，请重输。")
            continue
        temp = answer
        if temp[0] == '-':
            temp = temp[1:]
        if not all(ch in string.digits+"." for ch in temp):
            print("存在不支持字符，请重输。")
            continue
        if temp.count(".") > 1:
            print("小数点过多，请重输。")
            continue
        if temp.startswith(".") or temp.endswith("."):
            print("格式错误，请重输。")
            continue
        return float(answer)

def overfloatinput(question, over):
    while True:
        answer = floatinput(question)
        if answer in config.Specificians:
            return answer
        if answer > over:
            return answer
        else:
            print("未超过初值，请重输。")

def UppsetEnd(NameList, KeyList, ScoreList):
    print("\n强制结束。")
    save_data()
    print(NameList, KeyList, ScoreList)
    return

def judgeOut(judge, Score, lay, CorrectCount=0, WrongCount=0, TotalTime=0):
    if judge == "返回":
        if lay == 2:
            print("已返回。\n")
        if lay == 1:
            print("已是最顶层。\n")
            return [None, Score, CorrectCount, WrongCount, TotalTime]
    if judge == "退出登录":
        if lay == 1:
            print("正在退出……")
        else:
            print("准备退出登录……")
    return [judge, Score, CorrectCount, WrongCount, TotalTime]

def is_idle():
    return "idlelib" in sys.modules

def getkey(question):
    import getpass
    import warnings
    if sys.stdin.isatty() and not is_idle():
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                return getpass.getpass(question)
            except:
                return input(question)
    return input(question)

if __name__ == "__main__":
    print("=== utils.py 测试 ===")
    print("1. 测试 wp")
    wp("测试 wp", 0.5)
    print("2. 测试 wpa")
    wpa("测试 wpa")
    print("3. 测试 floatinput")
    print(f"   返回：{floatinput('输入数字：')}")
    print("4. 测试 overfloatinput")
    print(f"   返回：{overfloatinput('输入大于10的数：', 10)}")
    print("5. 测试 judgeOut")
    print(f"   {judgeOut('返回', 0, 2)}")
    print("6. 测试 is_idle")
    print(f"   {is_idle()}")
    print("7. 测试 getkey")
    print(f"   输入：{getkey('密码：')}")
    print("测试结束。")
