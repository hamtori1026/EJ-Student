import sys
from html.parser import HTMLParser
import http.cookiejar
import urllib
import urllib.request
import mysmtplib
import mimetypes
import folium
from xml.dom import minidom
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QTextEdit, QWidget, QDialog, QApplication, QMessageBox, QPushButton, QMainWindow
REG_KEY = '6a767be25cc06c13652d563c47a518eb9c8bc5db834b8b6dc30f3b39b68dac9d'
REG_KEY2 = 'K7U3xYzFL04Grub64QsC1fPKXQxB6%2BmW3s%2BU0Vs7ngtict1lo%2Fx3zIeX3dwbZnO%2FAr5xChaeRF2DlKQL5PxyBw%3D%3D' #공공데이터포털 인증키


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
        self.choiceNum = 0
        self._title = ""
        self._message = ""
        self._from_email = ""
        self._to_email = ""
        self._password = ""
        self._smtp_port = SMTP_PORT
        self._smtp_host = SMTP_HOST
        self._reg_key = REG_KEY
        self._reg_key2 = REG_KEY2

        self.pushButton.clicked.connect(self.searchName) # 이름 검색 버튼 이벤트
        self.pushButton_4.clicked.connect(self.searchByIngredient) # 재료 검색 버튼 이벤트
        self.pushButton_3.clicked.connect(self.searchByID) # ID 검색 버튼 이벤트
        self.pushButton_2.clicked.connect(self.settingEmail) # email 발송 버튼 이벤트
        self.pushButton_5.clicked.connect(self.sendEmail)
        self.pushButton_6.clicked.connect(self.sendEmail)
        self.pushButton_7.clicked.connect(self.sendEmail)
        self.pushButton_8.clicked.connect(self.searchAddressSuwon)
        self.pushButton_10.clicked.connect(self.searchAddressYeosu)
        self.pushButton_11.clicked.connect(self.searchAddressGeoje)
        self.pushButton_9.clicked.connect(self.choiceMap)


        writeImageWidget(self.pic1,"/Img/","pic1","png")
        self.pic1.setScaledContents(True)
        writeImageWidget(self.pic2,"/Img/","pic2","png")
        self.pic2.setScaledContents(True)
        writeImageWidget(self.ingrePic2,"/Img/","ingrePic2","png")
        self.ingrePic2.setScaledContents(True)
        writeImageWidget(self.mainpic,"/Img/","main","png")
        self.mainpic.setScaledContents(True)
        writeImageWidget(self.idPic2,"/Img/","ingrePic2","png")
        self.idPic2.setScaledContents(True)
        writeImageWidget(self.mailBox,"/Img/","mail","jpg")
        self.mailBox.setScaledContents(True)

        #writeImageWidget(self.display,"/","cookPic","png")
        #self.display_img.setScaledContents(True);
        #self.display.setPixmap(QPixmap('./img/' +  str("cookPic") + '.' + str("png")))

    def settingEmail(self):
        if self.pushButton_2.clicked:
            self.setFrom(self.textEdit.toPlainText())
            self.setPassword(self.textEdit_2.toPlainText())
            self.setTo(self.textEdit_3.toPlainText())
            self.setTitle(self.textEdit_6.toPlainText())
            self.textBrowser_14.setText("메일 계정 세팅 완료")
    #메일 발송
    def sendEmail(self):
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
        self.textBrowser_15.setText("***메일 발송 완료***")
        self.textBrowser_16.setText("***메일 발송 완료***")
        self.textBrowser_17.setText("***메일 발송 완료***")


        s.close()
####### 지도 서치

    def searchAddressYeosu(self) :  # 여수 지역
        url = "http://data.jeonnam.go.kr/rest/namdotourist/getNdtrConvmarketList?authApiKey="+self._reg_key2+"&tourNm=%EC%97%AC%EC%88%98"
        res = self.opener.open(url)
        self.textBrowser_19.clear()

        self.choiceNum = 2
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildMessageYeosu(res)
        
    def searchAddressSuwon(self) : # 수원 지역
        url = "http://api.suwon.go.kr/openapi-data/service/TradMarket/getTradMarket?pageNo=2&numOfRows=10&ServiceKey="+self._reg_key2
        res = self.opener.open(url)
        self.textBrowser_19.clear()

        self.choiceNum = 1
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildMessageSuwon(res)
        
    def searchAddressGeoje(self) : # 거제 지역
        self.choiceNum = 3
        self.textBrowser_19.clear()

        url = "http://data.geoje.go.kr/rfcapi/rest/geojemarket/getGeojemarketList?authApiKey="+self._reg_key2
        res = self.opener.open(url)
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildMessageGeoje(res)

