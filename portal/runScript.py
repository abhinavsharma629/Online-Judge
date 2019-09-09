import shlex,subprocess
from subprocess import Popen, PIPE
import os

myinput = open('input.txt')
myoutput = open('output.txt', 'w')
myerror = open('error.txt', 'w')

returncode = 0
runtimeError = 0

choice=(int)(input("Enter Your Language Number:- 1- JAVA, 2- PY, 3- C++, 4- C:- "))

def languageChoice(langCode):
    global compileCode, runCode
    compileCode=""
    runCode=""
    
    if(langCode==1):
        compileCode="javac "+"hello.java"
        runCode="java hello"
    
    elif(langCode==2):
        runCode="py "+"hello.py"

    elif(langCode==3):
        compileCode="g++ "+"hello.cpp -o c++Output"
        runCode="c++Output"
    
    elif(langCode==4):
        compileCode="gcc "+"hello.c -o cOutput"
        runCode="cOutput"

languageChoice(choice)

if(choice!=2):
    try:
        process = subprocess.check_output(compileCode, shell=True)
        process1 = subprocess.Popen(runCode, stdin=myinput, stdout=myoutput, stderr=subprocess.PIPE , universal_newlines=True, shell=True)
        try:
            outs, stderr = process1.communicate(timeout=1)
            if(stderr):
                runtimeError = 1
        except Exception as e:
            process1.terminate()
            returncode = -1
            #print("Timeout", returncode)
    except subprocess.CalledProcessError as e:
        returncode = 1
        #print("Compilation Error")
    if(returncode==0 and runtimeError==1):
        returncode = 2
    
    print(returncode)
    

elif(choice==2):
    process=subprocess.Popen('py hello.py', stdin=myinput, stdout=myoutput, stderr=myerror , universal_newlines=True, shell=True)
    print(process.returncode)