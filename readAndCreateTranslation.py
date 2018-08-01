import os,sys,filecmp,argparse,re,getopt,time

# 从文件流中查找是否有这个字符串 有返回一个数组第一个为哪一行 第二个为这个字符串第一次出现的位置 
def matchStr4File(srcStr, desFile):
    resultPos = [];
    index = 0;
    if(None == srcStr) or (desFile == None):
        return None;
    for itemLine in desFile :
        strPos = itemLine.find(srcStr);
        if(strPos >= 0):
            resultPos.append(index);
            resultPos.append(strPos);
            return resultPos;
        index = index + 1;
    return resultPos;

# 反向遍历list 匹配数组 
def rMatchStr4File(str, lines):
    resultPos = [];
    index = -1;
    for itemLine in lines[::-1] :
        strPos = itemLine.find(str);
        if(strPos >= 0) :
            # 匹配到了数据
            resultPos.append(index);
            resultPos.append(strPos);
            return resultPos;
        index = index - 1;
    return resultPos;

# 根据类名，父类名，内容字符串 创建.h文件字符串内容
def createTranslationClass4hFile(className, superClassName, desStr) : 
    if((superClassName == None) or (len(superClassName) <= 0)):
        superClassName = 'NSObject';

    contentStr = normalStr(className);
    contentStr = contentStr + '#import <Foundation/Foundation.h>\n';
    if(0 != cmp(superClassName, 'NSObject')):
        contentStr = contentStr + '#import \"'+ superClassName +'.h\"\n'
    else:
        contentStr = contentStr + '#define _TFTranslationsImplement(v, hc) - (NSString *)v { if (self.hard_code || !self.map[@#v]) { return hc; } return self.map[@#v]; }\n';
    contentStr = contentStr + '@interface MCTranslation : '+ superClassName +'\n';
    if (cmp(superClassName, 'NSObject') == 0) :
        contentStr = contentStr + '@property (nonatomic, strong) NSDictionary<NSString *, NSString *> *map;\n';
        contentStr = contentStr + '/** 是否使用硬编码代码 */\n';
        contentStr = contentStr + '@property (nonatomic) BOOL hard_code;\n';
        contentStr = contentStr + '/**语言类型**/\n';
        contentStr = contentStr + '@property (nonatomic, assign, readonly) NSInteger languageType;\n';
        contentStr = contentStr + desStr;
    contentStr = contentStr + '\n@end';
    return contentStr;

# 根据类名以及内容创建m文件的字符串内容
def createTranslationClass4mFile(className, desStr) : 
    if (None == className) or (len(className) <= 0):
        print('类名字符串是空的');
        return None;
    contentStr = normalStr(className);
    contentStr = contentStr + '\n#import \"'+ className +'.h\"\n';
    contentStr = contentStr + '@implementation ' + className + '\n';
    if desStr == None :
        desStr = '';
    contentStr = contentStr + desStr;
    contentStr = contentStr + '\n\n@end';
    return contentStr;

# 文件头常规字符串
def normalStr(className):
    curTime = time.localtime(time.time());
    timeStr = str(curTime.tm_year) + '/' + str(curTime.tm_mon) + '/' + str(curTime.tm_mday);
    resultStr = '//  '+ className +'\n';
    resultStr = resultStr + '// \n';
    resultStr = resultStr + '//  Created or change by tsunami on ' + timeStr + '\n';
    resultStr = resultStr + '//  Copyright © '+ str(curTime.tm_year) +'年 haochang. All rights reserved.\n';
    return resultStr;

# 解析文件内容
def parserFileStr(itemLine) :
    vStr = '\"V\":\"';
    oStr = '\",\"O\":\"';
    tStr = '\",\"T\":\"';
    vLen = len(vStr);
    oLen = len(oStr);
    tLen = len(tStr);
    resultList = [];
    # for itemLine in srcStrLines :
    vPos = itemLine.find(vStr);
    oPos = itemLine.find(oStr);
    tPos = itemLine.find(tStr);

    if (vPos < 0) or (oPos < 0) or (tPos < 0):
        return None;

    lastChPos = itemLine.rfind('\"');
    firstStr = itemLine[(vPos + vLen):(oPos)];
    secondStr = itemLine[(oPos + oLen):(tPos)];
    thirdStr = itemLine[(tPos + tLen):(lastChPos)];
    resultList = [firstStr, secondStr, thirdStr];
    return resultList;

def argparseCreate():
    tempParse = argparse.ArgumentParser();
    tempParse.add_argument('--a', action='append', dest='chilFileNameList', default=[],help='enter child File Name List');
    tempParse.add_argument('--s', dest='superClassName', default='MCTranslation', help='param is super file and class name');
    args = tempParse.parse_args();
    return args;

rootPath = os.getcwd();
# #warning test code
# cList = ['CKLocalizable', 'CKLocalizable_english'];
# args = [cList, 'MCTranslation'];
# chilFileNameList = args[0];
# superClassName = args[1];
args = argparseCreate();
chilFileNameList = args.chilFileNameList;
superClassName = args.superClassName;

