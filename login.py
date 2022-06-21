from socket import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import pickle
from time import sleep
import threading

clntSock = 0 #서버와의 문제풀이를 위한 통신
chattSock = 0 #서버와의 멀티채팅을 위한 통신
subjectName = ""
subjectOrder = ""
subjectN = ""
menuFlag = 0 
countProblem = 0 #해당 과목의 문제 수
problemFlag = 0 #문제를 끝까지 다 풀었는지 여부를 체크하기 위한 flag
sampleFlag = 0
samplingList = [1,2,3,4] #객관식 선택지 랜덤배치를 위한 list
tempList = [] 
exitFlag = 0 #채팅을 위한 thread를 종료시키기 위한 flag

class PROJ(QWidget):
    def __init__(self):
        super().__init__()

        global clntSock
        clntSock = socket(AF_INET, SOCK_STREAM)
        clntSock.connect(('127.0.0.1',8080))        

        self.initUI()        

    def recvChattingMsg(self):
        global chattSock
        while 1:
            data = chattSock.recv(1024)
            if exitFlag == 1:
                chattSock.close()
                break
            msg_arr = pickle.loads(data)
            chattingUserID = msg_arr[0]
            msg = msg_arr[1]
            self.chattingText.append(chattingUserID+" 로부터 메세지: "+msg)
            

    def initUI(self):
        #로그인 이전 화면 - ID, PW, 로그인, 회원가입, 종료 버튼
        self.userinfoEnterID = QLineEdit(self)
        self.userinfoEnterID.setPlaceholderText('ID')
        self.userinfoEnterID.resize(150,45)
        self.userinfoEnterID.move(530,330)

        self.userinfoEnterPW = QLineEdit(self)
        self.userinfoEnterPW.setPlaceholderText('PW')
        self.userinfoEnterPW.resize(150,45)
        self.userinfoEnterPW.move(530,385)

        self.loginButton = QPushButton('로그인',self)
        self.loginButton.move(690,330)
        self.loginButton.resize(60,100)
        self.loginButton.clicked.connect(self.clickLoginButton)
        
        self.joinMemButton = QPushButton('회원가입',self)
        self.joinMemButton.move(530,460)
        self.joinMemButton.resize(105,30)
        self.joinMemButton.clicked.connect(self.clickJoinMemButton)
        
        self.exitButton = QPushButton('종료',self)
        self.exitButton.move(645,460)
        self.exitButton.resize(105,30)
        self.exitButton.clicked.connect(self.clickExit)

        self.msgLabel = QLabel('',self)
        self.msgLabel.resize(220,25)
        self.msgLabel.move(530,430)

        #로그인 이후 화면
        #우측화면
        self.problemText = QTextBrowser(self)
        self.problemText.resize(640,400)
        self.problemText.move(640,30)
        self.problemText.hide()

        self.problemText2 = QLineEdit(self)
        self.problemText2.resize(640,400)
        self.problemText2.move(640,0)
        self.problemText2.hide()

        self.choiceGroupBox = QGroupBox('',self)
        self.choiceGroupBox.resize(140,30)
        self.choiceGroupBox.move(640,400)
        self.choiceGroupBox.hide()
    
        self.choiceRadioButton1 = QRadioButton('객관식',self)
        self.choiceRadioButton1.resize(60,30)
        self.choiceRadioButton1.move(650,400)
        self.choiceRadioButton1.hide()

        self.choiceRadioButton2 = QRadioButton('주관식',self)
        self.choiceRadioButton2.resize(60,30)
        self.choiceRadioButton2.move(720,400)
        self.choiceRadioButton2.hide()

        self.problemNumberText = QLineEdit(self)
        self.problemNumberText.setReadOnly(True)
        self.problemNumberText.resize(50,30)
        self.problemNumberText.move(640,0)
        self.problemNumberText.hide()

        self.problemScoreText = QLineEdit(self)
        self.problemScoreText.setReadOnly(True)
        self.problemScoreText.resize(30,30)
        self.problemScoreText.move(1250,430)
        self.problemScoreText.hide()

        self.problemScoreText2 = QLineEdit(self)
        self.problemScoreText2.resize(30,30)
        self.problemScoreText2.move(1250,400)
        self.problemScoreText2.hide()

        self.choiceNumText1 = QLineEdit(self)
        self.choiceNumText1.setReadOnly(True)
        self.choiceNumText1.resize(540,30)
        self.choiceNumText1.move(690,470)
        self.choiceNumText1.hide()

        self.choiceNumText2 = QLineEdit(self)
        self.choiceNumText2.setReadOnly(True)
        self.choiceNumText2.resize(540,30)
        self.choiceNumText2.move(690,500)
        self.choiceNumText2.hide()

        self.choiceNumText3 = QLineEdit(self)
        self.choiceNumText3.setReadOnly(True)
        self.choiceNumText3.resize(540,30)
        self.choiceNumText3.move(690,530)
        self.choiceNumText3.hide()

        self.choiceNumText4 = QLineEdit(self)
        self.choiceNumText4.setReadOnly(True)
        self.choiceNumText4.resize(540,30)
        self.choiceNumText4.move(690,560)
        self.choiceNumText4.hide()

        self.answerText = QLineEdit(self)
        self.answerText.setPlaceholderText('답안')
        self.answerText.resize(320,40)
        self.answerText.move(960,600)
        self.answerText.hide()

        self.choiceNumText12 = QLineEdit(self)
        self.choiceNumText12.resize(540,30)
        self.choiceNumText12.move(690,440)
        self.choiceNumText12.hide()

        self.choiceNumText22 = QLineEdit(self)
        self.choiceNumText22.resize(540,30)
        self.choiceNumText22.move(690,470)
        self.choiceNumText22.hide()

        self.choiceNumText32 = QLineEdit(self)
        self.choiceNumText32.resize(540,30)
        self.choiceNumText32.move(690,500)
        self.choiceNumText32.hide()

        self.choiceNumText42 = QLineEdit(self)
        self.choiceNumText42.resize(540,30)
        self.choiceNumText42.move(690,530)
        self.choiceNumText42.hide()

        self.answerText2 = QLineEdit(self)
        self.answerText2.setPlaceholderText('정답')
        self.answerText2.resize(320,40)
        self.answerText2.move(960,570)
        self.answerText2.hide()

        self.scoreBoard = QLineEdit(self)
        self.scoreBoard.setReadOnly(True)
        self.scoreBoard.resize(140,40)
        self.scoreBoard.move(1120,660)
        fontScore = self.scoreBoard.font()
        fontScore.setPointSize(14)
        self.scoreBoard.setFont(fontScore)
        self.scoreBoard.setAlignment(Qt.AlignCenter)
        self.scoreBoard.hide()
        self.scoreBoard.clear()

        self.submitUserBoard = QLineEdit(self)
        self.submitUserBoard.setReadOnly(True)
        self.submitUserBoard.resize(180,30)
        self.submitUserBoard.move(1100,0)
        self.submitUserBoard.hide()

        #좌측화면
        self.prevButton = QPushButton('이전',self)
        self.prevButton.resize(80,40)
        self.prevButton.move(560,105)
        self.prevButton.hide()
        self.prevButton.clicked.connect(self.clickPrevButton)
            
        self.systemMsgText = QTextEdit(self)
        self.systemMsgText.setReadOnly(True)
        self.systemMsgText.resize(640,100)
        self.systemMsgText.move(0,150)
        self.systemMsgText.hide()
        
        self.chattingText = QTextEdit(self)
        self.chattingText.setReadOnly(True)
        self.chattingText.resize(640,500)
        self.chattingText.move(0,250)
        self.chattingText.hide()

        self.chattingUser = QLineEdit(self)
        self.chattingUser.setPlaceholderText('상대방아이디')
        self.chattingUser.resize(100,50)
        self.chattingUser.move(0,750)
        self.chattingUser.hide()
        
        self.userConnectCheckButton = QPushButton('접속확인',self)
        self.userConnectCheckButton.resize(50,50)
        self.userConnectCheckButton.move(100,750)
        self.userConnectCheckButton.hide()
        self.userConnectCheckButton.clicked.connect(self.clickUserConnectCheckButton)
        
        self.sendMsgText = QLineEdit(self)
        self.sendMsgText.resize(440,50)
        self.sendMsgText.move(150,750)
        self.sendMsgText.hide()

        self.sendMsgButton = QPushButton('전송',self)
        self.sendMsgButton.resize(50,50)
        self.sendMsgButton.move(590,750)
        self.sendMsgButton.hide()
        self.sendMsgButton.clicked.connect(self.clickSendMsgButton)
        
        self.subjectNameLabel = QLabel('시험명',self)
        self.subjectNameLabel.resize(190,15)
        self.subjectNameLabel.move(30,20)
        self.subjectNameLabel.setAlignment(Qt.AlignCenter)
        self.subjectNameLabel.hide()
        
        self.subjectOrderLabel = QLabel('회차',self)
        self.subjectOrderLabel.resize(190,15)
        self.subjectOrderLabel.move(350,20)
        self.subjectOrderLabel.setAlignment(Qt.AlignCenter)
        self.subjectOrderLabel.hide()

        self.subjectNameText = QLineEdit(self)
        self.subjectNameText.setPlaceholderText('시험명')
        self.subjectNameText.resize(150,50)
        self.subjectNameText.move(10,25)
        self.subjectNameText.hide()

        self.subjectOrderText = QLineEdit(self)
        self.subjectOrderText.setPlaceholderText('회차')
        self.subjectOrderText.resize(150,50)
        self.subjectOrderText.move(160,25)
        self.subjectOrderText.hide()

        self.subjectNameBox = QComboBox(self)
        self.subjectNameBox.resize(190,25)
        self.subjectNameBox.move(30,60)
        self.subjectNameBox.hide()

        self.subjectOrderBox = QComboBox(self)
        self.subjectOrderBox.resize(190,25)
        self.subjectOrderBox.move(350,60)
        self.subjectOrderBox.hide()

        self.subjectNameSelect = QLineEdit(self)
        self.subjectNameSelect.setPlaceholderText('시험명')
        self.subjectNameSelect.resize(190,25)
        self.subjectNameSelect.move(30,35)
        self.subjectNameSelect.hide()

        self.subjectOrderSelect = QLineEdit(self)
        self.subjectOrderSelect.setPlaceholderText('회차')
        self.subjectOrderSelect.resize(190,25)
        self.subjectOrderSelect.move(350,35)
        self.subjectOrderSelect.hide()

        self.solveButton = QPushButton('문제풀기',self)
        self.solveButton.move(10,0)
        self.solveButton.resize(200,100)
        self.solveButton.hide()
        self.solveButton.clicked.connect(self.clickSolveButton)

        self.selectSubjectButton = QPushButton('시험선택',self)
        self.selectSubjectButton.move(240,0)
        self.selectSubjectButton.resize(80,100)
        self.selectSubjectButton.hide()
        self.selectSubjectButton.clicked.connect(self.clickSelectSubjectButton)

        self.solveStartButton = QPushButton('풀기',self)
        self.solveStartButton.move(560,0)
        self.solveStartButton.resize(80,100)
        self.solveStartButton.hide()
        self.solveStartButton.clicked.connect(self.clickSolveStartButton)

        self.uploadButton = QPushButton('문제업로드',self)
        self.uploadButton.move(220,0)
        self.uploadButton.resize(200,100)
        self.uploadButton.hide()
        self.uploadButton.clicked.connect(self.clickUploadButton)

        self.reviseButton = QPushButton('문제수정',self)
        self.reviseButton.move(430,0)
        self.reviseButton.resize(200,100)
        self.reviseButton.hide()
        self.reviseButton.clicked.connect(self.clickReviseButton)

        self.problemNumText = QLineEdit(self)
        self.problemNumText.setPlaceholderText('문항번호')
        self.problemNumText.resize(100,50)
        self.problemNumText.move(330,10)
        self.problemNumText.hide()

        self.reviseStartButton = QPushButton('수정시작',self)
        self.reviseStartButton.resize(180,25)
        self.reviseStartButton.move(440,10)
        self.reviseStartButton.hide()
        self.reviseStartButton.clicked.connect(self.clickReviseStartButton)

        self.removeStartButton = QPushButton('삭제',self)
        self.removeStartButton.resize(180,25)
        self.removeStartButton.move(440,35)
        self.removeStartButton.hide()
        self.removeStartButton.clicked.connect(self.clickRemoveStartButton)

        self.addProblemButton = QPushButton('덧붙이기',self)
        self.addProblemButton.resize(300,25)
        self.addProblemButton.move(330,65)
        self.addProblemButton.hide()
        self.addProblemButton.clicked.connect(self.clickAddProblemButton)

        self.uploadStartButton = QPushButton('문제작성',self)
        self.uploadStartButton.move(320,0)
        self.uploadStartButton.resize(320,100)
        self.uploadStartButton.hide()
        self.uploadStartButton.clicked.connect(self.clickUploadStartButton)

        self.logoutButton = QPushButton('로그아웃',self)
        self.logoutButton.move(640,760)
        self.logoutButton.resize(320,40)
        self.logoutButton.hide()
        self.logoutButton.clicked.connect(self.clickLogoutButton)

        self.exitButton2 = QPushButton('종료',self)
        self.exitButton2.move(960,760)
        self.exitButton2.resize(320,40)
        self.exitButton2.hide()
        self.exitButton2.clicked.connect(self.clickExitAfterLogin)

        self.submitButton = QPushButton('제출하기',self)
        self.submitButton.move(640,720)
        self.submitButton.resize(160,40)
        self.submitButton.hide()
        self.submitButton.clicked.connect(self.clickSubmitButton)

        self.nextProblemButton = QPushButton('다음문제',self)
        self.nextProblemButton.move(1120,720)
        self.nextProblemButton.resize(160,40)
        self.nextProblemButton.hide()
        self.nextProblemButton.clicked.connect(self.clickNextProblemButton)

        self.saveButton = QPushButton('저장하기',self)
        self.saveButton.move(640,720)
        self.saveButton.resize(160,40)
        self.saveButton.hide()
        self.saveButton.clicked.connect(self.clickSaveButton)

        self.nextProblemButton2 = QPushButton('다음문제',self)
        self.nextProblemButton2.move(1120,720)
        self.nextProblemButton2.resize(160,40)
        self.nextProblemButton2.hide()
        self.nextProblemButton2.clicked.connect(self.clickNextProblemButton2)

        

        #layoutset
        self.setWindowTitle('실전 대비 모의고사')
        self.setGeometry(200,200,200,200)
        self.resize(1280,800)
        self.show()


    def clickPrevButton(self):
        self.solveButton.show()
        self.uploadButton.show()
        self.reviseButton.show()
        self.prevButton.hide()
        self.subjectNameText.hide()
        self.subjectOrderText.hide()
        self.subjectNameBox.hide()
        self.subjectOrderBox.hide()
        self.subjectNameLabel.hide()
        self.subjectOrderLabel.hide()
        self.subjectNameSelect.hide()
        self.subjectOrderSelect.hide()
        self.solveStartButton.hide()
        self.selectSubjectButton.hide()
        self.uploadStartButton.hide()
        self.reviseStartButton.hide()
        self.removeStartButton.hide()
        self.addProblemButton.hide()
        self.problemNumText.hide()
        self.subjectNameText.clear()
        self.subjectOrderText.clear()
        self.subjectNameBox.clear()
        self.subjectOrderBox.clear()
        self.subjectNameSelect.clear()
        self.subjectOrderSelect.clear()
        self.problemNumText.clear()
    
        
        #초기상태로 돌아가게 해주기.

        
    #모의고사를 응시할 때 사용되는 버튼의 기능을 수행하는 함수들
    def clickSolveButton(self):
        menu = "a"
        clntSock.send(menu.encode('utf-8'))
        self.prevButton.show()
        self.solveButton.hide()
        self.uploadButton.hide()
        self.reviseButton.hide()
        self.scoreBoard.hide()
        self.subjectNameBox.show()
        self.subjectNameLabel.show()
        self.subjectNameSelect.show()
        self.subjectNameText.hide()
        self.subjectOrderText.hide()
        self.selectSubjectButton.show()
        self.subjectNameBox.clear()
        self.subjectNameBox.addItem("시험명")
        self.subjectOrderBox.clear()
        self.subjectOrderBox.addItem("회차")
        self.subjectNameSelect.clear()
        self.subjectOrderSelect.clear()
        flag = int((clntSock.recv(1)).decode('utf-8'))
        if flag == 1:
            #여기에서는 combobox에 목록을 추가해준
            subjectNameList_arr = clntSock.recv(1024)
            subjectNameList = pickle.loads(subjectNameList_arr)
            for i in range(len(subjectNameList)):
                self.subjectNameBox.addItem(subjectNameList[i])
        else:
            print("else")

    def clickSelectSubjectButton(self):
        global subjectN
        if self.subjectNameSelect.text() == "":
            self.systemMsgText.append("시험명을 입력하지 않았습니다.")
        else:
            menu = "b"
            clntSock.send(menu.encode('utf-8'))
            subjectN = self.subjectNameSelect.text()
            subjectN_arr = (subjectN,)
            data = pickle.dumps(subjectN_arr)
            clntSock.send(data)

            data = clntSock.recv(1024)
            countSno_arr = pickle.loads(data)
            countSno = countSno_arr[0]

            if countSno > 0:            
                data2 = clntSock.recv(1024)
                subjectO = pickle.loads(data2)
                self.subjectOrderBox.clear()
                self.subjectOrderBox.addItem("회차")
                for i in range(len(subjectO)):
                    self.subjectOrderBox.addItem(subjectO[i])
                self.subjectOrderBox.show()
                self.subjectOrderLabel.show()
                self.subjectOrderSelect.show()
                self.solveStartButton.show()
            else:
                self.systemMsgText.append("해당 시험이 존재하지 않습니다.")

    def clickSolveStartButton(self):
        global countProblem
        global problemFlag
        global tempList
        global sampleFlag
        if self.subjectOrderSelect.text() == "":
            self.systemMsgText.append("회차를 입력하지 않았습니다.")
        else:
            menu = "c"
            clntSock.send(menu.encode('utf-8'))
            subjectO = self.subjectOrderSelect.text()
            data = (subjectN,subjectO)
            subjectInfo_arr = pickle.dumps(data)
            clntSock.send(subjectInfo_arr)
            
            data = clntSock.recv(1024)
            countSno_arr = pickle.loads(data)
            countSno = countSno_arr[0]

            if countSno > 0:
                self.problemText.show()
                self.problemNumberText.show()
                self.submitUserBoard.show()
                self.choiceNumText1.show()
                self.choiceNumText2.show()
                self.choiceNumText3.show()
                self.choiceNumText4.show()
                self.answerText.show()
                self.problemScoreText.show()
                self.submitButton.show()
                self.nextProblemButton.show()
                self.prevButton.hide()
                self.userConnectCheckButton.hide()
                self.sendMsgButton.hide()
                

                data = clntSock.recv(1024)
                countPno_arr = pickle.loads(data)
                countProblem = countPno_arr[0]
                
                data = clntSock.recv(2048)
                problemN = pickle.loads(data)
                if problemN[0] == countProblem:
                    self.nextProblemButton.hide()
                    problemFlag = 0
                else:
                    problemFlag = 1

                if problemN[3] != "":
                    sampleFlag = 0
                else:
                    sampleFlag = 1
                
                tempList = random.sample(samplingList,4)
                
                self.problemNumberText.setText(repr(problemN[0])+"번")
                self.problemText.setText(problemN[1])
                self.choiceNumText1.setText(problemN[tempList[0]+2])
                self.choiceNumText2.setText(problemN[tempList[1]+2])
                self.choiceNumText3.setText(problemN[tempList[2]+2])
                self.choiceNumText4.setText(problemN[tempList[3]+2])
                self.problemScoreText.setText(repr(problemN[2]))
                self.submitUserBoard.setText("출제자 : "+problemN[7])
            else:
                self.systemMsgText.append("해당 과목의 해당 회차가 존재하지 않습니다.")

    def clickNextProblemButton(self):
        global problemFlag
        global tempList
        global sampleFlag
        problemFlag = 0
        if self.answerText.text() == "":
            self.systemMsgText.append("답안을 입력하지 않았습니다.")
        else:
            clntSock.send((repr(problemFlag)).encode('utf-8'))
            answer = ""
            
            if sampleFlag == 0:
                answer = repr(tempList[(int(self.answerText.text()))-1])
            else:
                answer = self.answerText.text()
            answer_arr = (answer,)
            data = pickle.dumps(answer_arr)
            clntSock.send(data)

            data = clntSock.recv(2048)
            problemN = pickle.loads(data)
            
            if problemN[0] == countProblem:
                self.nextProblemButton.hide()
            
            if problemN[3] != "":
                sampleFlag = 0
            else:
                sampleFlag = 1
            
            tempList = random.sample(samplingList,4)
                
            self.problemNumberText.setText(repr(problemN[0])+"번")
            self.problemText.setText(problemN[1])
            self.choiceNumText1.setText(problemN[tempList[0]+2])
            self.choiceNumText2.setText(problemN[tempList[1]+2])
            self.choiceNumText3.setText(problemN[tempList[2]+2])
            self.choiceNumText4.setText(problemN[tempList[3]+2])
            self.answerText.clear()
            self.problemScoreText.setText(repr(problemN[2]))

    def clickSubmitButton(self):
        global problemFlag
        if self.answerText.text() == "":
            self.systemMsgText.append("답안을 입력하지 않았습니다.")
        else:
            problemNumber = self.problemNumberText.text().split('번')[0]
            if int(problemNumber) != countProblem:
                problemFlag = 1
            clntSock.send((repr(problemFlag)).encode('utf-8'))
            answer = ""
            if sampleFlag == 0:
                answer = repr(tempList[(int(self.answerText.text()))-1])
            else:
                answer = self.answerText.text()
            answer_arr = (answer,)
            data = pickle.dumps(answer_arr)
            clntSock.send(data)
            
            data = clntSock.recv(1024)
            userScore_arr = pickle.loads(data)
            userScore = userScore_arr[0]

            if str(userScore) == "None":
                userScore = 0
            
            self.scoreBoard.setText("점수 : "+str(userScore)+"점")

            self.scoreBoard.show()
            self.solveButton.show()
            self.uploadButton.show()
            self.reviseButton.show()
            self.userConnectCheckButton.show()
            self.sendMsgButton.show()
            self.submitButton.hide()
            self.nextProblemButton.hide()
            self.subjectNameBox.hide()
            self.subjectOrderBox.hide()
            self.subjectNameLabel.hide()
            self.subjectOrderLabel.hide()
            self.subjectNameSelect.hide()
            self.subjectOrderSelect.hide()
            self.problemNumberText.hide()
            self.submitUserBoard.hide()
            self.problemText.hide()
            self.choiceNumText1.hide()
            self.choiceNumText2.hide()
            self.choiceNumText3.hide()
            self.choiceNumText4.hide()
            self.answerText.hide()
            self.problemScoreText.hide()
            self.solveStartButton.hide()
            self.selectSubjectButton.hide()
            self.problemNumberText.clear()
            self.submitUserBoard
            self.problemText.clear()
            self.choiceNumText1.clear()
            self.choiceNumText2.clear()
            self.choiceNumText3.clear()
            self.choiceNumText4.clear()
            self.answerText.clear()
            self.problemScoreText.clear()
            self.subjectNameBox.clear()
            self.subjectNameBox.addItem("시험명")
            self.subjectOrderBox.clear()
            self.subjectOrderBox.addItem("회차")


    #모의고사 문제를 업로드 및 수정할 때 사용되는 버튼의 기능을 수행하는 함수들
    def clickUploadButton(self):
        self.solveButton.hide()
        self.uploadButton.hide()
        self.reviseButton.hide()
        self.prevButton.show()
        self.scoreBoard.hide()
        self.scoreBoard.clear()
        self.subjectNameText.show()
        self.subjectOrderText.show()
        self.uploadStartButton.show()
        
    def clickUploadStartButton(self):
        global menuFlag
        global subjectName
        global subjectOrder
        if self.subjectNameText.text() == "":
            self.systemMsgText.append("시험명을 입력하지 않았습니다.")
        elif self.subjectOrderText.text() == "":
            self.systemMsgText.append("회차를 입력하지 않았습니다.")
        else:
            menuFlag = 0
            subjectName = self.subjectNameText.text()
            subjectOrder = self.subjectOrderText.text()
            menu = 5
            clntSock.send(repr(menu).encode('utf-8'))
            subjectInfo = (subjectName,subjectOrder)
            subjectInfo_arr = pickle.dumps(subjectInfo)
            clntSock.send(subjectInfo_arr)

            flag = int((clntSock.recv(1)).decode('utf-8'))
            if flag == 1:
                self.saveButton.show()
                self.nextProblemButton2.show()
                self.problemText2.show()
                self.choiceNumText12.show()
                self.choiceNumText22.show()
                self.choiceNumText32.show()
                self.choiceNumText42.show()
                self.answerText2.show()
                self.problemScoreText2.show()
                self.choiceGroupBox.show()
                self.choiceRadioButton1.show()
                self.choiceRadioButton2.show()
                self.prevButton.hide()
            else:
                self.systemMsgText.append("이미 존재하는 과목입니다.")

    def clickReviseButton(self):
        self.solveButton.hide()
        self.uploadButton.hide()
        self.reviseButton.hide()
        self.prevButton.show()
        self.scoreBoard.hide()
        self.scoreBoard.clear()
        self.subjectNameText.show()
        self.subjectOrderText.show()
        self.problemNumText.show()
        self.reviseStartButton.show()
        self.removeStartButton.show()
        self.addProblemButton.show()

    def clickReviseStartButton(self):
        global menuFlag
        global subjectName
        global subjectOrder
        if self.subjectNameText.text() == "":
            self.systemMsgText.append("시험명을 입력하지 않았습니다.")
        elif self.subjectOrderText.text() == "":
            self.systemMsgText.append("회차를 입력하지 않았습니다.")
        elif self.problemNumText.text() == "":
            self.systemMsgText.append("문항번호를 입력하지 않았습니다.")
        else:
            menu = 7
            menuFlag = 1
            clntSock.send(repr(menu).encode('utf-8'))
            subjectName = self.subjectNameText.text()
            subjectOrder = self.subjectOrderText.text()
            problemNum = self.problemNumText.text()
            subjectInfo = (subjectName,subjectOrder,problemNum)
            subjectInfo_arr = pickle.dumps(subjectInfo)
            clntSock.send(subjectInfo_arr)
            data = clntSock.recv(1024)
            existSubject_arr = pickle.loads(data)
            existSubject = existSubject_arr[0]
            if existSubject > 0:
                flag = int((clntSock.recv(1)).decode('utf-8'))
                if flag == 1:
                    data = clntSock.recv(1024)
                    pno_arr = pickle.loads(data)
                    pnoCount = pno_arr[0]
                    if int(problemNum) > 0 and int(problemNum) <= pnoCount:
                        self.saveButton.show()
                        self.problemText2.show()
                        self.choiceNumText12.show()
                        self.choiceNumText22.show()
                        self.choiceNumText32.show()
                        self.choiceNumText42.show()
                        self.answerText2.show()
                        self.problemScoreText2.show()
                        self.choiceGroupBox.show()
                        self.choiceRadioButton1.show()
                        self.choiceRadioButton2.show()
                        self.prevButton.hide()
                        data = clntSock.recv(2048)
                        problemInfo = pickle.loads(data)
                        problemPtext = problemInfo[0]
                        problemPanswer = problemInfo[1]
                        problemPscore = problemInfo[2]
                        problemPtype = problemInfo[3]
                        problemPchoice1 = problemInfo[4]
                        problemPchoice2 = problemInfo[5]
                        problemPchoice3 = problemInfo[6]
                        problemPchoice4 = problemInfo[7]
                        if problemPtype == 1:
                            self.choiceRadioButton1.setChecked(True)
                        else:
                            self.choiceRadioButton2.setChecked(True)
                        self.problemText2.setText(problemPtext)
                        self.answerText2.setText(problemPanswer)
                        self.problemScoreText2.setText(repr(problemPscore))
                        self.choiceNumText12.setText(problemPchoice1)
                        self.choiceNumText22.setText(problemPchoice2)
                        self.choiceNumText32.setText(problemPchoice3)
                        self.choiceNumText42.setText(problemPchoice4)
                    else:
                        self.systemMsgText.append("해당 문항이 존재하지 않습니다.")
                else:
                    self.systemMsgText.append("수정할 권한이 없습니다.")
            else:
                self.systemMsgText.append("해당 시험이나 회차가 존재하지 않습니다.")

    def clickRemoveStartButton(self):
        global subjectName
        global subjectOrder
        if self.subjectNameText.text() == "":
            self.systemMsgText.append("시험명을 입력하지 않았습니다.")
        elif self.subjectOrderText.text() == "":
            self.systemMsgText.append("회차를 입력하지 않았습니다.")
        elif self.problemNumText.text() == "":
            self.systemMsgText.append("문항번호를 입력하지 않았습니다.")
        else:
            menu = "d"
            clntSock.send(menu.encode('utf-8'))
            
            subjectName = self.subjectNameText.text()
            subjectOrder = self.subjectOrderText.text()
            problemNum = self.problemNumText.text()
            subjectInfo = (subjectName,subjectOrder,problemNum)
            subjectInfo_arr = pickle.dumps(subjectInfo)
            clntSock.send(subjectInfo_arr)

            data = clntSock.recv(1024)
            existSubject_arr = pickle.loads(data)
            existSubject = existSubject_arr[0]
            if existSubject > 0:            
                flag = int((clntSock.recv(1)).decode('utf-8'))
                if flag == 1:#삭제가능
                    data = clntSock.recv(1024)
                    pno_arr = pickle.loads(data)
                    pnoCount = pno_arr[0]
                    if int(problemNum) > 0 and int(problemNum) <= pnoCount:
                        self.systemMsgText.append("삭제 완료")
                    else:
                        self.systemMsgText.append("해당 문항이 존재하지 않습니다,")
                else:
                    self.systemMsgText.append("삭제할 권한이 없습니다.")
            else:
                self.systemMsgText.append("해당 시험이나 회차가 존재하지 않습니다.")
            self.solveButton.show()
            self.uploadButton.show()
            self.reviseButton.show()
            self.subjectNameText.hide()
            self.subjectOrderText.hide()
            self.problemNumText.hide()
            self.reviseStartButton.hide()
            self.removeStartButton.hide()
            self.addProblemButton.hide()
            self.prevButton.hide()
            self.subjectNameText.clear()
            self.subjectOrderText.clear()
            self.problemNumText.clear()

    def clickAddProblemButton(self):
        global subjectName
        global subjectOrder
        global menuFlag
        if self.subjectNameText.text() == "":
            self.systemMsgText.append("시험명을 입력하지 않았습니다.")
        elif self.subjectOrderText.text() == "":
            self.systemMsgText.append("회차를 입력하지 않았습니다.")
        else:
            menuFlag = 0
            subjectName = self.subjectNameText.text()
            subjectOrder = self.subjectOrderText.text()
            menu = 8
            clntSock.send(repr(menu).encode('utf-8'))
            subjectInfo = (subjectName,subjectOrder)
            subjectInfo_arr = pickle.dumps(subjectInfo)
            clntSock.send(subjectInfo_arr)
            data = clntSock.recv(1024)
            existSubject_arr = pickle.loads(data)
            existSubject = existSubject_arr[0]
            if existSubject > 0:
                flag = int((clntSock.recv(1024)).decode('utf-8'))
                if flag == 1:
                    self.saveButton.show()
                    self.nextProblemButton2.show()
                    self.problemText2.show()
                    self.choiceNumText12.show()
                    self.choiceNumText22.show()
                    self.choiceNumText32.show()
                    self.choiceNumText42.show()
                    self.answerText2.show()
                    self.problemScoreText2.show()
                    self.choiceGroupBox.show()
                    self.choiceRadioButton1.show()
                    self.choiceRadioButton2.show()
                    self.prevButton.hide()
                else:
                    self.systemMsgText.append("덧붙일 권한이 없습니다.")
            else:
                self.systemMsgText.append("해당 시험이나 회차가 존재하지 않습니다.")

    def clickSaveButton(self):
        errorFlag = 0
        if self.problemText2.text() == "":
            self.systemMsgText.append("제시문을 입력하지 않았습니다.")
            errorFlag = 1
        elif self.problemScoreText2.text() == "":
            self.systemMsgText.append("점수를 입력하지 않았습니다.")
            errorFlag = 1
        elif self.answerText2.text() == "":
            self.systemMsgText.append("정답을 입력하지 않았습니다.")
            errorFlag = 1
        elif self.choiceRadioButton1.isChecked() == False and self.choiceRadioButton2.isChecked()== False:
            self.systemMsgText.append("객관식인지 주관식인지 선택하지 않았습니다.")
            errorFlag = 1
        elif self.choiceNumText12.text() == "":
            if self.choiceRadioButton1.isChecked() == True:
                self.systemMsgText.append("객관식의 1번 선택지를 입력하지 않았습니다.")
                errorFlag = 1
            elif self.choiceRadioButton2.isChecked() == True:
                errorFlag = 0
        elif self.choiceNumText22.text() == "":
            if self.choiceRadioButton1.isChecked() == True:
                self.systemMsgText.append("객관식의 2번 선택지를 입력하지 않았습니다.")
                errorFlag = 1
            elif self.choiceRadioButton2.isChecked() == True:
                errorFlag = 0
        elif self.choiceNumText32.text() == "":
            if self.choiceRadioButton1.isChecked() == True:
                self.systemMsgText.append("객관식의 3번 선택지를 입력하지 않았습니다.")
                errorFlag = 1
            elif self.choiceRadioButton2.isChecked() == True:
                errorFlag = 0
        elif self.choiceNumText42.text() == "":
            if self.choiceRadioButton1.isChecked() == True:
                self.systemMsgText.append("객관식의 4번 선택지를 입력하지 않았습니다.")
                errorFlag = 1
            elif self.choiceRadioButton2.isChecked() == True:
                errorFlag = 0
                
        if errorFlag == 0:
            self.solveButton.show()
            self.uploadButton.show()
            self.reviseButton.show()
            self.subjectNameText.hide()
            self.subjectOrderText.hide()
            self.saveButton.hide()
            self.nextProblemButton2.hide()
            self.problemText2.hide()
            self.choiceNumText12.hide()
            self.choiceNumText22.hide()
            self.choiceNumText32.hide()
            self.choiceNumText42.hide()
            self.answerText2.hide()
            self.problemScoreText2.hide()
            self.uploadStartButton.hide()
            self.choiceGroupBox.hide()
            self.choiceRadioButton1.hide()
            self.choiceRadioButton2.hide()
            self.problemNumText.hide()
            self.reviseStartButton.hide()
            self.removeStartButton.hide()
            self.addProblemButton.hide()
            problemNum = self.problemNumText.text()
            problem = self.problemText2.text()
            problemScore = self.problemScoreText2.text()
            answer2 = self.answerText2.text()
            if self.choiceRadioButton1.isChecked():
                ptype = True
                choiceNum12 = self.choiceNumText12.text()
                choiceNum22 = self.choiceNumText22.text()
                choiceNum32 = self.choiceNumText32.text()
                choiceNum42 = self.choiceNumText42.text()
                problemInfo = (subjectName,subjectOrder,problem,problemScore,answer2,ptype,choiceNum12,choiceNum22,choiceNum32,choiceNum42)
                self.choiceRadioButton1.setChecked(False)
            else:
                ptype = False
                problemInfo = (subjectName,subjectOrder,problem,problemScore,answer2,ptype)
                self.choiceRadioButton2.setChecked(False)
            if menuFlag == 0:#문제 처음 출제 혹은 문제 추가 출제
                menu = 6
            else:#문제 하나 수정
                menu = 9
            clntSock.send(repr(menu).encode('utf-8'))
            problemInfo_arr = pickle.dumps(problemInfo)
            clntSock.send(problemInfo_arr)
            if menu == 9:
                problemNumData = (problemNum,0)
                problemNum_arr = pickle.dumps(problemNumData)
                clntSock.send(problemNum_arr)
            self.problemText2.clear()
            self.problemScoreText2.clear()
            self.answerText2.clear()
            self.choiceNumText12.clear()
            self.choiceNumText22.clear()
            self.choiceNumText32.clear()
            self.choiceNumText42.clear()
            self.subjectNameText.clear()
            self.subjectOrderText.clear()
            self.problemNumText.clear()

    def clickNextProblemButton2(self):
        if self.problemText2.text() == "":
            self.systemMsgText.append("제시문을 입력하지 않았습니다.")
            errorFlag = 1
        elif self.problemScoreText2.text() == "":
            self.systemMsgText.append("점수를 입력하지 않았습니다.")
            errorFlag = 1
        elif self.answerText2.text() == "":
            self.systemMsgText.append("정답을 입력하지 않았습니다.")
            errorFlag = 1
        elif self.choiceRadioButton1.isChecked() == False and self.choiceRadioButton2.isChecked()== False:
            self.systemMsgText.append("객관식인지 주관식인지 선택하지 않았습니다.")
            errorFlag = 1
        elif self.choiceNumText12.text() == "":
            if self.choiceRadioButton1.isChecked() == True:
                self.systemMsgText.append("객관식의 1번 선택지를 입력하지 않았습니다.")
                errorFlag = 1
            elif self.choiceRadioButton2.isChecked() == True:
                errorFlag = 0
        elif self.choiceNumText22.text() == "":
            if self.choiceRadioButton1.isChecked() == True:
                self.systemMsgText.append("객관식의 2번 선택지를 입력하지 않았습니다.")
                errorFlag = 1
            elif self.choiceRadioButton2.isChecked() == True:
                errorFlag = 0
        elif self.choiceNumText32.text() == "":
            if self.choiceRadioButton1.isChecked() == True:
                self.systemMsgText.append("객관식의 3번 선택지를 입력하지 않았습니다.")
                errorFlag = 1
            elif self.choiceRadioButton2.isChecked() == True:
                errorFlag = 0
        elif self.choiceNumText42.text() == "":
            if self.choiceRadioButton1.isChecked() == True:
                self.systemMsgText.append("객관식의 4번 선택지를 입력하지 않았습니다.")
                errorFlag = 1
            elif self.choiceRadioButton2.isChecked() == True:
                errorFlag = 0
        else:
            problem = self.problemText2.text()
            problemScore = self.problemScoreText2.text()
            answer2 = self.answerText2.text()
            if self.choiceRadioButton1.isChecked():
                ptype = True
                choiceNum12 = self.choiceNumText12.text()
                choiceNum22 = self.choiceNumText22.text()
                choiceNum32 = self.choiceNumText32.text()
                choiceNum42 = self.choiceNumText42.text()
                problemInfo = (subjectName,subjectOrder,problem,problemScore,answer2,ptype,choiceNum12,choiceNum22,choiceNum32,choiceNum42)
                self.choiceRadioButton1.setChecked(False)
            else:
                ptype = False
                problemInfo = (subjectName,subjectOrder,problem,problemScore,answer2,ptype)
                self.choiceRadioButton2.setChecked(False)
            menu = 6
            clntSock.send(repr(menu).encode('utf-8'))
            problemInfo_arr = pickle.dumps(problemInfo)
            clntSock.send(problemInfo_arr)
            self.problemText2.clear()
            self.problemScoreText2.clear()
            self.answerText2.clear()
            self.choiceNumText12.clear()
            self.choiceNumText22.clear()
            self.choiceNumText32.clear()
            self.choiceNumText42.clear()


    #채팅할 때 사용되는 버튼의 기능을 수행하는 함수들
    def clickUserConnectCheckButton(self):
        if self.chattingUser.text() == "":
            self.chattingText.append("상대방 아이디를 입력하지 않았습니다.")
        else:
            menu = "e"
            clntSock.send(menu.encode('utf-8'))
            chattingUserID = self.chattingUser.text()
            chattingUserID_arr = (chattingUserID,)
            data = pickle.dumps(chattingUserID_arr)
            clntSock.send(data)
            concheck = (clntSock.recv(1)).decode('utf-8')
            if int(concheck) == 1:
                self.chattingText.append(self.chattingUser.text()+"이(가) 접속중입니다.")
            else:
                self.chattingText.append(self.chattingUser.text()+"이(가) 접속중이지 않습니다.")

    def clickSendMsgButton(self):
        global chattSock
        if self.chattingUser.text() == "":
            self.chattingText.append("상대방 아이디를 입력하지 않았습니다.")
        elif self.sendMsgText.text() == "":
            self.chattingText.append(self.chattingUser.text()+"에게 전송할 메세지를 입력하지 않았습니다.")
        else:
            menu = "f"
            clntSock.send(menu.encode('utf-8'))
            chattingUserID = self.chattingUser.text()
            chattingMsg = self.sendMsgText.text()
            chattingInfo = (chattingUserID,chattingMsg)
            data = pickle.dumps(chattingInfo)
            clntSock.send(data)
            concheck = (clntSock.recv(1)).decode('utf-8')
            if int(concheck) != 1:
                self.chattingText.append(chattingUserID+" 이(가) 접속중이지 않습니다.")
            else:
                self.chattingText.append(chattingUserID+" 에게 보내는 메시지: "+chattingMsg)
            self.sendMsgText.clear()

    #로그인과 로그아웃 및 종료할 때 필요한 함수들
    def clickLoginButton(self):
        loginFlag = self.login()
        if loginFlag == 0:
            self.userinfoEnterID.hide()
            self.userinfoEnterPW.hide()
            self.loginButton.hide()
            self.joinMemButton.hide()
            self.exitButton.hide()
            self.msgLabel.hide()
            self.solveButton.show()
            self.uploadButton.show()
            self.reviseButton.show()
            self.logoutButton.show()
            self.exitButton2.show()
            self.systemMsgText.show()
            self.chattingText.show()
            self.chattingUser.show()
            self.userConnectCheckButton.show()
            self.sendMsgText.show()
            self.sendMsgButton.show()
        elif loginFlag == 1:
            self.msgLabel.setText("ID가 존재하지 않습니다.")
        elif loginFlag == 2:
            self.msgLabel.setText("PW가 틀렸습니다.")
        elif loginFlag == 3:
            self.msgLabel.setText("이미 접속중인 ID입니다")

    def clickJoinMemButton(self):
        self.joinMem()
        
    def clickLogoutButton(self):
        global exitFlag
        global chattSock
        exitFlag = 1
        self.userinfoEnterID.clear()
        self.userinfoEnterID.show()
        self.userinfoEnterPW.clear()
        self.userinfoEnterPW.show()
        self.loginButton.show()
        self.joinMemButton.show()
        self.exitButton.show()
        self.msgLabel.clear()
        self.msgLabel.show()
        self.problemNumberText.hide()
        self.submitUserBoard.hide()
        self.problemText.hide()
        self.problemText2.hide()
        self.choiceGroupBox.hide()
        self.choiceRadioButton1.hide()
        self.choiceRadioButton2.hide()
        self.problemScoreText.hide()
        self.problemScoreText2.hide()
        self.choiceNumText1.hide()
        self.choiceNumText2.hide()
        self.choiceNumText3.hide()
        self.choiceNumText4.hide()
        self.choiceNumText12.hide()
        self.choiceNumText22.hide()
        self.choiceNumText32.hide()
        self.choiceNumText42.hide()
        self.answerText.hide()
        self.answerText2.hide()
        self.chattingText.hide()
        self.systemMsgText.hide()
        self.chattingUser.hide()
        self.userConnectCheckButton.hide()
        self.sendMsgText.hide()
        self.sendMsgButton.hide()
        self.subjectNameText.hide()
        self.subjectOrderText.hide()
        self.subjectNameBox.hide()
        self.subjectOrderBox.hide()
        self.subjectNameLabel.hide()
        self.subjectOrderLabel.hide()
        self.subjectNameSelect.hide()
        self.subjectOrderSelect.hide()
        self.solveButton.hide()
        self.solveStartButton.hide()
        self.selectSubjectButton.hide()
        self.uploadButton.hide()
        self.uploadStartButton.hide()
        self.reviseButton.hide()
        self.logoutButton.hide()
        self.exitButton2.hide()
        self.submitButton.hide()
        self.nextProblemButton.hide()
        self.nextProblemButton2.hide()
        self.saveButton.hide()
        self.problemNumText.hide()
        self.reviseStartButton.hide()
        self.removeStartButton.hide()
        self.addProblemButton.hide()
        self.problemText2.clear()
        self.problemScoreText2.clear()
        self.answerText2.clear()
        self.choiceNumText12.clear()
        self.choiceNumText22.clear()
        self.choiceNumText32.clear()
        self.choiceNumText42.clear()
        self.subjectNameText.clear()
        self.subjectOrderText.clear()
        self.problemNumText.clear()
        self.scoreBoard.hide()
        self.scoreBoard.clear()
        self.chattingUser.clear()
        self.sendMsgText.clear()
        self.systemMsgText.clear()
        self.chattingText.clear()
        menu = 4
        clntSock.send(repr(menu).encode('utf-8'))

    def clickExit(self):
        global exitFlag
        exitFlag = 1
        menu = 0
        clntSock.send(repr(menu).encode('utf-8'))
        sys.exit()

    def clickExitAfterLogin(self):
        global exitFlag
        menu = 3
        clntSock.send(repr(menu).encode('utf-8'))
        exitFlag = 1
        sys.exit()
        
    def joinMem(self):
        ID = self.userinfoEnterID.text()
        PW = self.userinfoEnterPW.text()
        if len(ID) > 16:
            self.msgLabel.setText("ID의 최대 길이는 16입니다.")
        elif len(PW) > 32:
            self.msgLabel.setText("PW의 최대 길이는 32입니다.")
        else:
            menu = 2
            clntSock.send(repr(menu).encode('utf-8'))
            arr = (ID,PW)
            data_arr = pickle.dumps(arr)
            clntSock.send(data_arr)
            flag = clntSock.recv(1)
            if int(flag.decode('utf-8')) == 0:
                self.msgLabel.setText("이미 존재하는 ID입니다")
            else:
                self.msgLabel.setText("회원가입에 성공하였습니다.")
        
    def login(self):
        global exitFlag
        global chattSock
        exitFlag = 0
        
        menu = 1
        clntSock.send(repr(menu).encode('utf-8'))
        ID = self.userinfoEnterID.text()
        PW = self.userinfoEnterPW.text()

        arr = (ID,PW)
        data_arr = pickle.dumps(arr)
        clntSock.send(data_arr)
        flag = clntSock.recv(1)
        
        if int(flag) == 0:
            data = clntSock.recv(1024)
            index_arr = pickle.loads(data)
            index = index_arr[0]
            
            chattSock = socket(AF_INET, SOCK_STREAM)
            chattSock.connect(('127.0.0.1',(8081+index)))
            t = threading.Thread(target = self.recvChattingMsg, args = ())
            t.start()

            self.systemMsgText.append(ID+" 로 로그인하였습니다.")
            self.systemMsgText.append("1. 문제풀이 시 채팅을 보낼 수 없습니다.")
            self.systemMsgText.append("2. 절대로 '종료' 버튼을 통해서만 종료하십시오.")
            self.systemMsgText.append("3. 채팅을 위한 메세지 외에 따옴표를 입력하지 마십시오.")
        
        return int(flag.decode('utf-8'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PROJ()
    sys.exit(app.exec_())
