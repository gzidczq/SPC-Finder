
from __future__ import print_function
import sys, os, copy

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

#根据FPRules 查找bug
def findBugsByFPRules(fileList,FPRuleList):
   bugList=[]
   bugCount=0
   ruleCount=str(len(FPRuleList))#分析规则数
   trvailRuleCount=0#conf=1的规则书
   lineCount=str(len(fileList))#分析文件行数，即函数数
   for rule in FPRuleList:
      ruleLeftSet=set(rule[0])
      confirmCount=0
      againstCount=0
      for line in fileList:
         lineSet=set(line[0:len(line)-1])#每一行所有函数调用组成到集合
         #print(lineSet)
         leftContain=True
         for rls in ruleLeftSet:
            if(rls not in line):#ruleLeftSet不在该行中，不需要分析该rule
               leftContain=False
               break
         if(leftContain == True):#rule 左边包含在line中，检查右边是否包含
            rightContain=True
            ruleRightSet=set(rule[1])
            for rrs in ruleRightSet:
               if(rrs not in lineSet):#right item not contain in  rule
                  rightContain=False
                  break
            if(rightContain==True):#confirm rule 
               confirmCount=confirmCount+1
            else:#against rule ,find a bug
               againstCount=againstCount+1
               bugCount=bugCount+1
               bugStr=str(bugCount)+', Find a bug in: '+str(line)+', against rule: '+str(rule)
               bugList.append(bugStr)
      if(againstCount==0):
         trvailRuleCount=trvailRuleCount+1
      print(rule)
      print('conf:'+str(confirmCount/(confirmCount+againstCount))+','+str(confirmCount)+'/'+str(confirmCount+againstCount))   
   print('findBugsByFPRules finished! analysis '+lineCount+' function calls for '+ruleCount+' rules, including '+str(trvailRuleCount)+' rules with confidence 1. Find '+str(len(bugList))+' Bugs.')
   return bugList


#读取FPGrowth生成文件     
def loadFPGReslut(fileName):
   FPRuleList=[]#存放FPRule的list，每一条rule为一个两个元素的list，第二个元素是‘=>’右边，第一个为‘=>’左边的元素
   FPGFile = open(fileName,'r')
   for line in FPGFile:
      FPRule=[]
      line=line.replace(' ', '')#去掉空格
      line=line.replace('[', '')#去掉括号
      line=line.replace(']', '')#去掉括号
      line=line.replace('=T', '')#去掉=T
      if (line.find('-->')==-1):#该行不是关联规则格式
         continue
      #若是关联规则格式
      preLine=line[0:line.find('-->')]#关联规则前半部分
      FPRuleLeft=preLine.split(',') 
      subLine=line[line.find('-->')+3:line.find('(confidence:')]#关联规则后半部分
      FPRuleRight=subLine.split(',') 

      FPRule.append(FPRuleLeft) 
      FPRule.append(FPRuleRight) 
      FPRuleList.append(FPRule)

   return FPRuleList

mappingFileName=sys.argv[1] 
mappingFile = open(mappingFileName,'r')
fileList=[]#所有行存到fileList中，每一个元素为一个lineList
for line in mappingFile:
   lineList=[]#每一行存一个list 前面为func 信息 最后一个元素为位置信息
   preLine=line[0:line.find('@')]
   lineList = preLine.split(',')  
   subLine=line[line.find('@'):len(line)-1]
   lineList.append(subLine)
   temp=copy.deepcopy(lineList)
   fileList.append(temp)

ruleFileName=sys.argv[2] 
FPRuleList=loadFPGReslut(ruleFileName)
FPbugList=findBugsByFPRules(fileList,FPRuleList)
for bug in FPbugList:
   print(bug)





