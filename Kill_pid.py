'''
杀死进程
'''
import os
class KillPid:
    def __init__(self,port):
        try:
            with os.popen(f'netstat -aon|findstr {port}') as res:
                res = res.read().split('\n')
            result = []
            for line in res:
                temp = [i for i in line.split(' ') if i != '']
                if len(temp) > 4:
                    result.append({'pid': temp[4], 'address': temp[1], 'state': temp[3]})

            for i in result:
                if(int(i.get('address')[i.get('address').index(':')+1:])==port):
                    os.popen(f"taskkill -pid {int(i.get('pid'))} -f")
                    break
        except Exception as e:
            pass
if __name__ == '__main__':
    KillPid(8082)