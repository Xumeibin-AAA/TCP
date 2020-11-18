# -*- coding:utf-8 -*-
import socket,sys,time,os  #导入socket模块
from time import sleep
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication,QPushButton,QGridLayout,QTextEdit,QWidget,QMessageBox
from multiprocessing import Process
from TCP import client,connect
from TCP.Kill_pid import KillPid
from TCP.readini import ReadIni, WriteIni


class Server:
    def __init__(self):
        host = ReadIni(r'TCP\conf.ini','host')          #主机IP
        port = int(ReadIni(r'TCP\conf.ini','port'))                 #端口号
        KillPid(port)
        web = socket.socket()           #创建 socket 对象
        print(host)
        print(port)
        web.bind((host,port))       #绑定端口
        web.listen(5)               #设置最多连接数
        print ('服务器等待客户端连接...')
        # 开启死循环
        while True:
            conn, addr = web.accept()  # 建立客户端连接
            print('连接成功')
            Type = conn.recv(1024)  # 获取客户端请求数据
            print('接受消息成功')
            Type = Type.decode()
            print(Type)

            if Type == "file":
                data = conn.recv(1024)  # 获取客户端请求数据
                print(data)

                data = data.decode()
                file_size = int(data)

                data = conn.recv(1024)  # 获取客户端请求数据
                temp = 1
                data = data.decode()
                file_name = data
                print(file_name)

                # conn.close()            #关闭链接
                data = conn.recv(file_size)
                temp = 0
                # print(data)
                load_path = ReadIni(r'TCP\conf.ini','load_path')
                with open(f"{load_path}\{file_name}", "wb") as file:
                    file.write(data)
                    file.close
                    print("下载完成")
                with open(ReadIni(r'TCP\conf.ini','temp_path'), mode='w', encoding='utf-8') as file:
                    file.write(f'{file_name} 已下载完成')
                    file.close()
                WriteIni('TCP\conf.ini', 'state', 'true')

            else:
                data = conn.recv(1024)  # 获取客户端请求数据
                data = data.decode()
                file_size = int(data)
                print(file_size)
                data = conn.recv(file_size)
                data = data.decode()
                with open(ReadIni(r'TCP\conf.ini','temp_path'), mode='w', encoding='utf-8') as file:
                    file.write(data)
                    file.close()
                WriteIni('TCP\conf.ini', 'state', 'true')
                sleep(2)
                # conn.close()            #关闭链接


'''
图形界面
'''
class MyFrame(QWidget):
    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        self.text1 = QTextEdit()
        self.text2 = QTextEdit()
        but1 = QPushButton("发送")
        layout.addWidget(self.text1,0,0,1,4)
        layout.addWidget(self.text2, 4,0,2,4)
        layout.addWidget(but1,6,1,4,2)
        self.setGeometry(300,300,600,600)
        self.show()

        self.therad = MyThread()
        self.therad.sig.connect(self.updata)
        self.therad.start()

        but1.clicked.connect(self.send)
        WriteIni('TCP\conf.ini', 'state', 'true')
    # 最终显示在文本框的内容
    def updata(self,msg):
        message = str(msg).replace("[",'').replace("]",'').replace("'",'')

        self.text1.append(message)
    def send(self):
        Error = 0
        try:
            c = client.Client()
            if len(self.text2.toPlainText())!=0:
                message = self.text2.toPlainText()
                if 'file:///' in message:
                    print(message[message.index("///")+3:])
                    if os.path.isdir(self.text2.toPlainText()[self.text2.toPlainText().index("///")+3:]):
                        QMessageBox.information(self, 'inf', '不能传输目录！！！')
                        Error = 1
                    else:
                        c.send(self.text2.toPlainText())
                else:
                    c.send(self.text2.toPlainText())



            else:

                QMessageBox.information(self,'inf','输入内容不能为空！！！')

                Error = 1
        except Exception as e:
            pass

        while True:
            try:
                if Error==0:
                    if int(time.time())%2==0:
                        with open(ReadIni(r'TCP\conf.ini','temp_path'), mode='w', encoding='utf-8') as file:
                            file.write(f"{'本机发送'} {self.text2.toPlainText()}")
                            file.close()
                        self.text2.clear()
                        WriteIni('TCP\conf.ini', 'state', 'true')
                        break
                else:
                    break
            except Exception as e:
                pass



'''
信号槽
'''
class MyThread(QThread):
    sig = pyqtSignal(object)
    def __init__(self):
        super().__init__()
    def run(self):
        while True:
            if int(time.time()) % 2 == 1:
                if ReadIni('TCP\conf.ini','state')=='true':
                    with open(ReadIni(r'TCP\conf.ini','temp_path'), mode='r', encoding='utf-8') as file:
                        f = file.readlines()
                        file.close()
                    self.sig.emit(f"{time.strftime('%Y-%m-%d %H:%M:%S')}   {f}")
                    WriteIni('TCP\conf.ini', 'state', 'false')
                    sleep(1)



def start():
    app = QApplication(sys.argv)
    myframe = MyFrame()
    p = Process(target=Server)
    p.start()
    # p1 = Process(target=connect.send)
    # p1.start()
    myframe.initUI()
    sys.exit(app.exec_())

