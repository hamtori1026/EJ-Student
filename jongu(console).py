# -*- coding: utf-8 -*-


from MyObjectEngine import *
from getpass import *

#### Menu  implementation
def printMenu():
    print("\n★ 맛있는 요리♪ 맛있는 레시피! ★\n")
    print("=============♥Menu♥=============")
    print(">> 1. 검색 (요리 이름)\t[n]")
    print(">> 2. 검색 (재료 이름)\t[s]")
    print(">> 3. 검색 (레시피 ID)\t [c]")
    print(">> 4. 메일 발송 ()\t [m]")
    print("=============♥Menu♥=============")
    

def setEmailInformation(engine, message = None, message_input_mode = False):
    engine.setTitle(input('제목 작성 : '))
    engine.setFrom(str(input ('보내는 사람 email(GMAIL만 가능) :')))
    engine.setPassword(getpass (' 비밀번호 :'))
    engine.setTo(str(input ('받는 사람 email :')))
    if message_input_mode:
        engine.setMessage(str(input ('메시지 작성 :')))
    elif message != None:
        engine.setMessage(message)
    else:
        engine.setMessage(engine.currentRecipe)
    return
 
def main():
    engine = MyObjectEngine()
    menu = ''

    while menu != 'q':
        printMenu()
        menu = str(input ('원하는 메뉴를 선택하세요 >>'))

        if menu ==  'n':
            recipeNAME = input("요리 이름을 입력하세요>> ").encode('utf-8')
            engine.searchByName(recipeNAME)
        elif menu == 's':
            recipeIngredient = input("재료 이름을 입력하세요>> ").encode('utf-8')
            engine.searchByIngredient(recipeIngredient)
        elif menu == 'c':
            recipeID = input("레시피 번호를 입력하세요>> ")
            engine.searchByID(recipeID)

        elif menu == 'm':
            setEmailInformation(engine)
            engine.sendEmail()

if __name__ == '__main__':
    main()
    exit()

