
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

#输出functioncallDef for weka
def outputFuncCallDefs():
   global funcList 
   funcList = list(functionSet)
   print("@relation 'FunctionCalls'")
   for func in funcList:
      print(str(funcList.index(func))+','+str(func))   
      outFile.write('@attribute '+str(func)+' {F, T}\n')


#输出每一个函数内的函数调用
index=1
def outputFuncCallInFunc(file):
   global funcList,index
   input = open(file, 'r')
   dataStr=''
   mappingStr=''
   funcIndexList=[]
   posStr=''
   for line in input:
      if('--------------Analysis' in line):
         posStr=line[line.find('Analysis-'):len(line)-1]
         continue
      elif('---------------finish' in line):  
         if(len(funcIndexList)>0):
            funcIndexList=list(set(funcIndexList))
            funcIndexList.sort()
            for fi in funcIndexList:
               mappingStr=mappingStr+str(funcList[fi])+',' 
               dataStr=dataStr+str(fi)+' T,' 
            mappingFile.write(mappingStr[:len(mappingStr)-1]+'@'+posStr+'@index:'+str(index)+'\n')
            outFile.write('{'+dataStr[:len(dataStr)-1]+'}\n')
            index=index+1
            dataStr=''
            mappingStr=''
            funcIndexList=[]
      elif('Funcation Call:' in line):
         pos = line.find('()')
         funcName=str(line[16:pos+2])
         if(funcName in funcList):
            funcIndex = funcList.index(funcName)
            funcIndexList.append(funcIndex)
            #dataStr=dataStr+str(funcIndex)+' T,'  
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

funcList = list(functionSet)
print('read '+str(fileCount)+' files, '+str(funcDefCount)+' Function Defs, '+str(funcCount)+' function calls, contain  '+str(len(functionSet))+' unrepeat function calls')

preName=sys.argv[1][0:len(sys.argv[1])-1]
arffFileName=preName+'.arff'
mappingFileName=preName+'.setMapping'
outFile=open(arffFileName,'w') 
mappingFile=open(mappingFileName,'w') 
outFile.write("@relation 'FunctionCalls'\n")
outputFuncCallDefs()
outFile.write("@data\n")



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


