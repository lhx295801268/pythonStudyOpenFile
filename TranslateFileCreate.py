import argparse, os, filecmp, sys, re, getopt, time
#coding:utf-8
# 读取文件
def readFile(filePath):
    fileIsExist = os.path.exists(filePath);
    if fileIsExist == False :
        print("did not find this file");
        return None;
    return open(filePath);

# 解析文件内容
def parserFileStr(srcStrLines) :
    vStr = '\"V\":\"';
    oStr = '\",\"O\":\"';
    tStr = '\",\"T\":\"';
    vLen = len(vStr);
    oLen = len(oStr);
    tLen = len(tStr);
    resultList = [];
    for itemLine in srcStrLines :
        vPos = itemLine.find(vStr);
        oPos = itemLine.find(oStr);
        tPos = itemLine.find(tStr);
        lastChPos = itemLine.rfind('\"');
        firstStr = itemLine[(vPos + vLen):(oPos)];
        secondStr = itemLine[(oPos + oLen):(tPos)];
        thirdStr = itemLine[(tPos + tLen):(lastChPos)];
        tempList = [firstStr, secondStr, thirdStr];
        resultList.append(tempList);
    return resultList;
    
# 解析文件 拼接.h文件
# #import <Foundation/Foundation.h>
# @interface TFTranslations : NSObject {
# @protected
# 	/** 动态更新文本map */
# 	NSDictionary<NSString *, NSString *> *_map;
# }
# /** 是否使用硬编码代码 */
# @property (nonatomic) BOOL hard_code;
def createHFileStr(contentList):
    curTime = time.localtime(time.time());
    dayStr = str(curTime.tm_year) +'.'+ str(curTime.tm_mon) + '.'+ str(curTime.tm_mday);
    dayStr = dayStr + ' ' + str(curTime.tm_hour) + ':' + str(curTime.tm_min) + ':' + str(curTime.tm_sec);
    resultStr = '/*'+ fileName +'.class \n build with '+ dayStr +'*/\n\n';

    resultStr = resultStr + '#import <Foundation/Foundation.h>\n';
    resultStr = resultStr + '@interface ' + fileName + ' : NSObject {\n';
    resultStr = resultStr + '\t@protected\n' + '\t/** 动态更新文本map */\n' + '\tNSDictionary<NSString *, NSString *> *_map;\n}\n';
    resultStr = resultStr + '\t/** 是否使用硬编码代码 */\n' + '\t@property (nonatomic) BOOL hard_code;\n\n'# + '@property (nonatomic, assign, readonly) MCLanguageType *curLanguageTaype;\n\n'; 

    for itemList in contentList :
        # print('======>'+itemList[0]+'\t======>'+itemList[1]+'\t======>'+itemList[2]);
        tempItemStr = '\t/*'+ itemList[1] +'*/\n';
        tempItemStr = tempItemStr + '\t@property (nonatomic, strong, readonly) NSString * ' + itemList[0] + ';\n';
        resultStr = resultStr + tempItemStr;
    resultStr = resultStr + '\n\n@end';
    return resultStr;

# 解析文件 拼接.m文件
# #import "TFTranslations.h"
# #define _TFTranslationsImplement(v, hc) - (NSString *)v { if (self.hard_code || !_map[@#v]) { return hc; } return _map[@#v]; }
# @implementation TFTranslations
# _TFTranslationsImplement(MCLocalization_1, @"======>更新提示")
# @end
def createMFileStr(contentList):
    resultStr = '# import \"'+ fileName +'.h\"\n';
    resultStr = resultStr + '#define _TFTranslationsImplement(v, hc) - (NSString *)v { if (self.hard_code || !_map[@#v]) { return hc; } return _map[@#v]; }\n';
    resultStr = resultStr + '@implementation ' + fileName + '\n';
    for itemList in contentList :
        resultStr = resultStr + '\t_TFTranslationsImplement(' + itemList[0] + ', ' + '@\"' + itemList[2] + '\");\n';
    resultStr = resultStr + '@end';
    return resultStr;

def createFile(folderFilePath, createFileName, contentStr) :
    tempPath = folderFilePath + '/' + createFileName;
    if (tempPath == None) or (contentStr == None) :
        print('写入路径或者写入内容是空的');
        return False;
    fullFile = open(tempPath, 'wr');
    fullFile.write(contentStr);
    fullFile.close;  
    return True; 



#mark main progress
parser = argparse.ArgumentParser();
# , "-o", help="-o output file folder path", type=String, "-n", help="-n file name", type=String
parser.add_argument("-i", help="-i is src file path");
parser.add_argument("-o", help="-o output file folder path");
parser.add_argument("-n", help="-n file name");
args = parser.parse_args();
srcFilePath = args.i;
desFolderPath = args.o;
fileName = args.n;

applicationPath = os.getcwd();
if (srcFilePath == None) :
    srcFilePath = applicationPath + '/CKLocalizable';
if (desFolderPath == None) :
    desFolderPath = applicationPath;
if (fileName == None) :
    fileName = 'TFTranslations';
    

srcFileLines = readFile(srcFilePath);
if(None == srcFileLines) :
    exit();
totalList = parserFileStr(srcFileLines);
srcFileLines.close;

hStr = createHFileStr(totalList);
mStr = createMFileStr(totalList);
createFile(desFolderPath, (fileName + '.h'), hStr);
createFile(desFolderPath, (fileName + '.m'), mStr);