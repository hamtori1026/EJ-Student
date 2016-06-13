from html.parser import HTMLParser
import http.cookiejar
import urllib
import mysmtplib
import mimetypes
import folium
from xml.dom.minidom import *
from xml.dom import minidom
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

REG_KEY = '6a767be25cc06c13652d563c47a518eb9c8bc5db834b8b6dc30f3b39b68dac9d'
REG_KEY2 = 'K7U3xYzFL04Grub64QsC1fPKXQxB6%2BmW3s%2BU0Vs7ngtict1lo%2Fx3zIeX3dwbZnO%2FAr5xChaeRF2DlKQL5PxyBw%3D%3D' #공공데이터포털 인증키
SMTP_HOST = "smtp.gmail.com" # Gmail SMTP 서버 주소.
SMTP_PORT = "587"

class MyObjectEngine(object):
    """description of class"""

    def __init__(self):
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
        self._reg_key2 = REG_KEY2
    def __debug_print(self, message):
        if not self._debug: return
        print(type(self).__name__, ">", message)
    
    def buildMessage(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()

        #print(res)
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 
        ItemDomList = GetItemDomList(res)
        ItemList = xmlParser(ItemDomList)

        try:
            for xmlItem in ItemList:
                print("********<<레시피 ID>>********")
                print(xmlItem['RECIPE_ID'].decode("cp949"))
                print("<<요리 이름>>")
                print(xmlItem['RECIPE_NM_KO'].decode("cp949"))
                print("<<설명>>")
                print(xmlItem['SUMRY'].decode("cp949"))
                print("<<칼로리>>")
                print(xmlItem['CALORIE'].decode("cp949"))
                print("<<주 재료>>")
                print(xmlItem['IRDNT_CODE'].decode("cp949"))
                print("<<가격>>")
                print(xmlItem['PC_NM'].decode("cp949"))    
                print("<<권장 인원>>")
                print(xmlItem['QNT'].decode("cp949"))
                print("<<타입>>")
                print(xmlItem['TY_NM'].decode("cp949"))
                print("<<난이도>>")
                print(xmlItem['LEVEL_NM'].decode("cp949"))
                print("<<국가>>")
                print(xmlItem['NATION_NM'].decode("cp949"))
                print("<<요리 시간>>")
                print(xmlItem['COOKING_TIME'].decode("cp949"))
                print("<<이미지 URL>>")
                print(xmlItem['IMG_URL'].decode("cp949"))
            #self.currentRecipe = strip_tags("ID : "+res.decode("utf-8").split("Sn=")[1])
            #print(self.currentRecipe)
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

    def buildMessage1(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 

        ItemDomList = GetItemDomList(res)
        ItemList = idParser(ItemDomList)

        #for xmlItem2 in ItemList2:
        #    print(xmlItem2['RECIPE_NM_KO'].decode("cp949"))

            
        print(" << 요리 과정 >> ")
        try:
            for xmlItem in ItemList:
                print(xmlItem['ROW_NUM'].decode("cp949") + " 번 ")
                print(xmlItem['COOKING_DC'].decode("cp949"))
            self.currentRecipe = strip_tags(res.decode("utf-8").split("recipeSn=")[0])
            #print(self.currentRecipe)
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True
    def buildMessage2(self, xml_buffer): # TODO need layout building. 
        res = xml_buffer.read()
        # TODO if you want to update current status, write here. :) 
        # >example
        #  self.currentRecipeName = namevar
        #  self.currentRecipeID = id 

        ItemDomList = GetItemDomList(res)
        ItemList = ingreParser(ItemDomList)
        #print(ItemList)
        try:
            for xmlItem in ItemList:
                print("***************************")
                print("<<음식 ID>>")
                print(xmlItem['RECIPE_ID'].decode("cp949"))
                print("<<재료 이름>>")
                print(xmlItem['IRDNT_NM'].decode("cp949"))
                print("<<재료 양>>")
                print(xmlItem['IRDNT_CPCTY'].decode("cp949"))
                print("<<주재료or부재료>>")
                print(xmlItem['IRDNT_TY_NM'].decode("cp949"))
                print("***************************")
           #self.currentRecipe = strip_tags(res.decode("utf-8").split("recipeSn=")[0])
            #print(self.currentRecipe)
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

###################        # 지도 빌드

    def buildMessageYeosu(self, xml_buffer3): # TODO need layout building. 
        res = xml_buffer3.read()
        ItemDomList = GetItemDomListYeosu(res)
        ItemList = YeosuxmlParser(ItemDomList)
        try:
            
            for xmlItem in ItemList:
                print("명칭")
                print("-> ",xmlItem['tourNm'].decode("cp949"))
                print("주소 : ")
                print("-> ",xmlItem['tourAddr'].decode("cp949"))
                print("전화번호")
                print("-> ",xmlItem['tourTel'].decode("cp949"))
                print("위도")
                print("-> ",xmlItem['tourYpos'].decode("cp949"))
                print("경도")
                print("-> ",xmlItem['tourXpos'].decode("cp949"),'\n\n')


            map_1 = folium.Map(location=[34.780260, 127.661807], zoom_start=13)
            
            for xmlItem in ItemList:
                map_1.polygon_marker(location=[xmlItem['tourYpos'].decode("cp949"), xmlItem['tourXpos'].decode("cp949")], popup=xmlItem['tourNm'].decode("cp949"), fill_color='#132b5e', radius=15)

            self.yeosuCreate(map_1)
              
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True
    
 
    def yeosuCreate(self,map_1):
        map_1.create_map(path='MakeYeosuMap.html')    
        print("\n지도가 생성되었습니다. Name = [MakeYeosuMap.html]")  
        
    def buildMessageSuwon(self, xml_buffer3): # TODO need layout building. 
        res = xml_buffer3.read()
        ItemDomList = GetItemDomListSuwon(res)
        ItemList = SuwonxmlParser(ItemDomList)
        try:
            
            for xmlItem in ItemList:
                print("명칭")
                print("-> ",xmlItem['plcName'].decode("cp949"))
                print("주소 : ")
                print("-> ",xmlItem['newAddr'].decode("cp949"))
                print("전화번호")
                print("-> ",xmlItem['tellnum'].decode("cp949"))
                print("위도")
                print("-> ",xmlItem['lat'].decode("cp949"))
                print("경도")
                print("-> ",xmlItem['lng'].decode("cp949"),'\n\n')
                
            
            map_1 = folium.Map(location=[37.280009, 127.007823], zoom_start=13)
            
            for xmlItem in ItemList:
                map_1.polygon_marker(location=[xmlItem['lat'].decode("cp949"), xmlItem['lng'].decode("cp949")], popup=xmlItem['plcName'].decode("cp949"), fill_color='#132b5e', radius=15)

            map_1.create_map(path='MakeSuwonMap.html')
            print("\n지도가 생성되었습니다. Name = [MakeSuwonMap.html]")
            
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True


    def buildMessageGeoje(self, xml_buffer3): # TODO need layout building. 
        res = xml_buffer3.read()
        ItemDomList = GetItemDomListGeoje(res)
        ItemList = GeojexmlParser(ItemDomList)
        try:
            
            for xmlItem in ItemList:
                print("명칭")
                print("-> ",xmlItem['marketNm'].decode("cp949"))
                print("주소 : ")
                print("-> ",xmlItem['marketNewAddr'].decode("cp949"))
                print("전화번호")
                print("-> ",xmlItem['marketTel'].decode("cp949"))
                print("위도")
                print("-> ",xmlItem['marketYpos'].decode("cp949"))
                print("경도")
                print("-> ",xmlItem['marketXpos'].decode("cp949"),'\n\n')
                
                
            map_1 = folium.Map(location=[34.880580, 128.622389], zoom_start=13) #거제 위도,경도
            
            for xmlItem in ItemList:
                map_1.polygon_marker(location=[xmlItem['marketYpos'].decode("cp949"), xmlItem['marketXpos'].decode("cp949")], popup=xmlItem['marketNm'].decode("cp949"), fill_color='#132b5e', radius=15)

            map_1.create_map(path='MakeGeojeMap.html')    
            print("\n지도가 생성되었습니다. Name = [MakeGeojeMap.html]")
                
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True
    ################## 지도 서치 
    def searchAddressYeosu(self) :  # 여수 지역
        url = "http://data.jeonnam.go.kr/rest/namdotourist/getNdtrConvmarketList?authApiKey="+self._reg_key2+"&tourNm=%EC%97%AC%EC%88%98"
        res = self.opener.open(url)
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildMessageYeosu(res)
        
    def searchAddressSuwon(self) : # 수원 지역
        url = "http://api.suwon.go.kr/openapi-data/service/TradMarket/getTradMarket?pageNo=2&numOfRows=10&ServiceKey="+self._reg_key2
        res = self.opener.open(url)
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildMessageSuwon(res)
        
    def searchAddressGeoje(self) : # 거제 지역
        url = "http://data.geoje.go.kr/rfcapi/rest/geojemarket/getGeojemarketList?authApiKey="+self._reg_key2
        res = self.opener.open(url)
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildMessageGeoje(res)


################## 기존 서치
    def searchByName(self, name):
        self.__debug_print("searchByName : " + name.decode("utf-8"))
        url = "http://data.mafra.go.kr:7080/openapi/"+self._reg_key+"/xml/Grid_20150827000000000226_1/1/5?RECIPE_NM_KO="
        strSave = urllib.parse.quote(name)
        res = self.opener.open(url+strSave)
        #print(res)   
        #doc = parseString(url+strSave)
        #doc.toxml() 
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False
        
        return self.buildMessage(res)
    def searchByIngredient(self, ingredient):
        self.__debug_print("searchByIngredient : " + ingredient.decode("utf-8"))
        url = "http://data.mafra.go.kr:7080/openapi/"+self._reg_key+"/xml/Grid_20150827000000000227_1/1/15?IRDNT_NM="
        strSave = urllib.parse.quote(ingredient)
        res = self.opener.open(url+strSave)
        
        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False
        
        return self.buildMessage2(res)
    def searchByID(self, id):
        self.__debug_print("searchByID : " + str(id))
        url = "http://data.mafra.go.kr:7080/openapi/"+self._reg_key+"/xml/Grid_20150827000000000228_1/1/15?RECIPE_ID="
        res = self.opener.open(url+str(id))

        # url request failed
        if not res.getcode() == 200:
            self.currentRecipe = ""
            self.__debug_print("URL Open Error!!")
            return False

        return self.buildMessage1(res)

    def sendEmail(self):
        self.__debug_print("Email Send!")
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
        s.close()
    

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
    #print(ItemDomList)
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
