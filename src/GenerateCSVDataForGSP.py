
from __future__ import print_function
import sys, os

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

#文件类型

functionSet=set()
fileCount=0
funcCount=0
funcDefCount=0
funcList=list(functionSet)

#分析每一行
def analysisLine(line):
   print(line)
   global funcCount 
   global funcDefCount 
   if('--------------Analysis' in line):
       funcDefCount = funcDefCount+1
   if('Funcation Call:' in line):
      pos = line.find('()')
      if(pos>15):
         #print(line[16:pos+2])  
         #print(line)
         funcCount=funcCount+1
         functionSet.add(str(line[16:pos+2]))    

#读取reulst文件
def readResultFile(file):
   input = open(file, 'r')
   for line in input:
     analysisLine(line)

#输出表头 for RM
def outputFuncCallasTitle():
   global funcList 
   #funcList = list(functionSet)
   outStr='id,custom,'
   for func in funcList:
      outStr=outStr+str(func)+',' 
   outFile.write(outStr[0:len(outStr)-1]+'\n')


#输出每一个函数内的函数调用
index=1
lineId=1
def outputFuncCallInFunc(file):
   global funcList,index,lineId
   input = open(file, 'r')
   dataStr=''
   includeFuncList=[]
   posStr=''
   for line in input:
      if('--------------Analysis' in line):
         posStr=line[line.find('Analysis-'):len(line)-1]
         continue
      elif('---------------finish' in line):  
            dataStr=dataStr[0:len(dataStr)-1]+'@'+posStr+'....@'+str(index)+'\n'
            index=index+1
            mappingFile.write(dataStr)
            dataStr=''
            continue
      elif('Funcation Call:' in line):
         pos = line.find('()')
         funcName=str(line[16:pos+2])
         if(funcName in funcList):
            funStr=''
            for f in funcList:
               if f == funcName:
                  funStr=funStr+'1,'
               else:
                  funStr=funStr+'0,'
            outFile.write(str(lineId)+','+str(index)+','+funStr[0:len(funStr)-1]+'\n')
            lineId=lineId+1
            dataStr=dataStr+funcName+','  
         #else:
         #   dataStr=funcName+'not in list'
      
      
      


outputFileDic = os.getcwd()
if (len(sys.argv)>1):
   outputFileDic = os.path.join(outputFileDic,sys.argv[1])
print(outputFileDic)

#currentDir = sys.path[0]
dirlist = os.listdir(outputFileDic)
for line in dirlist:
   #if (os.path.isfile(line)):
   fileString = str(line)
   dotPos = fileString.rfind('.') 
   fileType = fileString[dotPos:]
   #print(fileType)
   if(fileType=='.result'):#result 文件
      #print(line)
      fileCount=fileCount+1
      fullPathFile = os.path.join(outputFileDic,line)
      readResultFile(fullPathFile)

funcList = sorted(list(functionSet))
#print(funcList)
print('read '+str(fileCount)+' files, '+str(funcDefCount)+' Function Defs, '+str(funcCount)+' function calls, contain  '+str(len(functionSet))+' unrepeat function calls')

preName=sys.argv[1][0:len(sys.argv[1])-1]
csvfFileName=preName+'.csv'
mappingFileName=preName+'.sequenceMapping'
outFile=open(csvfFileName,'w') 
mappingFile=open(mappingFileName,'w') 

outputFuncCallasTitle()


for line in dirlist:
   fileString = str(line)
   dotPos = fileString.rfind('.') 
   fileType = fileString[dotPos:]
   #print(fileType)
   if(fileType=='.result'):#result 文件
      #print(line)
      #fileCount=fileCount+1
      fullPathFile = os.path.join(outputFileDic,line)
      outputFuncCallInFunc(fullPathFile)

outFile.close()
mappingFile.close()


'''
for fpathe,dirs,fs in os.walk(outputFileDic):
  for f in fs:
    fileString = str(f)
    dotPos = fileString.rfind('.') 
    fileType = fileString[dotPos:]
    #print(fileType)
    if(fileType=='.result'):#result 文件
       print(fileType)
       #readResultFile(f)
'''


