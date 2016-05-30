from html.parser import HTMLParser
import http.cookiejar
import urllib
import mysmtplib
import mimetypes
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

REG_KEY = '6a767be25cc06c13652d563c47a518eb9c8bc5db834b8b6dc30f3b39b68dac9d'
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
            self.currentRecipe = strip_tags("ID : "+res.decode("utf-8").split("recipeSn=")[1])
            print(self.currentRecipe)
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
            self.currentRecipe = strip_tags("ID : "+res.decode("utf-8").split("recipeSn=")[0])
            print(self.currentRecipe)
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
            self.currentRecipe = strip_tags("ID : "+res.decode("utf-8").split("recipeSn=")[0])
            print(self.currentRecipe)
        except Exception as e:
            self.__debug_print("Parsing Error! :" + str(e))
        return True

    def searchByName(self, name):
        self.__debug_print("searchByName : " + name.decode("utf-8"))
        url = "http://data.mafra.go.kr:7080/openapi/"+self._reg_key+"/xml/Grid_20150827000000000226_1/1/5?RECIPE_NM_KO="
        strSave = urllib.parse.quote(name)
        res = self.opener.open(url+strSave)
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

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()