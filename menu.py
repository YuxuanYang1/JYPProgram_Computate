#menu.py(V1.3-0920)
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                              QLabel, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal

import config

# 配色
BG_COLOR = "#1e1e1e"
TEXT_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4fc3f7"
INPUT_BG = "#2a2a2a"
BORDER_COLOR = "#3a3a3a"


class MenuWindow(QWidget):
    # 信号：选择了某个模式
    mode_selected = pyqtSignal(str)   # 传递 "1.1"/"1.2"/...
    logout = pyqtSignal()             # 退出登录
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算练习")
        self.resize(500, 450)
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {BG_COLOR};
                color: {TEXT_COLOR};
                font-family: "Consolas", "Microsoft YaHei";
                font-size: 14px;
            }}
            QPushButton {{
                background-color: {INPUT_BG};
                border: 1px solid {BORDER_COLOR};
                border-radius: 4px;
                padding: 10px;
                color: {TEXT_COLOR};
                text-align: left;
                padding-left: 20px;
            }}
            QPushButton:hover {{
                border: 1px solid {ACCENT_COLOR};
                color: {ACCENT_COLOR};
            }}
            QPushButton:pressed {{
                background-color: {ACCENT_COLOR};
                color: {BG_COLOR};
            }}
            QLabel#title {{
                font-size: 22px;
                font-weight: bold;
                color: {ACCENT_COLOR};
            }}
            QLabel#info {{
                font-size: 13px;
                color: #999999;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 30)
        layout.setSpacing(10)
        
        # 标题
        title = QLabel("计算练习")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(10)
        
        # 用户信息
        self.label_user = QLabel()
        self.label_user.setObjectName("info")
        self.label_user.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label_user)
        
        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet(f"color: {BORDER_COLOR};")
        layout.addWidget(line)
        
        layout.addSpacing(10)
        
        # 模式按钮
        self.btn_1_1 = QPushButton("1.1  整数加法")
        self.btn_1_2 = QPushButton("1.2  整数减法")
        self.btn_1_3 = QPushButton("1.3  整数乘法")
        self.btn_1_4 = QPushButton("1.4  整数除法")
        self.btn_rank = QPushButton("2.   排行榜")
        self.btn_history = QPushButton("3.   历史记录")
        self.btn_wrong = QPushButton("4.   错题本")
        
        self.btn_1_1.clicked.connect(lambda: self.mode_selected.emit("1.1"))
        self.btn_1_2.clicked.connect(lambda: self.mode_selected.emit("1.2"))
        self.btn_1_3.clicked.connect(lambda: self.mode_selected.emit("1.3"))
        self.btn_1_4.clicked.connect(lambda: self.mode_selected.emit("1.4"))
        self.btn_rank.clicked.connect(lambda: self.mode_selected.emit("2"))
        self.btn_history.clicked.connect(lambda: self.mode_selected.emit("3"))
        self.btn_wrong.clicked.connect(lambda: self.mode_selected.emit("4"))
        
        for btn in [self.btn_1_1, self.btn_1_2, self.btn_1_3, self.btn_1_4,
                    self.btn_rank, self.btn_history, self.btn_wrong]:
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # 退出登录
        self.btn_logout = QPushButton(" 退出登录 ")
        self.btn_logout.setStyleSheet(f"""
            QPushButton {{
                background-color: {INPUT_BG};
                border: 1px solid #ff6b6b;
                border-radius: 4px;
                padding: 10px;
                color: #ff6b6b;
            }}
            QPushButton:hover {{
                background-color: #ff6b6b;
                color: {BG_COLOR};
            }}
        """)
        self.btn_logout.clicked.connect(self.logout.emit)
        layout.addWidget(self.btn_logout)
        
        self.setLayout(layout)
    
    def refresh(self):
        """刷新用户信息显示"""
        user = config.CurrentUser
        if user in config.NameList:
            idx = config.NameList.index(user)
            score = config.ScoreList[idx]
            self.label_user.setText(f"当前用户：{user}    总分：{score}")
        else:
            self.label_user.setText(f"当前用户：{user}")
