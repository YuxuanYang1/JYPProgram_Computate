# user.py(V1.2-0918)
import string
import hashlib
import config
from utils import wpa, wp, getkey, UppsetEnd
from data import load_data, save_data, load_history, save_history
from menu import main
from announcement import show_announcement

def modify_password():
    target = input("请输入账号名：")
    AccountNumber_tmp = -1
    for sonG, sonA in enumerate(config.NameList):
        if sonA == target:
            AccountNumber_tmp = sonG
            break
    if AccountNumber_tmp == -1:
        wpa("账号不存在。\n")
        return
    oldkey = getkey("请输入旧密码：")
    if hashlib.sha256(oldkey.encode()).hexdigest() != config.KeyList[AccountNumber_tmp]:
        wpa("旧密码不正确。\n")
        return
    newkey = getkey("请输入新密码（4-10字符）：")
    if not (4 <= len(newkey) <= 10):
        wpa("密码长度不和。\n")
        return
    if any(SonC not in string.printable for SonC in newkey):
        wpa("存在不支持字符，请重输。\n")
        return
    config.KeyList[AccountNumber_tmp] = hashlib.sha256(newkey.encode()).hexdigest()
    save_data()
    wpa("密码修改成功！\n")

def modify_name():
    target = input("请输入账号名：")
    AccountNumber_tmp = -1
    for sonG, sonA in enumerate(config.NameList):
        if sonA == target:
            AccountNumber_tmp = sonG
            break
    if AccountNumber_tmp == -1:
        wpa("账号不存在。\n")
        return
    key_tmp = getkey("请输入密码：")
    if hashlib.sha256(key_tmp.encode()).hexdigest() != config.KeyList[AccountNumber_tmp]:
        wpa("密码不正确。\n")
        return
    newname = input("请输入新账号名：")
    if newname in config.NameList:
        wpa("该账号名已被占用。\n")
        return
    config.NameList[AccountNumber_tmp] = newname
    save_data()
    wpa(f"账号名修改成功！新账号名：{newname}\n")

def on(state):
    load_data()
    load_history()
    if state in ["All", "Ann"]:
        show_announcement()
    while True:
        if state in ["All", "login"]:
            loginstate = 1
            while loginstate:
                print("接下来是登录环节，请在提示符后键入账号名。")
                print("如果没有账号，我们将会自动为你注册")
                wpa("可以输入'修改密码'/'修改账号名'来修改。")
                Name = input("账号名：")
                if Name == "结束":
                    UppsetEnd(config.NameList, config.KeyList, config.ScoreList)
                    return
                elif Name == "admin":
                    adminkey = getkey("管理员密码：")
                    if hashlib.sha256(adminkey.encode()).hexdigest() == config.ADMIN_KEY_HASH:
                        wpa("已进入管理员模式。\n")
                        from admin import admin_menu
                        admin_menu()
                    else:
                        wpa("管理员密码不正确。\n")
                    continue
                elif Name == "修改密码":
                    modify_password()
                    continue
                elif Name == "修改账号名":
                    modify_name()
                    continue
                AccountNumber = -1
                found = False
                for sonG, sonA in enumerate(config.NameList):
                    if sonA == Name:
                        AccountNumber = sonG
                        found = True
                        break
                if found:
                    for attempt in range(4):
                        if attempt == 0:
                            wpa("请在提示符后键入密码。")
                        else:
                            wpa(f"密码不正确，请重新输入，你还有{4-attempt}次机会。")
                        key = getkey("密码：\n")
                        if key == "结束":
                            UppsetEnd(config.NameList, config.KeyList, config.ScoreList)
                            return
                        if hashlib.sha256(key.encode()).hexdigest() == config.KeyList[AccountNumber]:
                            wpa(f"欢迎回来，{Name}")
                            Score = config.ScoreList[AccountNumber]
                            config.CurrentUser = Name
                            loginstate = 0
                            break
                    else:
                        wpa("登录失效，请确认信息后重新登录\n")
                        loginstate = 2
                if loginstate == 1:
                    while True:
                        key = input("新账号注册：请设置密码（英文数字符号组合，4-10字符）。")
                        if key == "结束":
                            UppsetEnd(config.NameList, config.KeyList, config.ScoreList)
                            return
                        if not (4 <= len(key) <= 10):
                            wpa("密码长度不和。")
                            continue
                        if any(SonC not in string.printable for SonC in key):
                            wpa("存在不支持字符，请重输。")
                            continue
                        config.NameList.append(Name)
                        config.KeyList.append(hashlib.sha256(key.encode()).hexdigest())
                        config.ScoreList.append(0)
                        save_data()
                        wpa(f"好的，{Name}，恭喜你成为第{len(config.NameList)}名用户，请再次登录确认。\n")
                        break
                if loginstate == 2:
                    loginstate = 1
        if state == "All":
            result = main()
            order, score = result[0], result[1]
            wpa(f"\n好的，{Name}，您的本轮得分是{score}，再见！\n")
            config.ScoreList[AccountNumber] = Score + score
            save_data()
            if order == "结束":
                UppsetEnd(config.NameList, config.KeyList, config.ScoreList)
                return
        elif state in ["login", "Ann"]:
            return

if __name__ == "__main__":
    print("=== user.py 测试 ===")
    print("1. 测试公告（on('Ann')）")
    on("Ann")
    print("2. 测试登录（on('login')）")
    on("login")
    print("测试结束。")
