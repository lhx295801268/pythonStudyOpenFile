import sys, getopt ,os , time , getpass

def openFile(filePath):
    isExist = os.path.exists(filePath);
    if False == isExist:
        return None;

    fo = open(filePath);
    return fo;


def disposeStr(fileContent):
    if fileContent == None:
        return None;

    for line1 in fileContent :
        print '---->' + line1 + '<------';


raw_input('输入文件路径\n');
readFilePath = '/Users/xtkj20180625/Documents/Localizable.strings';
fileContent = openFile(readFilePath);
disposeStr(fileContent);
raw_input('输入输出文件路径\n')
