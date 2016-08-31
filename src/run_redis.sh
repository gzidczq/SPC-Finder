#!/bin/bash

echo 'sudo ./compile_redis.sh redis/src redis_pp >InfoCompile'
echo '使用compile.sh批量编译，第一个参数为输入文件夹路径，第二个参数为输出文件路径.....'
START=`date +%s%N`
sudo ./compile_redis.sh redis/src redis_pp >InfoCompile
echo 'sudo ./compile_redis.sh redis/src/modules redis_pp >InfoCompile'
sudo ./compile_redis.sh redis/src/modules redis_pp >InfoCompile
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '编译完成，耗时：'$costTime 'ms'

#不分析cluster.c文件
cd redis_pp
rm -rf cluster_pp.c
cd ..

echo 'sudo ./GetFuncCalls.sh redis_pp redis_Funcs >infoGenerateFuncCall'
echo '使用GetFuncCalls.sh 批量生成函数调用信息，第一个参数为输入文件夹路径，第二个参数为输出文件路径.....'
START=`date +%s%N`
sudo ./GetFuncCalls.sh redis_pp redis_Funcs >infoGenerateFuncCall
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '函数调用信息生成完成，耗时：'$costTime 'ms'


echo 'python GenerateFuncData.py redis_Funcs/ >InfoFuncSet'
echo '使用GenerateFuncData.py生成函数调用集，生成*.arff和×.setMapping文件,第一个参数为输入文件夹路径，第二个参数为输出文件路径.....'
START=`date +%s%N`
python GenerateFuncData.py redis_Funcs/ >InfoFuncSet
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '函数调用集生成完成，耗时：'$costTime 'ms'


echo 'python GenerateCSVDataForGSP.py redis_Funcs/ >InfoFuncSeq'
echo 'GenerateCSVDataForGSP.py生成函数调用序列，生成*.csv和×.sequenceMapping文件，第一个参数为输入文件夹路径，第二个参数为输出文件路径.....'
START=`date +%s%N`
python GenerateCSVDataForGSP.py redis_Funcs/ >InfoFuncSeq
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '函数调用序列生成完成，耗时：'$costTime 'ms'


echo 'python AnalysisBugsBySet.py redis_Funcs.setMapping FPGrowthResult_redis >InfoBugBySet'
echo '使用关联规则查找bug....'
START=`date +%s%N`
python AnalysisBugsBySet.py redis_Funcs.setMapping FPGrowthResult_redis >InfoBugBySet
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '使用关联规则查找bug完成，耗时：'$costTime 'ms'


echo 'python AnalysisBugsBySequence.py redis_Funcs.sequenceMapping GSPResult_redis >InfoBugBySequence'
echo '使用序列模式查找bug....'
START=`date +%s%N`
python AnalysisBugsBySequence.py redis_Funcs.sequenceMapping GSPResult_redis >InfoBugBySequence
END=`date +%s%N`
costTime=$((($END-$START)/1000000))
echo '使用序列模式查找bug完成，耗时：'$costTime 'ms'



