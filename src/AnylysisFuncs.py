#-----------------------------------------------------------------
# pycparser: explore_ast.py
#
# This example demonstrates how to "explore" the AST created by
# pycparser to understand its structure. The AST is a n-nary tree
# of nodes, each node having several children, each with a name.
# Just read the code, and let the comments guide you. The lines
# beginning with #~ can be uncommented to print out useful
# information from the AST.
# It helps to have the pycparser/_c_ast.cfg file in front of you.
#
# Copyright (C) 2008-2015, Eli Bendersky
# License: BSD
#-----------------------------------------------------------------
from __future__ import print_function
import sys

# This is not required if you've installed pycparser into
# your site-packages/ with setup.py
#
sys.path.extend(['.', '..'])

from pycparser import c_parser, c_ast, parse_file

# This is some C source to parse. Note that pycparser must begin
# at the top level of the C file, i.e. with either declarations
# or function definitions (this is called "external declarations"
# in C grammar lingo)
#
# Also, a C parser must have all the types declared in order to
# build the correct AST. It doesn't matter what they're declared
# to, so I've inserted the dummy typedef in the code to let the
# parser know Hash and Node are types. You don't need to do it
# when parsing real, correct C code.
#
'''
text = r"""
    typedef int Node, Hash;

    void HashPrint2(Hash* hash, void (*PrintFunc)(char*, char*))
    {
        unsigned int i;

        if (hash == NULL || hash->heads == NULL)
            return;

        for (i = 0; i < hash->table_size; ++i)
        {
            Node* temp = hash->heads[i];

            while (temp != NULL)
            {
                PrintFunc(temp->entry->key, temp->entry->value);
                temp = temp->next;
            }
        }
    }
"""
'''

text = r"""
    typedef int Node, Hash;

    void HashPrint2(Hash* hash, void (*PrintFunc)(char*, char*))
    {
        unsigned int i;
        i=i+1;

        if (printf("ddd") == printf("aaa") ){
           printf("adf");
           hash++;
        }
        else
           printf("bcd");
        

        for (i = 1; i < hash->table_size; ++i)
        {
            Node* temp = hash->heads[i];
            Node* temp2 = PrintFunc("adf");
            printf("adf");

            while (entry != NULL)
            {
                PrintFunc(temp->entry->key, temp->entry->value);
                temp = temp->next;
            }
        }
    }
"""

# Create the parser and ask to parse the text. parse() will throw
# a ParseError if there's an error in the code
#
#parser = c_parser.CParser()


#print(len(sys.argv))


#ast = parser.parse(text, filename='<none>')

# Uncomment the following line to see the AST in a nice, human
# readable way. show() is the most useful tool in exploring ASTs
# created by pycparser. See the c_ast.py file for the options you
# can pass it.
#
#~ ast.show()

# OK, we've seen that the top node is FileAST. This is always the
# top node of the AST. Its children are "external declarations",
# and are stored in a list called ext[] (see _c_ast.cfg for the
# names and types of Nodes and their children).
# As you see from the printout, our AST has two Typedef children
# and one FuncDef child.
# Let's explore FuncDef more closely. As I've mentioned, the list
# ext[] holds the children of FileAST. Since the function
# definition is the third child, it's ext[2]. Uncomment the
# following line to show it:
#
#~ print('ast.ext[2].show()')
#~ ast.ext[2].show()

def visitSubBloc(sbloc):
    if (sbloc is None):
       return
    sblocTyp = type(sbloc)
    #print(sblocTyp)
    if(sblocTyp == c_ast.Compound and sbloc.block_items is not None):
       for ssbloc in sbloc.block_items:
          recursiveVist(ssbloc)
    else:
       recursiveVist(sbloc)

#递归遍历bloc内部

