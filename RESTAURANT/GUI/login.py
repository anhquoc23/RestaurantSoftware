from PyQt6.QtWidgets import QWidget, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
from RESTAURANT.BUS import UserBus as user

class Login(QMainWindow):
    def __init__(self):
        super().__init__()

        # Thiết lập thông tin cho window
        self.setWindowTitle('PHẦN MỀM QUẢN LÝ NHÀ HÀNG')
        self.resize(350, 320)

        #Tạo Layout lớn
        v_layout = QVBoxLayout()

        h_username = QHBoxLayout()
        lb_employee_id = QLabel('ID NHÂN VIÊN')
        lb_employee_id.setStyleSheet('min-width: 100px')
        txt_employee_id = QLineEdit()
        h_username.addWidget(lb_employee_id)
        h_username.addWidget(txt_employee_id)

        h_pw = QHBoxLayout()
        lb_pw = QLabel('MẬT KHẨU')
        lb_pw.setStyleSheet('min-width: 100px')
        txt_pw = QLineEdit()
        txt_pw.setEchoMode(QLineEdit.EchoMode.Password)
        h_pw.addWidget(lb_pw)
        h_pw.addWidget(txt_pw)

        h_btn = QHBoxLayout()
        btn_login = QPushButton("Login")
        h_btn.addWidget(btn_login)


        # Thêm các layout con vào layout lớn
        v_layout.addLayout(h_username)
        v_layout.addLayout(h_pw)
        v_layout.addLayout(h_btn)

        container =QWidget()
        container.setLayout(v_layout)
        self.setCentralWidget(container)

        def login(self):
            try:
                if user.check_login(txt_employee_id.text(), txt_pw.text()):
                    print('Login')
                else:
                    print('Invalid')
            except Exception as e:
                print(e)

        btn_login.clicked.connect(login)


# 4830fde6e0b44d9f83e2a42571cb811c
