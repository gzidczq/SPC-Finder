
from __future__ import print_function
import sys, os, copy

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

#根据GSP Sequence 查找bug
def findBugsByGSPSequence(fileList,SequenceList,minConf):
   bugList=[]
   bugCount=0
   seCount=str(len(SequenceList))#分析序列数
   usefulSEList=[]#1>conf>minconf的序列列表
   mapFromSEtoBugList=dict()
   trvailRuleCount=0#conf=1的序列书
   lineCount=str(len(fileList))#分析文件行数，即函数数
   for se in SequenceList:
      confirmCount=0
      againstCount=0
      for line in fileList:
        seIndex=0
        lineIndex=0
        while(lineIndex<len(line)):
           if(se[seIndex]==line[lineIndex]):#se当前元素在line中找到匹配到
              seIndex=seIndex+1
              if(seIndex==len(se)):#confirm found
                 confirmCount=confirmCount+1
                 break
           lineIndex=lineIndex+1
        if(seIndex+1==len(se)):#against found 除最后一个元素外，该序列se都在line中，find a bug
           bugStr='Find a bug in: '+str(line)+', against sequence: '+str(se)
           againstCount=againstCount+1
           if(str(se) in mapFromSEtoBugList.keys()):#已有记录
              mapFromSEtoBugList[str(se)].append(bugStr)
           else:#还没有记录
              mapFromSEtoBugList[str(se)]=[bugStr]
      #print(se)
      #print('confirmCount:'+str(confirmCount)+', againstCount:'+str(againstCount))
      if((confirmCount/(confirmCount+againstCount))>=minConf and againstCount!=0):
         usefulSEList.append(str(se))
      if(againstCount==0):         
         trvailRuleCount=trvailRuleCount+1

   #for key in mapFromSEtoBugList:
   #   print(key)
   #   print(mapFromSEtoBugList[key])
   for uSE in usefulSEList:
       for bug in mapFromSEtoBugList[str(uSE)]:
          bugList.append(bug)

   print('findBugsByGSP finished! analysis '+lineCount+' function calls for '+seCount+' sequences, including '+str(len(usefulSEList))+' useful sequence, and '+str(trvailRuleCount)+' sequences with confidence 1. Find '+str(len(bugList))+' Bugs.')
   print('Used sequences:')
   for uSE in usefulSEList:
      print(uSE)
   return bugList
   
#读取GSP生成文件
def loadGSPReslut(fileName):
   GSPFile = open(fileName,'r')
   SequenceList=[]#存放GSP序列的list，每一条序列为一个list
   FPGFile = open(fileName,'r')
   for line in FPGFile:#格式：0.035: <addReply()>  <addReply()>  
      if (line.find(': <')==-1):#该行不是序列格式
         continue
      sequence=[]
      line=line[line.find('<'):]
      line=line.replace('>  <', ',')#去掉空格
      line=line.replace('  \n', '')#去掉行尾
      line=line.replace('<', '')#去掉括号
      line=line.replace('>', '')#去掉括号
      sequence=line.split(',') 
      SequenceList.append(sequence)
  
   return SequenceList
     

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



gspFileName=sys.argv[2] 
SequenceList=loadGSPReslut(gspFileName)
#for se in SequenceList:
#   print(se)

GSPbugList=findBugsByGSPSequence(fileList,SequenceList,0.9)
for bug in GSPbugList:
   print(bug)





