#!/bin/bash

#创建输出目录
if [ -d $2 ]
  then
  echo '输出目录' $2 '已存在'
else
  echo '创建输出目录' $2 
  mkdir $2
  sudo chmod 777 $2
fi

test=0
for file in ./$1/* ;do
    #((test++))
    #if ((test>50)); then continue
    #fi
    echo $file
    dir=${file%/*}
    fileName=${file##*/}
    echo "python AnylysisFuncs.py $file >$2/$fileName.result"
    python AnylysisFuncs.py $file >$2/$fileName.result
    #cp -p $file ./$2
done

