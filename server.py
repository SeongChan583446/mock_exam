from socket import *
import pymysql
import pickle
import threading
from time import sleep

IDList = []
clntThread = []
exitFlag = []
serverChattSock = []
chattSockList = []

def joinMem(sock):
    flag = 0
    data = sock.recv(1024)
    data_arr = pickle.loads(data)
    ID = data_arr[0]
    PW = data_arr[1]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select PW from userinfo where ID = '"+ID+"';"    
    curs.execute(sql)
    rows = curs.fetchall()
    if len(rows) == 0:
        sql = "insert into userinfo(ID,PW) values('"+ID+"','"+PW+"');"
        curs.execute(sql)
        conn.commit()
        flag = 1
    sock.send((repr(flag)).encode('utf-8'))
    conn.close()    
    
def login(sock,index):
    global IDList
    flag = 0
    data = sock.recv(1024)
    data_arr = pickle.loads(data)
    ID = data_arr[0]
    PW = data_arr[1]
    
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select PW, concheck from userinfo where ID = '"+ID+"';"    
    curs.execute(sql)
    rows = curs.fetchall()
    if len(rows) == 0:
        flag = 1
    else:
        if rows[0].get('PW') != PW:
            flag = 2
        else:
            if rows[0].get('concheck') == 1:
                flag = 3
    sock.send((repr(flag)).encode('utf-8'))
    if flag == 0:
        IDList[index] = ID
        sql = "update userinfo set concheck = 1 where ID = '"+ID+"';"
        curs.execute(sql)
        conn.commit()

        index_arr = (index,)
        data = pickle.dumps(index_arr)
        sock.send(data)
        
        chattSock, chattAddr = serverChattSock[index].accept()
        print(str(chattAddr),"에서 접속하였습니다.")
        chattSockList[index] = chattSock

    conn.close()
        
    return flag

def logout(ID,index):
    global IDList
    global chattSockList
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "update userinfo set concheck = 0 where ID = '"+ID+"';"
    curs.execute(sql)
    conn.commit()
    conn.close()
    arr = ("aa","aa")
    data = pickle.dumps(arr)
    chattSockList[index].send(data)
    IDList[index] = ""

def submit(sock,ID):
    flag = 0
    data = sock.recv(1024)
    subjectInfo = pickle.loads(data)
    subjectName = subjectInfo[0]
    subjectOrder = subjectInfo[1]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select count(sno) from subject where sname = '"+subjectName+"' and sorder = '"+subjectOrder+"';"
    curs.execute(sql)
    rows = curs.fetchall()
    if rows[0].get('count(sno)') == 0:
        flag = 1
        sql = "select count(sno) from subject;"
        curs.execute(sql)
        rows2 = curs.fetchall()
        sno = rows2[0].get('count(sno)')
        sql = "insert into subject(sno,sname,sorder,submit_user) values("+repr(sno)+",'"+subjectName+"','"+subjectOrder+"','"+ID+"');"
        curs.execute(sql)
        conn.commit()
    else:
        print("이미 존재하는 과목입니다.")
    conn.close()
    sock.send(repr(flag).encode('utf-8'))

