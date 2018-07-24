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
    for line1 in fileContent :
        if 0 > line1.find('" = "') :
            continue;
        else :
            resultList = [];
            resultList = matchSubstrPosList(line1, '"');
            resultStr += '';
        print('====>' + resultStr + '<====');

def matchSubstrPosList(srcStr, childStr):
    resultList = [];
    startIndex = 0;
    itemPos = -1;
    while startIndex < len(srcStr) :
        itemPos = srcStr.find(childStr, startIndex, (len(srcStr) - startIndex));
        if itemPos >= 0 :
            # resultList += itemPos;
            resultList.append(itemPos);
            startIndex = itemPos + 1;
    return resultList;

readFilePath = '/Users/xtkj20180625/Documents/Localizable.strings';
fileContent = openFile(readFilePath);
disposeStr(fileContent);