superFileHPath = rootPath + '/' + superClassName + '.h';
superFileMPath = rootPath + '/' + superClassName + '.m';

# 如果文件不存在先创建 避免下面的操作错误
isExistSuperHFile = os.path.exists(superFileHPath);
isExistSuperMFile = os.path.exists(superFileMPath);
if isExistSuperHFile == False :
    contentStr = createTranslationClass4hFile(superClassName, 'NSObject', '');
    tempFile = open(superFileHPath, 'wr');
    tempFile.write(contentStr);
    tempFile.close();

if False == isExistSuperMFile :
    contentStr = createTranslationClass4mFile(superClassName, '');
    tempFile = open(superFileMPath, 'wr');
    tempFile.write(contentStr);
    tempFile.close();

superFileH = open(superFileHPath);
superFileM = open(superFileMPath);
superFileH.close();
superFileM.close();

superFileH = open(superFileHPath);
superFileM = open(superFileMPath);
superHLinesNum = 0;
for tempLine in superFileH :
    # print('=====>'+ tempLine +'<=====')
    superHLinesNum = superHLinesNum + 1;
superMLinesNum = 0;
for tempLine in superFileM :
    # print('=====>'+ tempLine +'<=====')
    superMLinesNum = superMLinesNum + 1;
resultInsertContentStr_H = '';
resultInsertContentStr_M = '';

for childFileName in chilFileNameList :
    cPath = rootPath + '/' + childFileName;
    cFile = open(cPath);
    cFileLines = cFile;
    willWriteStr = '';
    for cItemLine in cFileLines:
        itemAttr = parserFileStr(cItemLine);
        print('parser data list count is: '+str(itemAttr.count)+'\tThis content is : ', itemAttr);
        if (itemAttr != None) :
            # 第一个参数为属性名
            attrName = itemAttr[0];
            # 第二个参数为key
            keyName = itemAttr[1];
            # 第三个参数为value
            valueName = itemAttr[2];

            # 操作父类文件
            matchPos = matchStr4File(attrName, superFileH);
            if (None == matchPos) or (matchPos.count != 2):
                # 没有匹配到字符串 父类.h文件添加属性 同时 父类.m文件添加初始化值
                isHadTheAttr_H = False;
                if (resultInsertContentStr_H.find(attrName)) > 0:
                    isHadTheAttr_H = True;
                # //头文件插入属性
                hNum = superHLinesNum;
                # /** 原文:更新提示 译文:======>更新提示 */
                insertStr = '/** 原文:'+ keyName + '译文:'+ keyName +' */\n';
                insertStr = insertStr + '@property (nonatomic, strong, readonly) NSString *'+ attrName +';\n';
                resultInsertContentStr_H = resultInsertContentStr_H + insertStr;
                # //执行文件插入函数
                mNum = superMLinesNum;
                insertStr = '\n\t_TFTranslationsImplement('+ attrName +', @\"'+ keyName +'\")\n';
                resultInsertContentStr_M = resultInsertContentStr_M + insertStr;
            
            # 子类操作 .h文件不用写 只写.m文件
            cWriteStr = '\t_TFTranslationsImplement('+ attrName +', @\"'+ valueName +'\")\n';
            willWriteStr = willWriteStr + cWriteStr;
        hStr = createTranslationClass4hFile(childFileName, superClassName, '');
        mStr = createTranslationClass4mFile(childFileName, willWriteStr);
        hFilePath = rootPath + '/' + childFileName + '.h';
        mFilePath = rootPath + '/' + childFileName + '.m';
        hFile = open(hFilePath, 'wr');
        mFile = open(mFilePath, 'wr');
        hFile.write(hStr);
        mFile.write(mStr);
        hFile.close();
        mFile.close();

hContentStr = '';
mContentStr = '';
superFileH.close();
superFileM.close();
superFileH = open(superFileHPath);
superFileM = open(superFileMPath);
for itemLine in superFileH:
    if (itemLine.find('@end') == 0):
        hContentStr = hContentStr + resultInsertContentStr_H;
        hContentStr = hContentStr + itemLine;
    else:
        hContentStr = hContentStr + itemLine;
        # tempPos = itemLine.find('/** 原文:');
        # tempPos2 = itemLine.find('@property (nonatomic, strong, readonly) NSString *');
        # if(tempPos == 0) or (tempPos2 == 0) :
        #     hContentStr = hContentStr + itemLine;

for itemLine in superFileM:
    if (itemLine.find('@end') >= 0):
        mContentStr = mContentStr + resultInsertContentStr_M;
        mContentStr = mContentStr + itemLine;
    else:
        mContentStr = mContentStr + itemLine;
superFileH.close();
superFileM.close();
overHFo = open(superFileHPath, 'wr');
overHFo.write(hContentStr);
overHFo.close();
overMFo = open(superFileMPath, 'wr');
overMFo.write(mContentStr);
overMFo.close();


                    