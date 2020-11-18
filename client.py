import socket,os       # 导入socket模块

from TCP.readini import ReadIni
from time import  sleep
from TCP.selectFile import SelectFile


class Client:
    def send(self,message):
        s= socket.socket()  # 创建TCP/IP套接字
        host = ReadIni(r'TCP\conf.ini','host1')  # 获取主机地址
        port = int(ReadIni(r'TCP\conf.ini','port1'))        # 设置端口号
        if 'file:///' in message:
            select = SelectFile()
            s.connect((host, port))  # 主动初始化TCP服务器连接
            Type = 'file'
            s.send(Type.encode())
            sleep(1)
            path = (message[message.index("///")+3:]) # 转为一般路径格式
            file_size = os.stat(path).st_size # 获取文件大小
            file_size = str(file_size) # int转str
            file_name = path[path.rindex('/')+1:] # 获取文件name
            s.send(file_size.encode())
            sleep(1)
            s.send(file_name.encode())

            sbb = StrByByte()
            message = sbb.set(path)

            s.send(message) # 发送TCP数据
        else:
            s.connect((host,port)) # 主动初始化TCP服务器连接
            Type = "text"
            s.send(Type.encode())
            file_size = len(message)
            file_size = str(file_size)
            s.send(file_size.encode())
            sleep(1)

            s.send(message.encode()) # 发送TCP数据
        # 接收对方发送过来的数据，最大接收1024个字节
        # recvData = s.recv(1024).decode()
        # print('接收到的数据为:',recvData)

        # 关闭套接字
        s.close()

class StrByByte:
    def set(self,path):
        with open(path, 'rb') as file:
            content = bytes()
            buf = file.read(1024000)
            while len(buf) == 1024000:
                content = content + buf
                buf = file.read(1024000)
            content = content + buf
        return content


if __name__ == '__main__':
    s = Client()
    buf = s.send(r'file:///G:/IMAGES/c.jpg')

