# zbo(V1.2-0918)
import time
import random
import config
from utils import wpa, floatinput, overfloatinput, judgeOut
from data import save_history

r = random.randint

def CreateNumber(order, start, end, quantity):
    if order in ["+", "-", "*"]:
        return [r(start, end) for _ in range(quantity)]
    elif order == "-op":
        res = []
        for _ in range(quantity):
            b = r(start, end)
            res.append(b)
            res.append(b + r(start, end))
        return res
    else:
        res = []
        for _ in range(quantity):
            b = r(start, end)
            while b == 0:
                b = r(start, end)
            mul_val = r(start, end)
            res.append(b)
            res.append(b * mul_val)
        return res

def BasicOperationJudge(order, NumberA, NumberB):
    orders = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "-op": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b
    }
    return orders[order](NumberA, NumberB)

def BasicOperation(order):
    PartScore = 0
    CorrectCount = 0
    WrongCount = 0
    TotalTime = 0
    orderprime = order
    if order == "-":
        addorder = input("支持负数出现，请回车，不支持输入任意内容即可。")
        if addorder != "":
            orderprime = "-op"
    while True:
        print("\n选择练习模式：")
        print("1.自定义")
        print("2.默认模式")
        base = input("请选择：")
        if base in config.Specificians:
            return judgeOut(base, PartScore, 2, CorrectCount, WrongCount, TotalTime)
        elif base == "1":
            start = floatinput("\n输入起始值：")
            if start in config.Specificians:
                return judgeOut(start, PartScore, 2, CorrectCount, WrongCount, TotalTime)
            end = overfloatinput("输入末值：", start)
            if end in config.Specificians:
                return judgeOut(end, PartScore, 2, CorrectCount, WrongCount, TotalTime)
            start = int(start)
            end = int(end)
            break
        elif base == "2":
            while True:
                print("\n选择默认模式：")
                print("1. 5以内的运算")
                print("2. 10以内的运算")
                print("3. 20以内的运算")
                print("4. 100以内的运算")
                print("5. 10000以内的运算")
                print("6. 极限模式")
                level = input("选择：")
                if level in config.Specificians:
                    return judgeOut(level, PartScore, 2, CorrectCount, WrongCount, TotalTime)
                elif level in config.Difficulty:
                    start = config.Difficulty[level]["start"]
                    end = config.Difficulty[level]["end"]
                    break
                else:
                    print("不支持！")
            break
        else:
            print("不支持！")
    while True:
        Numbers = CreateNumber(orderprime, start, end, 2)
        NumberA, NumberB = Numbers[1], Numbers[0]
        this_question_wrong = False
        while True:
            StartTime = time.time()
            answer = floatinput(f"\n{NumberA}{order}{NumberB}=?:")
            EndTime = time.time()
            print(f"用时：{EndTime - StartTime:.2f}秒")
            if answer in config.Specificians:
                return judgeOut(answer, PartScore, 2, CorrectCount, WrongCount, TotalTime)
            elif abs(answer - BasicOperationJudge(order, NumberA, NumberB)) < 1e-6:
                PartScore += 2
                wpa(f"答对了，真棒！")
                TotalTime += EndTime - StartTime
                break
            else:
                if not this_question_wrong:
                    PartScore -= 1
                    this_question_wrong = True
                    if config.CurrentUser:
                        if config.CurrentUser not in config.WrongList:
                            config.WrongList[config.CurrentUser] = []
                        config.WrongList[config.CurrentUser].append({
                            "question": f"{NumberA}{order}{NumberB}=?",
                            "correct": BasicOperationJudge(order, NumberA, NumberB),
                            "your": answer
                        })
                        save_history()
                wpa("答错了，请重答！")
        if this_question_wrong:
            WrongCount += 1
        else:
            CorrectCount += 1

if __name__ == "__main__":
    print("=== zbo.py 测试 ===")
    from data import load_data
    load_data()
    print("1. 测试 CreateNumber")
    print(f"   加法取数：{CreateNumber('+', 1, 10, 2)}")
    print(f"   减法取数：{CreateNumber('-', 1, 10, 2)}")
    print(f"   负减法取数：{CreateNumber('-op', 1, 10, 2)}")
    print(f"   乘法取数：{CreateNumber('*', 1, 10, 2)}")
    print(f"   除法取数：{CreateNumber('/', 1, 10, 2)}")
    print("2. 测试 BasicOperationJudge")
    print(f"   3+5={BasicOperationJudge('+', 3, 5)}")
    print(f"   3-5={BasicOperationJudge('-', 3, 5)}")
    print(f"   3*5={BasicOperationJudge('*', 3, 5)}")
    print(f"   6/3={BasicOperationJudge('/', 6, 3)}")
    print("3. 测试 BasicOperation（手动答题）")
    print(f"   返回：{BasicOperation('+')}")
    print("测试结束。")         