############ 맵 저장 서치 #########
    def createMAPSuwon(self) : # 수원 지역
        url = "http://api.suwon.go.kr/openapi-data/service/TradMarket/getTradMarket?pageNo=2&numOfRows=10&ServiceKey="+self._reg_key2
        res = self.opener.open(url)

        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildSuwonCreate(res)
        
    def createMAPYeosu(self) : # 여수 지역
        url = "http://data.jeonnam.go.kr/rest/namdotourist/getNdtrConvmarketList?authApiKey="+self._reg_key2+"&tourNm=%EC%97%AC%EC%88%98"
        res = self.opener.open(url)
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildYeosuCreate(res)
        
    def createMAPGeoje(self) : # 거제 지역
        url = "http://data.geoje.go.kr/rfcapi/rest/geojemarket/getGeojemarketList?authApiKey="+self._reg_key2
        res = self.opener.open(url)

        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildGeojeCreate(res)


####### 기존 서치 
    #이름 검색
    def searchName(self):
        if self.pushButton.clicked:
            nameSave = self.textEdit_4.toPlainText()
            self.textBrowser_15.clear()

        url = "http://data.mafra.go.kr:7080/openapi/"+self._reg_key+"/xml/Grid_20150827000000000226_1/1/5?RECIPE_NM_KO="
            #6a767be25cc06c13652d563c47a518eb9c8bc5db834b8b6dc30f3b39b68dac9d
        #"http://data.mafra.go.kr:7080/openapi/6a767be25cc06c13652d563c47a518eb9c8bc5db834b8b6dc30f3b39b68dac9d/xml/Grid_20150827000000000226_1/1/5?RECIPE_NM_KO=잡채
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
            self.textBrowser_16.clear()


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
            self.textBrowser_17.clear()

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