def saveProblem(sock,ID,menu):
    sql = ""
    data = sock.recv(2048)
    problemInfo = pickle.loads(data)
    subjectName = problemInfo[0]
    subjectOrder = problemInfo[1]
    problem = problemInfo[2]
    problemScore = problemInfo[3]
    answer = problemInfo[4]
    pbool = problemInfo[5]
    if pbool == True:
        choiceNum1 = problemInfo[6]
        choiceNum2 = problemInfo[7]
        choiceNum3 = problemInfo[8]
        choiceNum4 = problemInfo[9]
        ptype = "true"
    else:
        choiceNum1 = ""
        choiceNum2 = ""
        choiceNum3 = ""
        choiceNum4 = ""
        ptype = "false"
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql2 = "select sno from subject where sname = '"+subjectName+"' and sorder = '"+subjectOrder+"';"
    curs.execute(sql2)
    rows = curs.fetchall()
    sno = rows[0].get('sno')
    if menu == 6:
        sql2 = "select count(pno) from problem where sno = "+repr(sno)+";"
        curs.execute(sql2)
        rows2 = curs.fetchall()
        pno = rows2[0].get('count(pno)')
        sql = "insert into problem(pno,sno,ptext,panswer,pscore,ptype,pchoice1,pchoice2,pchoice3,pchoice4) \
            values("+repr(pno+1)+","+repr(sno)+",'"+problem+"','"+answer+"','"+problemScore+"',"+ptype+",'"+choiceNum1+"','"+choiceNum2+"','"+choiceNum3+"','"+choiceNum4+"');"
    else:
        problemNum_arr = sock.recv(1024)
        problemNum = pickle.loads(problemNum_arr)
        pno = problemNum[0]
        sql = "update problem set ptext = '"+problem+"', panswer = '"+answer+"', pscore = '"+problemScore+"', ptype = "+ptype+", pchoice1 = '"+choiceNum1+"', pchoice2 = '"+choiceNum2+"', pchoice3 = '"+choiceNum3+"', pchoice4 = '"+choiceNum4+"' \
            where sno = "+repr(sno)+" and pno = "+pno+";"
    curs.execute(sql)
    conn.commit()
    conn.close()

def reviseProblem(sock,ID):
    flag = 0
    data = sock.recv(1024)
    subjectInfo = pickle.loads(data)
    subjectName = subjectInfo[0]
    subjectOrder = subjectInfo[1]
    problemNum = subjectInfo[2]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select count(sno) from subject where sname = '"+subjectName+"' and sorder = '"+subjectOrder+"';"
    curs.execute(sql)
    rows = curs.fetchall()
    existSubject = rows[0].get('count(sno)')
    existSubject_arr = (existSubject,)
    data = pickle.dumps(existSubject_arr)
    sock.send(data)
    if existSubject > 0:
        sql = "select sno, submit_user from subject where sname = '"+subjectName+"'and sorder = '"+subjectOrder+"';"
        curs.execute(sql)
        rows = curs.fetchall()
        submit_ID = rows[0].get('submit_user')
        if ID == submit_ID:
            flag = 1
            sock.send(repr(flag).encode('utf-8'))
            sno = rows[0].get('sno')
            sql = "select count(pno) from problem where sno = "+repr(sno)+";"
            curs.execute(sql)
            rows = curs.fetchall()
            pnoCount = rows[0].get('count(pno)')
            pno_arr = (pnoCount,)
            data = pickle.dumps(pno_arr)
            sock.send(data)
            if int(problemNum) > 0 and int(problemNum) <= pnoCount:
                sql = "select ptext, panswer, pscore, ptype, pchoice1, pchoice2, pchoice3, pchoice4 from problem where sno = "+repr(sno)+" and pno = "+problemNum+";"
                curs.execute(sql)
                rows2 = curs.fetchall()
                problemInfo = (rows2[0].get('ptext'),rows2[0].get('panswer'),rows2[0].get('pscore'),rows2[0].get('ptype'),rows2[0].get('pchoice1'),rows2[0].get('pchoice2'),rows2[0].get('pchoice3'),rows2[0].get('pchoice4'))
                problemInfo_arr = pickle.dumps(problemInfo)
                sock.send(problemInfo_arr)
            else:
                print("문항번호가 존재하지 않습니다.")
        else:
            sock.send(repr(flag).encode('utf-8'))
            print("수정 권한이 없는 유저입니다.")
    else:
        print("문제가 존재하지 않습니다.")
    conn.close()