def recursiveVist(bloc):
    if (bloc is None):
       return
    #print('begin current block...')
    #bloc.show()
    #print('end current block...')
    blocTyp = type(bloc)
    #print(blocTyp)
     
    if(blocTyp == c_ast.FuncCall):
       nameBloc = bloc.name
       nameTyp=type(nameBloc)
       #bloc.show()
       if(nameTyp == c_ast.StructRef):
          subNameBloc = bloc.name.field
          subNameTyp=type(subNameBloc)
          if(subNameTyp == c_ast.StructRef):
             print('Funcation Call: %s() at %s, nameTyp %s' % (subNameBloc.field.name, bloc.coord, str(nameTyp)))     
          else:
             print('Funcation Call: %s() at %s, nameTyp %s' % (bloc.name.field.name, bloc.coord, str(nameTyp)))       
       elif(nameTyp!=c_ast.UnaryOp and nameTyp!= c_ast.Cast):#函数指针
          print('Funcation Call: %s() at %s, nameTyp %s' % (bloc.name.name, bloc.coord, str(nameTyp)))
       #if(str(bloc.coord).find('redis/src/object.c')>-1):
       #   bloc.show()

    #if
    elif (blocTyp == c_ast.If):
       #print('begin show if block...')
       #bloc.show()
       #print('begin cond block...')
       visitSubBloc(bloc.cond)  
       #print('begin iftrue block...')
       visitSubBloc(bloc.iftrue)
       #print('begin iffalse block...')
       visitSubBloc(bloc.iffalse)  
       #print('end iffalse block...')
      
    #二元操作
    elif (blocTyp == c_ast.BinaryOp):  
       visitSubBloc(bloc.left)  
       visitSubBloc(bloc.right)
      

    #for
    elif (blocTyp == c_ast.For):    
       visitSubBloc(bloc.init)
       visitSubBloc(bloc.cond)
       visitSubBloc(bloc.next)
       visitSubBloc(bloc.stmt)

    #Assignment
    elif (blocTyp == c_ast.Assignment):
       #print('begin Assignment block...')
       #bloc.show()    
       #print('end Assignment block...')
       visitSubBloc(bloc.lvalue)
       #print('begin Assignment lvalue block...')
       #bloc.lvalue.show()    
       #print('end Assignment lvalue block...')
       visitSubBloc(bloc.rvalue)
       #print('begin Assignment rvalue block...')
       #bloc.rvalue.show()    
       #print('end Assignment rvalue block...')
    
    #While
    elif (blocTyp == c_ast.While):    
       visitSubBloc(bloc.cond)
       visitSubBloc(bloc.stmt)
    
    #DoWhile
    elif (blocTyp == c_ast.DoWhile):    
       visitSubBloc(bloc.cond)
       visitSubBloc(bloc.stmt)

    #UnaryOp
    elif (blocTyp == c_ast.UnaryOp):
      visitSubBloc(bloc.expr)
     
    #StructRef
    elif (blocTyp == c_ast.StructRef):
      visitSubBloc(bloc.name)
      visitSubBloc(bloc.field)
     
    #StructRef
    elif (blocTyp == c_ast.Decl):
      visitSubBloc(bloc.init)

    #Return
    elif (blocTyp == c_ast.Return):
      visitSubBloc(bloc.expr)

    #Cast
    elif (blocTyp == c_ast.Cast):
      visitSubBloc(bloc.expr)

    #Switch
    elif (blocTyp == c_ast.Switch):
      visitSubBloc(bloc.cond)
      visitSubBloc(bloc.stmt)

    #Case
    elif (blocTyp == c_ast.Case):
      visitSubBloc(bloc.expr)
      visitSubBloc(bloc.stmts)

    #ExprList
    elif (blocTyp == c_ast.ExprList):
      visitSubBloc(bloc.exprs)
       
    #TernaryOp
    elif (blocTyp == c_ast.TernaryOp):
       #print('begin TernaryOp block...')
       #bloc.show()    
       #print('end TernaryOp block...')
       visitSubBloc(bloc.cond)  
       visitSubBloc(bloc.iftrue)
       visitSubBloc(bloc.iffalse) 

    #InitList
    elif (blocTyp == c_ast.InitList):
      visitSubBloc(bloc.exprs)

    #Label
    elif (blocTyp == c_ast.Label):
      visitSubBloc(bloc.stmt)

     
    #Typename
    elif (blocTyp == c_ast.Typename):
      visitSubBloc(bloc.name)

    #Default
    elif (blocTyp == c_ast.Default):
      visitSubBloc(bloc.stmts)


    elif (blocTyp == c_ast.ID or blocTyp == c_ast.Constant or blocTyp == c_ast.ArrayRef or str(blocTyp) == "<class 'NoneType'>" or blocTyp == c_ast.Continue or str(blocTyp) == "<class 'list'>" or blocTyp == c_ast.Goto or blocTyp == c_ast.Break or blocTyp == c_ast.EmptyStatement):
      temp=1
    
    else:
       print('unknow...')
       print(str(blocTyp))
       #bloc.show()

#遍历函数体内部
def insideFunc(func):
     #func.show()
     funcContent = func.body
     if (funcContent.block_items is None):
         return
     i=0
     for bloc in funcContent.block_items:
         #print('block %d' % (i))
         recursiveVist(bloc)
         i=i+1
     #firstBloc = funcContent.block_items[0]
     #firstBlocTyp = type(firstBloc)
     #print(firstBlocTyp)
     #print(firstBloc.children())
     #for bloc in firstBloc.children():
     #    bloc.show()
     #if(firstBlocTyp==c_ast.Decl):
         #childrenList = firstBloc.children()
         #childrenList.show()
         #for child in childrenList:
          #   child.show()

def traverseFuc(func):
     #检查是否本文件内的函数
     fucPos = str(func.decl.coord)
     linePos = fucPos.find(':')
     fucFile = fucPos[0:linePos]
     lineNo = fucPos[linePos+1:]
     slashPos = fucFile.rfind('/')
     fucFile = fucFile[slashPos+1:]
     #if(fucFile=='<none>'):
     #print('fucFile:'+fucFile)
     if(fucFile==fullFileName):
        print('--------------Analysis-%s-@%s@line: %s.....' % (func.decl.name, fucFile, lineNo))
        insideFunc(func)
        print('---------------finish-------------------------------')




if len(sys.argv) > 1:
        filename  = sys.argv[1]
        #print(filename)
else:
        print('未提供输入文件')

#获取原C程序文件名
print('filename:'+filename)
dashPos = filename.rfind('_')
fullFileName = 'lua/src/'+filename[0:dashPos]+'.c'
slashPos = fullFileName.rfind('/')
fullFileName = fullFileName[slashPos+1:]

print('fullFileName:'+fullFileName)
ast = parse_file(filename, use_cpp=True, cpp_args=r'-Iutils/fake_libc_include')
#ast.show()

for decl in ast.ext:
  typ = type(decl)
  if(typ==c_ast.FuncDef):
     traverseFuc(decl)