############## 기존 메시지 빌더 ################

    def buildMessage(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()
        s = ""
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 
        ItemDomList = GetItemDomList(res)
        ItemList = xmlParser(ItemDomList)
        try:
            for xmlItem in ItemList:
                download_image(xmlItem['IMG_URL'].decode("cp949"),"cookPic")
                writeImageWidget(self.display_img,"/", "cookPic", "jpg")
                self.display_img.setScaledContents(True)
                self.textBrowser_2.setText(xmlItem['RECIPE_ID'].decode("cp949"))
                self.textBrowser_4.setText(xmlItem['RECIPE_NM_KO'].decode("cp949"))
                self.textBrowser_5.setText(xmlItem['CALORIE'].decode("cp949"))
                self.textBrowser_6.setText(xmlItem['IRDNT_CODE'].decode("cp949"))
                self.textBrowser_7.setText(xmlItem['PC_NM'].decode("cp949"))    
                self.textBrowser_8.setText(xmlItem['QNT'].decode("cp949"))
                self.textBrowser_13.setText(xmlItem['TY_NM'].decode("cp949"))
                self.textBrowser_11.setText(xmlItem['LEVEL_NM'].decode("cp949"))
                self.textBrowser_10.setText(xmlItem['NATION_NM'].decode("cp949"))
                self.textBrowser_12.setText(xmlItem['COOKING_TIME'].decode("cp949"))
                self.textBrowser_9.setText(xmlItem['SUMRY'].decode("cp949"))
                s += "********<<레시피 ID>>********\n" + xmlItem['RECIPE_ID'].decode("cp949") + "\n<<요리 이름>>\n" + xmlItem['RECIPE_NM_KO'].decode("cp949") + "\n<<설명>>\n" + xmlItem['SUMRY'].decode("cp949") + "\n<<칼로리>>\n" + xmlItem['CALORIE'].decode("cp949") + "\n<<주 재료>>\n" + xmlItem['IRDNT_CODE'].decode("cp949") + "\n<<가격>>\n" + xmlItem['PC_NM'].decode("cp949") + "\n<<권장 인원>>\n" + xmlItem['QNT'].decode("cp949") + "\n<<타입>>\n" + xmlItem['TY_NM'].decode("cp949") + "\n<<난이도>>\n" + xmlItem['LEVEL_NM'].decode("cp949") + "\n<<국가>>\n" + xmlItem['NATION_NM'].decode("cp949") + "\n<<요리 시간>>\n" + xmlItem['COOKING_TIME'].decode("cp949")
                self.currentRecipe = s
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

    def buildMessage1(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()
        s = ""
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 
        ItemDomList = GetItemDomList(res)
        ItemList = idParser(ItemDomList)
        try:
            for xmlItem in ItemList:
                s += xmlItem['ROW_NUM'].decode("cp949") + " 번 \n" + xmlItem['COOKING_DC'].decode("cp949") + "\n"
                self.currentRecipe = s
            self.textBrowser_3.setText(s)
    #self.textBrowser_3.clear()
            #self.textBrowser_3.setText(self.currentRecipe)
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

    def buildMessage2(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()
        s = ""
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 
        ItemDomList = GetItemDomList(res)
        ItemList = ingreParser(ItemDomList)
        try:
            for xmlItem in ItemList:
                s += "<<음식 ID>> : " + xmlItem['RECIPE_ID'].decode("cp949")+"\n<<재료 이름>> : "+xmlItem['IRDNT_NM'].decode("cp949")+"\n<<재료 양>> : "+xmlItem['IRDNT_CPCTY'].decode("cp949")+"\n<<주재료 or 부재료>> : "+xmlItem['IRDNT_TY_NM'].decode("cp949") +"\n************************\n"
                self.currentRecipe = s
            self.textBrowser.setText(s)

        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

############## 지도 메시지 빌더 #############
    def buildMessageYeosu(self, xml_buffer3): # TODO need layout building. 
        res = xml_buffer3.read()
        s = ""
        ItemDomList = GetItemDomListYeosu(res)
        ItemList = YeosuxmlParser(ItemDomList)
        try:
            
            for xmlItem in ItemList:
                s += "명칭 : " + xmlItem['tourNm'].decode("cp949") + "\n주소 : " + xmlItem['tourAddr'].decode("cp949") + "\n전화번호 : " + xmlItem['tourTel'].decode("cp949") + "\n위도 : " + xmlItem['tourYpos'].decode("cp949") + "\n경도 : " + xmlItem['tourXpos'].decode("cp949") + "\n*****************\n"
            self.textBrowser_18.setText(s)
              
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True
        
        
    def buildMessageSuwon(self, xml_buffer3): # TODO need layout building. 
        res = xml_buffer3.read()
        s = ""
        ItemDomList = GetItemDomListSuwon(res)
        ItemList = SuwonxmlParser(ItemDomList)
        try:
            
            for xmlItem in ItemList:
                s += "명칭 : " + xmlItem['plcName'].decode("cp949") + "\n주소 : " + xmlItem['newAddr'].decode("cp949") + "\n전화번호 : " + xmlItem['tellnum'].decode("cp949") + "\n위도 : " + xmlItem['lat'].decode("cp949") + "\n경도 : " + xmlItem['lng'].decode("cp949") + "\n*****************\n"
            self.textBrowser_18.setText(s)

                
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True
        
    def buildMessageGeoje(self, xml_buffer3): # TODO need layout building. 
        res = xml_buffer3.read()
        s = ""
        ItemDomList = GetItemDomListGeoje(res)
        ItemList = GeojexmlParser(ItemDomList)
        try:
            
            for xmlItem in ItemList:
                s += "명칭 : " + xmlItem['marketNm'].decode("cp949") + "\n주소 : " + xmlItem['marketNewAddr'].decode("cp949") + "\n전화번호 : " + xmlItem['marketTel'].decode("cp949") + "\n위도 : " + xmlItem['marketYpos'].decode("cp949") + "\n경도 : " + xmlItem['marketXpos'].decode("cp949") + "\n*****************\n"
            self.textBrowser_18.setText(s)

                
                
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True
        

############### 지도 만들기 
    def choiceMap(self):
        if self.choiceNum == 1:
           self.createMAPSuwon()
        if self.choiceNum == 2:
           self.createMAPYeosu()
        if self.choiceNum == 3:
           self.createMAPGeoje()
        self.textBrowser_19.setText("맵 저장 완료!")
        
    def buildSuwonCreate(self,xml_buffer3) :    #수원 지도
        res = xml_buffer3.read()
        ItemDomList = GetItemDomListSuwon(res)
        ItemList = SuwonxmlParser(ItemDomList)
        try :
            map_1 = folium.Map(location=[37.280009, 127.007823], zoom_start=13)
            
            for xmlItem in ItemList:
                map_1.polygon_marker(location=[xmlItem['lat'].decode("cp949"), xmlItem['lng'].decode("cp949")], popup=xmlItem['plcName'].decode("cp949"), fill_color='#132b5e', radius=15)

            map_1.create_map(path='MakeSuwonMap.html')
            print("\n지도가 생성되었습니다. Name = [MakeSuwonMap.html]")
            
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True
        
    def buildYeosuCreate(self,xml_buffer3) :    #여수 지도
        res = xml_buffer3.read()
        ItemDomList = GetItemDomListYeosu(res)
        ItemList = YeosuxmlParser(ItemDomList)
        try :
            map_1 = folium.Map(location=[34.780260, 127.661807], zoom_start=13)
            
            for xmlItem in ItemList:
                map_1.polygon_marker(location=[xmlItem['tourYpos'].decode("cp949"), xmlItem['tourXpos'].decode("cp949")], popup=xmlItem['tourNm'].decode("cp949"), fill_color='#132b5e', radius=15)

            map_1.create_map(path='MakeYeosuMap.html')    
            print("\n지도가 생성되었습니다. Name = [MakeYeosuMap.html]") 
            
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True
        
    def buildGeojeCreate(self,xml_buffer3) :    #거제 지도
        res = xml_buffer3.read()
        ItemDomList = GetItemDomListGeoje(res)
        ItemList = GeojexmlParser(ItemDomList)
        try :
            map_1 = folium.Map(location=[34.880580, 128.622389], zoom_start=13) #거제 위도,경도
            
            for xmlItem in ItemList:
                map_1.polygon_marker(location=[xmlItem['marketYpos'].decode("cp949"), xmlItem['marketXpos'].decode("cp949")], popup=xmlItem['marketNm'].decode("cp949"), fill_color='#132b5e', radius=15)

            map_1.create_map(path='MakeGeojeMap.html')    
            print("\n지도가 생성되었습니다. Name = [MakeGeojeMap.html]")
            
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

def GetItemDomList(XML):
    DOM = minidom.parseString(XML)
    ItemDomList = DOM.getElementsByTagName('row')
    return ItemDomList

def GetTextFromItem(Item,TagName):
    Text = Item.getElementsByTagName(TagName)[0].firstChild.data
    Text = Text.encode('euc-kr')
    return Text

def xmlParser(itemDomList):
    itemList = []
    for itemDom in itemDomList:
        Item = {}
        Item['IRDNT_CODE'] = GetTextFromItem(itemDom,'IRDNT_CODE') # 재료
        Item['SUMRY'] = GetTextFromItem(itemDom,'SUMRY') # 설명
        Item['CALORIE'] = GetTextFromItem(itemDom,'CALORIE') # 칼로리
        Item['RECIPE_NM_KO'] = GetTextFromItem(itemDom,'RECIPE_NM_KO') # 요리 이름
        Item['QNT'] = GetTextFromItem(itemDom,'QNT') # 권장 인원
        Item['PC_NM'] = GetTextFromItem(itemDom,'PC_NM') # 가격
        Item['TY_NM'] = GetTextFromItem(itemDom,'TY_NM') # 종류
        Item['LEVEL_NM'] = GetTextFromItem(itemDom,'LEVEL_NM') # 난이도
        Item['NATION_NM'] = GetTextFromItem(itemDom,'NATION_NM') # 국가
        Item['RECIPE_ID'] = GetTextFromItem(itemDom,'RECIPE_ID') # 레시피 ID
        Item['COOKING_TIME'] = GetTextFromItem(itemDom,'COOKING_TIME') # 요리 시간     
        Item['IMG_URL'] = GetTextFromItem(itemDom,'IMG_URL') # 요리 사진
        itemList.append(Item)
    return itemList

def ingreParser(itemDomList):
    itemList = []
    for itemDom in itemDomList:
        Item = {}
        Item['ROW_NUM'] = GetTextFromItem(itemDom,'ROW_NUM') # ROW NUM
        Item['IRDNT_NM'] = GetTextFromItem(itemDom,'IRDNT_NM') # 재료 이름
        Item['IRDNT_CPCTY'] = GetTextFromItem(itemDom,'IRDNT_CPCTY') # 재료 양
        Item['IRDNT_TY_NM'] = GetTextFromItem(itemDom,'IRDNT_TY_NM') # 부/주재료
        Item['RECIPE_ID'] = GetTextFromItem(itemDom,'RECIPE_ID') # 검색용 아이디
        itemList.append(Item) 
    return itemList
       # Item['IRDNT_NM'] = GetTextFromItem(itemDom,'IRDNT_NM')

def idParser(itemDomList):
    itemList = []
    for itemDom in itemDomList:
        Item = {}
        Item['ROW_NUM'] = GetTextFromItem(itemDom,'ROW_NUM')
        Item['COOKING_DC'] = GetTextFromItem(itemDom,'COOKING_DC') # 요리 과정
        itemList.append(Item) 
    return itemList

##### 맵 관련

def YeosuxmlParser(itemDomList) :  #여수
    itemList = []
    for itemDom in itemDomList :
        Item = {}
        Item['tourNm'] = GetTextFromItem(itemDom,'tourNm') #명칭
        Item['tourZoneCd'] = GetTextFromItem(itemDom,'tourZoneCd') #지역코드
        Item['tourZoneNm'] = GetTextFromItem(itemDom,'tourZoneNm') #지역명
        Item['tourAddr'] = GetTextFromItem(itemDom,'tourAddr') #주소
        Item['tourTel'] = GetTextFromItem(itemDom,'tourTel') # 전화번호
        Item['tourYpos'] = GetTextFromItem(itemDom,'tourYpos') # 위도
        Item['tourXpos'] = GetTextFromItem(itemDom,'tourXpos') # 경도
        Item['tourId'] = GetTextFromItem(itemDom,'tourId') # 시장 고유코드
        itemList.append(Item)
    return itemList
    
def SuwonxmlParser(itemDomList) :  #수원
    itemList = []
    for itemDom in itemDomList :
        Item = {}
        Item['newAddr'] = GetTextFromItem(itemDom,'newAddr') #지역주소
        Item['plcName'] = GetTextFromItem(itemDom,'plcName') #명칭
        Item['tellnum'] = GetTextFromItem(itemDom,'tellnum') #전화번호
        Item['lat'] = GetTextFromItem(itemDom,'lat') # 위도
        Item['lng'] = GetTextFromItem(itemDom,'lng') # 경도
        itemList.append(Item)
    return itemList
    
def GeojexmlParser(itemDomList) :  #거제
    itemList = []
    for itemDom in itemDomList :
        Item = {}
        Item['marketNewAddr'] = GetTextFromItem(itemDom,'marketNewAddr') #지역주소
        Item['marketNm'] = GetTextFromItem(itemDom,'marketNm') #명칭
        Item['marketTel'] = GetTextFromItem(itemDom,'marketTel') #전화번호
        Item['marketYpos'] = GetTextFromItem(itemDom,'marketYpos') # 위도
        Item['marketXpos'] = GetTextFromItem(itemDom,'marketXpos') # 경도
        itemList.append(Item)
    return itemList

def GetItemDomListYeosu(XML):  #여수
    DOM = minidom.parseString(XML)
    ItemDomList2 = DOM.getElementsByTagName('list')
    return ItemDomList2
    
def GetItemDomListSuwon(XML):  #수원
    DOM = minidom.parseString(XML)
    ItemDomList2 = DOM.getElementsByTagName('item')
    return ItemDomList2
    
def GetItemDomListGeoje(XML):  #거제
    DOM = minidom.parseString(XML)
    ItemDomList2 = DOM.getElementsByTagName('list')
    return ItemDomList2


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def download_image(url, filename):
    full_name =  str(filename) + ".jpg"
    urllib.request.urlretrieve(url, full_name)


def writeImageWidget(Widget, Address, File, Extension):
    # 레이블에 이미지를 넣어준다. 파일 주소, 파일명, 확장자 순으로 받아서 넣어준다.
    Widget.setPixmap(QPixmap('.' + str(Address) + str(File) + '.' + str(Extension)))

if __name__ == '__main__':

    app = QApplication(sys.argv)

    form = MainWindow()
    form.show()

    sys.exit(app.exec_())