def removeProblem(sock,ID):
    flag = 0
    data = sock.recv(1024)
    subjectInfo = pickle.loads(data)
    subjectName = subjectInfo[0]
    subjectOrder = subjectInfo[1]
    problemNum = subjectInfo[2]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)

    sql = "select count(sno) from subject where sname = '"+subjectName+"' and sorder = '"+subjectOrder+"';"
    curs.execute(sql)
    rows = curs.fetchall()
    existSubject = rows[0].get('count(sno)')
    existSubject_arr = (existSubject,)
    data = pickle.dumps(existSubject_arr)
    sock.send(data)
    if existSubject > 0:
        sql = "select sno, submit_user from subject where sname = '"+subjectName+"'and sorder = '"+subjectOrder+"';"
        curs.execute(sql)
        rows = curs.fetchall()
        submit_ID = rows[0].get('submit_user')
        if ID == submit_ID:
            flag = 1
            sock.send(repr(flag).encode('utf-8'))
            sno = rows[0].get('sno')
            sql = "select count(pno) from problem where sno = "+repr(sno)+";"
            curs.execute(sql)
            rows = curs.fetchall()
            pnoCount = rows[0].get('count(pno)')
            pno_arr = (pnoCount,)
            data = pickle.dumps(pno_arr)
            sock.send(data)
            if int(problemNum) > 0 and int(problemNum) <= pnoCount:
                sql = "delete from problem where sno = "+repr(sno)+" and pno = "+problemNum+";"
                curs.execute(sql)
                conn.commit()
                sql = "update problem set pno = pno-1 where sno = "+repr(sno)+" and pno > "+problemNum+";"
                curs.execute(sql)
                conn.commit()
            else:
                print("문항번호가 존재하지 않습니다.")
        else:
            sock.send(repr(flag).encode('utf-8'))
            print("삭제 권한이 없는 유저입니다.")    
    else:
        print("문제가 존재하지 않습니다.")
    conn.close()

def addProblem(sock,ID):
    flag = 0
    data = sock.recv(1024)
    subjectInfo = pickle.loads(data)
    subjectName = subjectInfo[0]
    subjectOrder = subjectInfo[1]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select count(sno) from subject where sname = '"+subjectName+"' and sorder = '"+subjectOrder+"';"
    curs.execute(sql)
    rows = curs.fetchall()
    existSubject = rows[0].get('count(sno)')
    existSubject_arr = (existSubject,)
    data = pickle.dumps(existSubject_arr)
    sock.send(data)
    if existSubject > 0:
        sql = "select sno, submit_user from subject where sname = '"+subjectName+"'and sorder = '"+subjectOrder+"';"
        curs.execute(sql)
        rows = curs.fetchall()
        submit_ID = rows[0].get('submit_user')
        if ID == submit_ID:
            flag = 1
            sock.send(repr(flag).encode('utf-8'))
        else:
            sock.send(repr(flag).encode('utf-8'))
            print("수정 권한이 없는 유저입니다.")
    else:
        print("문제가 존재하지 않습니다.")
    conn.close()

def printSubjectName(sock):
    flag = 0
    subjectNameList = []
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select count(sname) from subject;"
    curs.execute(sql)
    countRows = curs.fetchall()
    if countRows[0].get('count(sno)') != 0:
        flag = 1
    sock.send(repr(flag).encode('utf-8'))
    if flag == 1:
        sql = "select sname from subject order by sname asc;"
        curs.execute(sql)
        rows = curs.fetchall()
        subjectNameList.append(rows[0].get('sname'))
        for i in range(len(rows)):
            if subjectNameList[-1] != rows[i].get('sname'):
                subjectNameList.append(rows[i].get('sname'))
        subjectNameList_arr = pickle.dumps(subjectNameList)
        sock.send(subjectNameList_arr)
    else:
        print("해당 과목이 존재하지 않습니다")
        
    conn.close()

def printSubjectOrder(sock):
    subjectOrderList = []
    data = sock.recv(1024)
    subjectN_arr = pickle.loads(data)
    subjectN = subjectN_arr[0]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select count(sno) from subject where sname = '"+subjectN+"';"
    curs.execute(sql)
    rows = curs.fetchall()
    countSno = rows[0].get('count(sno)')
    data = (countSno,)
    countSno_arr = pickle.dumps(data)
    sock.send(countSno_arr)
    if countSno > 0:
        sql = "select sorder from subject where sname = '"+subjectN+"';"
        curs.execute(sql)
        rows = curs.fetchall()
        for i in range(len(rows)):
            subjectOrderList.append(rows[i].get('sorder'))
        subjectOrderList_arr = pickle.dumps(subjectOrderList)
        sock.send(subjectOrderList_arr)
    else:
        print("해당 시험명이 존재하지 않습니다.")
    conn.close()

