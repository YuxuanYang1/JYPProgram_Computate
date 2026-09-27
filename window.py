#window.py(V1.3-start)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import config
from PyQt5.QtWidgets import QStackedWidget, QMainWindow, QDialog
from login import LoginWindow
from menu import MenuWindow
from practice import PracticeWindow
from difficulty import DifficultyDialog
from display import DisplayWindow
from admin import AdminWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算练习")
        self.resize(500, 450)
        
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2,
                (screen.height() - size.height()) // 2)
        
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # 登录页
        self.login_page = LoginWindow()
        self.login_page.login_success.connect(self.on_login_success)
        self.stack.addWidget(self.login_page)
        
        # 菜单页
        self.menu_page = MenuWindow()
        self.menu_page.mode_selected.connect(self.on_mode_selected)
        self.menu_page.logout.connect(self.on_logout)
        self.stack.addWidget(self.menu_page)
        
        # 答题页
        self.practice_page = PracticeWindow()
        self.practice_page.back_to_menu.connect(self.on_back_to_menu)
        self.stack.addWidget(self.practice_page)

        # 其他显示
        self.display_page = DisplayWindow()
        self.display_page.back_to_menu.connect(self.on_back_to_menu)
        self.stack.addWidget(self.display_page)
        
        # 管理员
        self.admin_page = AdminWindow()
        self.admin_page.back_to_login.connect(self.on_admin_back)
        self.login_page.admin_success.connect(self.on_admin_login)
        self.stack.addWidget(self.admin_page)
        
        self.stack.setCurrentWidget(self.login_page)
    
    def on_login_success(self, name):
        """登录成功，切到菜单页"""
        self.menu_page.refresh()
        self.stack.setCurrentWidget(self.menu_page)
    
    def on_mode_selected(self, mode):
        if mode in config.BasicSeries:
            order = config.BasicSeries[mode]
            dlg = DifficultyDialog(order, self)
            if dlg.exec_() == QDialog.Accepted:
                start, end = dlg.result_range
                self.practice_page.start_practice(order, start, end, dlg.support_negative)
                self.stack.setCurrentWidget(self.practice_page)
        elif mode == "2":
            self.display_page.show_rank()
            self.stack.setCurrentWidget(self.display_page)
        elif mode == "3":
            self.display_page.show_history()
            self.stack.setCurrentWidget(self.display_page)
        elif mode == "4":
            self.display_page.show_wrong()
            self.stack.setCurrentWidget(self.display_page)
            
    def on_back_to_menu(self):
        """从答题页返回菜单"""
        self.menu_page.refresh()
        self.stack.setCurrentWidget(self.menu_page)
        
    def on_logout(self):
        """退出登录，切回登录页"""
        config.CurrentUser = ""
        self.login_page.input_name.clear()
        self.login_page.input_key.clear()
        self.login_page.status.setText("")
        self.stack.setCurrentWidget(self.login_page)

    def on_admin_login(self):
        """管理员登录成功"""
        self.admin_page.refresh()
        self.stack.setCurrentWidget(self.admin_page)

    def on_admin_back(self):
        """管理员返回登录页"""
        self.login_page.input_name.clear()
        self.login_page.input_key.clear()
        self.login_page.status.setText("")
        self.stack.setCurrentWidget(self.login_page)

    def closeEvent(self, event):
        """关闭窗口时保存数据"""
        from data import save_data, save_history
        save_data()
        save_history()
        event.accept()

