import socket,os       # 导入socket模块
from TCP.readini import ReadIni,WriteIni
from time import sleep
import time
def send():

    while True:
        try:
            s = socket.socket()  # 创建TCP/IP套接字
            host = ReadIni(r'TCP\conf.ini', 'host1')  # 获取主机地址
            port = int(ReadIni(r'TCP\conf.ini', 'port1'))  # 设置端口号
            start = time.time()

            WriteIni(r'TCP\conf.ini', 'connect', "false")
            s.connect((host, port))  # 主动初始化TCP服务器连接
            s.send('')
        except Exception as e:
            pass
        finally:
            if (time.time() - start)<2:
                WriteIni(r'TCP\conf.ini', 'connect', "true")
            print(time.time() - start)
            sleep(5)
            s.close()
