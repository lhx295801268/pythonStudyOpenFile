import sys, getopt ,os , time , getpass, re
# 打开文件 文件路径
def openFile(filePath):
    isExist = os.path.exists(filePath);
    if False == isExist:
        return None;

    fo = open(filePath);
    return fo;

# 处理字符串
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
        #将\r换行替换为\n换行
        if (line1.find('\\r',0,len(line1)) >= 0) :
            line1 = line1.replace('\\r','\\n',len(line1));
        #将\r\n换行替换为\n换行
        if (line1.find('\\r\\n',0,len(line1)) >= 0) :
            line1 = line1.replace('\\r\\n','\\n',len(line1));

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
            # "第一次出现的位置
            firstShowPos = line1.find('\"');
            firstShowPos += 1;
            # 截取译前字符串
            preStr = line1[firstShowPos:midlleChildStrPos];
            # "最后一次出现的位置
            suffixStrPos = line1.rfind('\"');
            # 截取译后字符串
            annotationStr = line1[(midlleChildStrPos + matchStrLen):(suffixStrPos)];
            # 拼接标准字符串
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
# 将字符串写入文件
def writeStrToFile(filePath, contentStr) :
    if None == contentStr or filePath == None :
        return NO;
    file = open(filePath,'wr');
    #写入文件;
    file.write(contentStr);
    file.close();
# 程序文件所处路径
curFilePath = os.getcwd();
readFilePath = curFilePath + '/Localizable.strings';
print('文件路径为：' + readFilePath);
fileContent = openFile(readFilePath);
willWriteStr = disposeStr(fileContent);
writeStrToFile((curFilePath + '/CKLocalizable'), willWriteStr);
fileContent.close();
# print('---->:\n'+willWriteStr+'\n');