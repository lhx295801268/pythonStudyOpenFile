import sys, getopt ,os , time , getpass, re
def openFile(filePath):
    isExist = os.path.exists(filePath);
    if False == isExist:
        return None;

    fo = open(filePath);
    return fo;


def disposeStr(fileContent):
    if fileContent == None:
        return None;
    resultStr = '';
    
    lineCount = 1;
    for line1 in fileContent :
        matchStr = '\" = \"';
        matchStrLen = len(matchStr);
        #去掉首位空格
        line1.strip();
        midlleChildStrPos = line1.find(matchStr);
        lineLen = len(line1);
        if 0 > midlleChildStrPos :
            matchStr = '\"=\"';
            matchStrLen = len(matchStr);
            midlleChildStrPos = line1.find(matchStr);

        #只要首字符不是‘\"’或者没有找到对应字符子串的 直接continue 
        if('\"' != line1[0]) or (midlleChildStrPos < 0):
            continue
        else :
            preStr = line1[1:midlleChildStrPos];
            annotationStr = line1[(midlleChildStrPos + matchStrLen):(len(line1) - 3)];
            resultStr += ('\"V\":\"MCLocalization_' + str(lineCount) + '\",\"O\":\"' + preStr + '\",\"T\":\"' + annotationStr + '\"\n');
            lineCount += 1;
    return resultStr;

def matchSubstrPosList(srcStr, childStr):
    resultList = [];
    startIndex = 0;
    itemPos = -1;
    srcStrLength = len(srcStr);
    while startIndex < len(srcStr) :
        itemPos = srcStr.find(childStr, startIndex, (len(srcStr) - startIndex));
        if itemPos >= 0 :
            # resultList += itemPos;
            resultList.append(itemPos);
            startIndex = itemPos + 1;
        else:
            break;
    return resultList;

def writeStrToFile(filePath, contentStr) :
    if None == contentStr or filePath == None :
        return NO;
    file = open(filePath,'wr');
    #写入文件;
    file.write(contentStr);
    file.close();

curFilePath = os.getcwd();
readFilePath = curFilePath + '/Localizable.strings';
print('文件路径为：' + readFilePath);
fileContent = openFile(readFilePath);
willWriteStr = disposeStr(fileContent);
writeStrToFile((curFilePath + '/CKLocalizable'), willWriteStr);
fileContent.close();
# print('---->:\n'+willWriteStr+'\n');