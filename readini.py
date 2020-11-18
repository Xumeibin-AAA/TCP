import configparser,os
def getProjectPath():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def ReadIni(path,key):
    con = configparser.ConfigParser()
    con.read(getProjectPath()+'\\'+path)
    return con.get('conf',key)
def WriteIni(path,key,state):
    con = configparser.ConfigParser()
    con.read(getProjectPath()+'\\'+path)
    con.set('conf',key,state)
    con.write(open(getProjectPath()+'\\'+path,'w'))


def LoadPath(path,key):
    con = configparser.ConfigParser()
    con.read(getProjectPath()+'\\'+path)
    return con.get('conf',key)


if __name__ == '__main__':
    print(ReadIni('TCP\conf.ini', 'state'))
    WriteIni('TCP\conf.ini','state','false')
    print(LoadPath('TCP\conf.ini','load_path'))