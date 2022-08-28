# 셀레니움을 파이선으로 제어
# 두개의 창을 열어 xe게시판의 내용을 읽어 쇼핑몰 주문자동화
# visual atudio code 를 통해 수정함
# 주문서 100개를 자동으로 처리하는데 대략 200초 정도 소요됨.
# 예상보다 시간이 너무 오래걸려 selenium ide로 재개발 예정

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
import time 

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options)
action = ActionChains(driver)
driver.get('http://doldali.duckdns.org/')
H0 = driver.current_window_handle

driver.execute_script('window.open("http://stone-bridge.co.kr/member/login.php");')
H1 = driver.current_window_handle

time.sleep(.1)
driver.switch_to.window(driver.window_handles[0])
driver.find_element(By.XPATH,'//*[@id="fo_login_widget"]/a').click()
time.sleep(.1)
driver.find_element(By.ID,'user_id').send_keys('mgntbrandon@gmail.com')
<<<<<<< HEAD
driver.find_element(By.ID,'user_pw').send_keys('##')
=======
driver.find_element(By.ID,'user_pw').send_keys('..')
>>>>>>> f84ba783378839bd870c80026b9d43e35107184b
driver.find_element(By.XPATH,'//*[@id="acField"]/input[4]').click()
#driver.get('http://doldali.duckdns.org/index.php?mid=autoOrder')

driver.switch_to.window(driver.window_handles[1])
H1 = driver.current_window_handle

#time.sleep(2)
CondNo = 0