def printProblemInfoAndEnterAnswer(sock,ID):
    pchoice1 = ""
    pchoice2 = ""
    pchoice3 = ""
    pchoice4 = ""
    data = sock.recv(1024)
    subjectInfo_arr = pickle.loads(data)
    subjectN = subjectInfo_arr[0]
    subjectO = subjectInfo_arr[1]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select count(sno) from subject where sname = '"+subjectN+"' and sorder = '"+subjectO+"';"
    curs.execute(sql)
    rows = curs.fetchall()
    countSno = rows[0].get('count(sno)')
    data = (countSno,)
    countSno_arr = pickle.dumps(data)
    sock.send(countSno_arr)
    if countSno > 0:    
        sql = "select sno, submit_user from subject where sname = '"+subjectN+"' and sorder = '"+subjectO+"';"
        curs.execute(sql)
        rows2 = curs.fetchall()
        sno = rows2[0].get('sno')
        submit_user = rows2[0].get('submit_user')
        sql = "select count(pno) from problem where sno = "+repr(sno)+";"
        curs.execute(sql)
        rows2 = curs.fetchall()
        countPno = rows2[0].get('count(pno)')
        countPno_arr = (countPno,)
        data = pickle.dumps(countPno_arr)
        sock.send(data)
        sql = "select pno, ptext, pscore, panswer, pchoice1, pchoice2, pchoice3, pchoice4 from problem where sno = "+repr(sno)+";"
        curs.execute(sql)
        rows = curs.fetchall()
        sql = "select count(solve_user_times) from problem_solve where sno = "+repr(sno)+" and solve_user = '"+ID+"';"
        curs.execute(sql)
        rowsCountSolve = curs.fetchall()
        solveCount = rowsCountSolve[0].get('count(solve_user_times)')
        for i in range(len(rows)):
            arr = (rows[i].get('pno'),rows[i].get('ptext'),rows[i].get('pscore'),rows[i].get('pchoice1'),rows[i].get('pchoice2'),rows[i].get('pchoice3'),rows[i].get('pchoice4'),submit_user)
            data = pickle.dumps(arr)
            sock.send(data)
            problemFlag = int((sock.recv(1)).decode('utf-8'))
            if problemFlag == 1:
                for j in range(i+1,len(rows)-i,1):                
                    sql = "insert into problem_solve(pno,sno,panswer,pscore,solve_user,user_answer,solve_user_times)\
                        values("+repr(rows[j].get('pno'))+","+repr(sno)+",'"+rows[j].get('panswer')+"',"+repr(rows[j].get('pscore'))+",'"+ID+"','asdfasdf',"+repr(solveCount)+");"
                    curs.execute(sql)
                    conn.commit()
            data = sock.recv(1024)
            answer_arr = pickle.loads(data)
            answer = answer_arr[0]
            sql = "insert into problem_solve(pno,sno,panswer,pscore,solve_user,user_answer,solve_user_times)\
                        values("+repr(rows[i].get('pno'))+","+repr(sno)+",'"+rows[i].get('panswer')+"',"+repr(rows[i].get('pscore'))+",'"+ID+"','"+answer+"',"+repr(solveCount)+");"
            curs.execute(sql)
            conn.commit()
            if problemFlag == 1:
                break

        sql = "select max(solve_user_times) from problem_solve where sno = "+repr(sno)+" and solve_user = '"+ID+"';"
        curs.execute(sql)
        rows = curs.fetchall()
        solve_user_times = rows[0].get('max(solve_user_times)')
        sql = "select sum(pscore) from problem_solve where solve_user_times = "+repr(solve_user_times)+" and solve_user = '"+ID+"' and panswer = user_answer;"
        curs.execute(sql)
        rows = curs.fetchall()
        userScore = (rows[0].get('sum(pscore)'),)
        data = pickle.dumps(userScore)
        sock.send(data)
    else:
        print("해당 시험의 해당 회차가 존재하지 않습니다.")
    
    conn.close()

