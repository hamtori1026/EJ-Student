import sys
from html.parser import HTMLParser
import http.cookiejar
import urllib
import mysmtplib
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication
REG_KEY = '6a767be25cc06c13652d563c47a518eb9c8bc5db834b8b6dc30f3b39b68dac9d'
SMTP_HOST = "smtp.gmail.com" # Gmail SMTP 서버 주소.
SMTP_PORT = "587"
import module1

class MainWindow(QDialog, module1.Ui_Dialog):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.currentRecipe = "" # 
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        self._debug = True
        self._title = ""
        self._message = ""
        self._from_email = ""
        self._to_email = ""
        self._password = ""
        self._smtp_port = SMTP_PORT
        self._smtp_host = SMTP_HOST
        self._reg_key = REG_KEY
        self.pushButton.clicked.connect(self.searchName) # 이름 검색 버튼 이벤트
        self.pushButton_4.clicked.connect(self.searchByIngredient) # 재료 검색 버튼 이벤트
        self.pushButton_3.clicked.connect(self.searchByID) # ID 검색 버튼 이벤트
        self.pushButton_2.clicked.connect(self.sendEmail) # email 발송 버튼 이벤트

    #메일 발송
    def sendEmail(self):
        if self.pushButton_2.clicked:
            self.setFrom(self.textEdit.toPlainText())
            self.setPassword(self.textEdit_2.toPlainText())
            self.setTo(self.textEdit_3.toPlainText())
            self.setTitle(self.textEdit_6.toPlainText())
            self.setMessage(self.currentRecipe)

        msg = MIMEText(self._message, 'plain')
        msg['Subject'] = self._title
        msg['From'] = self._from_email
        msg['To'] = self._to_email
        
            
        s = mysmtplib.MySMTP(self._smtp_host,self._smtp_port)
        s.ehlo()
        s.starttls()
        s.ehlo()
        try:
            s.login(self._from_email, self._password)    # 로긴을 합니다. 
        except Exception as e:
            self.__debug_print("Login Error! :" + str(e))

            return False
        s.sendmail(self._from_email , [self._to_email], msg.as_string())
        self.__debug_print("메일 발송 완료")
        s.close()

    #이름 검색
    def searchName(self):
        if self.pushButton.clicked:
            nameSave = self.textEdit_4.toPlainText()

        url = "http://data.mafra.go.kr:7080/openapi/"+self._reg_key+"/xml/Grid_20150827000000000226_1/1/5?RECIPE_NM_KO="
        strSave = urllib.parse.quote(nameSave)
        res = self.opener.open(url+strSave)
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False
        return self.buildMessage(res)
        
    #재료 검색
    def searchByIngredient(self):
        if self.pushButton_4.clicked:
            ingreSave = self.textEdit_7.toPlainText()

        url = "http://data.mafra.go.kr:7080/openapi/"+self._reg_key+"/xml/Grid_20150827000000000227_1/1/15?IRDNT_NM="
        strSave = urllib.parse.quote(ingreSave)
        res = self.opener.open(url+strSave)
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False
        
        return self.buildMessage2(res)
    
    #ID 검색
    def searchByID(self):
        if self.pushButton_3.clicked:
            idSave = self.textEdit_5.toPlainText()
        url = "http://data.mafra.go.kr:7080/openapi/"+self._reg_key+"/xml/Grid_20150827000000000228_1/1/15?RECIPE_ID="
        res = self.opener.open(url+idSave)

        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildMessage1(res)

    def __debug_print(self, message):
        if not self._debug: return
        print(type(self).__name__, ">", message)


    def buildMessage(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 
        try:
            self.textBrowser_2.clear()
            self.currentRecipe = strip_tags("ID : "+res.decode("utf-8").split("recipeSn=")[1])
            self.textBrowser_2.setText(self.currentRecipe)
           
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

    def buildMessage1(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 
        try:
            self.textBrowser_3.clear()
            self.currentRecipe = strip_tags("ID : "+res.decode("utf-8").split("recipeSn=")[0])
            self.textBrowser_3.setText(self.currentRecipe)
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

    def buildMessage2(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 
        try:
            self.textBrowser.clear()
            self.currentRecipe = strip_tags("ID : "+res.decode("utf-8").split("recipeSn=")[0])
            self.textBrowser.setText(self.currentRecipe)
            #self.listWidget_3.addItem(self.currentRecipe)
           
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

    def setTitle(self, title):
        self._title = title

    def setMessage(self, message):
        self._message = message

    def setFrom(self, from_email):
        self._from_email = from_email

    def setTo(self, to_email):
        self._to_email = to_email

    def setPassword(self, password):
        self._password = password

    def setSMPT(self, smpt_host, smpt_port):
        self._smtp_host = smpt_host
        self._smtp_port = smpt_port
    def debugDisable(self):
        self._debug = False
    def debugEnable(self):
        self._debug = True

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

if __name__ == '__main__':

    app = QApplication(sys.argv)

    form = MainWindow()
    form.show()

    sys.exit(app.exec_())