while CondNo  < 9:
    time.sleep(1)
    driver.switch_to.window(H0)
    time.sleep(1)

    try:
        driver.get('http://doldali.duckdns.org/index.php?mid=autoOrder')
        if(driver.find_element(By.ID,'Uid').text=='없습니다'):
            time.sleep(5)
            continue
    except:
        time.sleep(5)
        continue
    Uid = driver.find_element(By.ID,'Uid').text
    Upw = driver.find_element(By.ID,'Upw').text
    RowCnt = driver.find_element(By.ID,'RowCnt').text
    ColCnt = driver.find_element(By.ID,'ColCnt').text
    try:
        재고문제 = driver.find_element(By.ID,'재고부족').text
        print('재고에 문제가 있습니다')
        time.sleep(5)
        continue
    except:
        print('재고에 문제가 없습니다')
    driver.switch_to.window(H1)
    driver.get('http://stone-bridge.co.kr/member/login.php')
    time.sleep(.1)
    driver.find_element(By.ID,'loginId').clear()
    driver.find_element(By.ID,'loginId').send_keys(Uid)
    driver.find_element(By.ID,'loginPwd').send_keys(Upw)
    driver.find_element(By.XPATH,'//*[@id="formLogin"]/div[1]/button/em').click()
    time.sleep(2)
    driver.get('http://stone-bridge.co.kr/order/cart.php')
    바구니=driver.find_element(By.XPATH,'//*[@id="top"]/div[2]/div/ul/li[4]/span/strong').text
    if 바구니!='0':
        driver.find_element(By.XPATH,'//*[@id="content"]/div[1]/div/div[3]/div[1]/button[1]').click()
        try:
            pop=Alert(driver)
            pop.accept()
        except:
            print('장바구니없네')

    driver.switch_to.window(H0)
    z = [[0 for col in range(18)] for row in range(int(RowCnt))]
    for i in range(1,int(RowCnt)+1):
        for j in range(1,int(ColCnt)+1):
            Xp="//*[@id='content']/table/tbody/tr["+str(i+1)+"]/td["+str(j)+"]"
            z[i-1][j-1]=driver.find_element(By.XPATH,Xp).text
            #print(Xp)
    driver.switch_to.window(H1)
    time.sleep(2)
    for i in range(0,int(RowCnt)):
        errCnt=0
        while errCnt < 100:
            time.sleep(.5)
            url = 'http://stone-bridge.co.kr/goods/goods_view.php?goodsNo='+z[i][5]
            driver.get(url)
            time.sleep(.5)
            try: 
                Cp=driver.find_element(By.XPATH,'//*[@id="frmView"]/div/div[4]')
                print("==== XPATH {0}가 통과됨 =========".format(i))
                break
            except:
                errCnt = errCnt + 1
                print("XPATH 에러가  i 값은 {0} errCnt {1} ".format(i,errCnt))
                continue

        Cp.click()
        Cp.click()

        arr = z[i][6].split('-')
        print(arr)
        for l in range(0,int(arr[0])+1):
            print('down key press')
            action.key_down(Keys.DOWN).key_up(Keys.DOWN).perform()

        action.key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
        time.sleep(0.2)
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        action.send_keys(z[i][10]).perform()
        if(z[i][0]=='묶음예정'):
            driver.find_element(By.XPATH,'//*[@id="cartBtn"]/em').click()
            print('묶음예정클릭')
        elif(z[i][0]=='묶음발송') or (z[i][0]=='예약'):   
            if(z[i][0]=='묶음발송'): 
                driver.find_element(By.XPATH,'//*[@id="cartBtn"]/em').click()
                time.sleep(1)
                cp = driver.find_element(By.XPATH,'//*[@id="content"]/div[1]/div/div[3]/div[2]/button[1]')
                #cp.click()
                cp.click()
                time.sleep(.2)
                print('묶음발송클릭')
            elif(z[i][0]=='예약'):  
                print('예약클릭')
                driver.find_element(By.XPATH,'//*[@id="frmView"]/div/div[6]/a[3]/em').click()

            #직접입력클릭
            driver.find_element(By.XPATH,'//*[@id="fds-order-info"]/div[3]/table/tbody/tr[1]/td/span[3]/label').click()
            #우편번호
            driver.find_element(By.NAME,'receiverZonecode').send_keys(z[i][15]) #우편변호
            driver.find_element(By.NAME,'receiverAddress').send_keys(z[i][16])  #주소
            driver.find_element(By.NAME,'receiverPhone').send_keys(z[i][13])    #전화
            driver.find_element(By.NAME,'receiverCellPhone').send_keys(z[i][14]) #휴대폰
            driver.find_element(By.NAME,'receiverName').send_keys(z[i][12]) #이름
            driver.find_element(By.NAME,'receiverAddressSub').send_keys(z[i][12]) #이름으로 대체
            driver.find_element(By.NAME,'orderMemo').send_keys(z[i][17]) #남기는말
            
            print(z[i][16]+z[i][12])
            #예치금사용 클릭
            driver.find_element(By.XPATH,'//*[@id="fds-order-info"]/div[4]/table/tbody/tr[8]/td/span[2]/label').click()
            #결제정보 확인 클릭
            driver.find_element(By.XPATH,'//*[@id="fds-order-info"]/div[5]/div[2]/div[2]/span/label').click()
            print('주문클릭전')
            driver.find_element(By.XPATH,'//*[@id="fds-order-info"]/div[5]/div[2]/div[3]/button/em').click()
            print('주문클릭후')
            try:
                pop=Alert(driver)
                pop.accept()
                print('자동화 주문버튼클릭 문제발생 ')
            except:
                pass
            print('주문클릭 완료!!')
        time.sleep(1)
        #element = driver.find_element_by_xpath('//*[@id="SelectOptionID"]')
        #drp = Select(element)
        #drp.select_by_index(0)
        #driver.find_element_by_xpath('//*[@id="frmView"]/div/div[4]/div/div/div').click()
        #print('배열의갯수')
        #print(len(drp.options))
        #all_options=drp.options
        #for option in all_options:
        #    print('내용')
        #    print(option.text)
        #if z[i][0]=='예약':
        #    print(z[i][5])
        #else :

        #no = input("숫자를 입력하세요: ")
    #print(z)
    
    #driver.find_element_by_xpath('//*[@id="fds-order-info"]/div[3]/table/tbody/tr[1]/td/span[3]/label').click()
    #driver.find_element_by_name('receiverAddress').send_keys('##')
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="top"]/div[2]/div/ul/li[1]/a').click()
    try:
        pop=Alert(driver)
        pop.accept()
    except:
        print('로그아웃 되었다')
    no = 1
    CondNo = int(no)