def userConnectCheck(sock):
    data = sock.recv(1024)
    chattingUserID_arr = pickle.loads(data)
    chattingUserID = chattingUserID_arr[0]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select concheck from userinfo where ID = '"+chattingUserID+"';"
    curs.execute(sql)
    rows = curs.fetchall()
    concheck = rows[0].get('concheck')
    sock.send(repr(concheck).encode('utf-8'))
    if concheck == 1:
        print("상대방이 접속중입니다.")
    else:
        print("접속중이지 않은 상대방입니다")

    conn.close()

def chattingFunc(sock,index):
    global chattSockList
    data = sock.recv(1024)
    chattingInfo_arr = pickle.loads(data)
    chattingRecvID = chattingInfo_arr[0]
    chattingMsg = chattingInfo_arr[1]
    conn = pymysql.connect(host = 'localhost', user = 'netpro19', password = 'netpro19', db = 'netpro')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select concheck from userinfo where ID = '"+chattingRecvID+"';"
    curs.execute(sql)
    rows = curs.fetchall()
    concheck = rows[0].get('concheck')
    sock.send(repr(concheck).encode('utf-8'))
    if concheck == 1:
        chattingSendID = IDList[index]
        chattingInfo_arr2 = (chattingSendID,chattingMsg)
        data2 = pickle.dumps(chattingInfo_arr2)
        chattSockList[IDList.index(chattingRecvID)].send(data2)
    else:
        print("상대방이 접속중이지 않습니다")
    
def clntAccept(clntSock, servSock, addr, index):
    global clntThread
    global exitFlag
    global serverChattSock
    serverChattSockTemp = socket(AF_INET,SOCK_STREAM)
    serverChattSockTemp.bind(('',(8081+index)))
    serverChattSockTemp.listen(0)
    
    serverChattSock.append(serverChattSockTemp)
    
    tmp = clntThread[index]
    exitFlag.append(0)
    tmpF = exitFlag[index]
    loginFlag = 0
    count = 0
    while 1:
        menu = (clntSock.recv(1)).decode('utf-8')
        if menu == "1":#로그인
            if login(clntSock,index) == 0:
                ID = IDList[index]
            count += 1
        elif menu == "2":#회원가입
            joinMem(clntSock)
        elif menu == "3":#로그인 후에 종료
            logout(ID,index)
            exitFlag[index] = 1
            break
        elif menu == "4":#로그인 후에 로그아웃
            logout(ID,index)
            exitFlag[index] = 1
        elif menu == "5":
            submit(clntSock,ID)
        elif menu == "6" or menu == "9":
            saveProblem(clntSock,ID,int(menu))
        elif menu == "7":
            reviseProblem(clntSock,ID)
        elif menu == "d":
            removeProblem(clntSock,ID)
        elif menu == "8":
            addProblem(clntSock,ID)
        elif menu == "a":
            printSubjectName(clntSock)
        elif menu == "b":
            printSubjectOrder(clntSock)
        elif menu == "c":
            printProblemInfoAndEnterAnswer(clntSock,ID)
        elif menu == "e":
            userConnectCheck(clntSock)
        elif menu == "f":
            chattingFunc(clntSock,index)
        elif menu == "0":#로그인 전에 종
            if count > 0:
                arr = ("aa","aa")
                data = pickle.dumps(arr)
                chattSockList[index].send(data)
                IDList[index] = ""
            break
    
    print("클라이언트의 연결을 종료합니다")
    clntSock.close()


serverSock = socket(AF_INET,SOCK_STREAM)
serverSock.bind(('',8080))
serverSock.listen(0)

while 1:
    connectionSock, addr = serverSock.accept()
    print(str(addr),"에서 접속이 확인되었습니다.")
    IDList.append("")
    chattSockList.append("")
    t = threading.Thread(target = clntAccept, args = (connectionSock, serverSock, addr, len(clntThread)))
    clntThread.append(t)
    t.start()
