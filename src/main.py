from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import difflib
import time

def getMyStudyPage(driver):
    driver.find_elements_by_class_name("linkItem")[1].click()
    driver.switch_to.window(driver.window_handles[-1])

def getExamPage(driver):
    for link in driver.find_elements_by_xpath("//*[@href]"):
        if(link.get_attribute("href") == "https://pc.xuexi.cn/points/exam-index.html"):
            link.click()
    driver.switch_to.window(driver.window_handles[-1])

def getExamPracticePage(driver):
    driver.find_elements_by_class_name("block")[0].click()
    driver.switch_to.window(driver.window_handles[-1])

def nextPractice(driver):
    if (driver.find_elements_by_tag_name("button")[0].get_attribute("innerText") == "再来一组"):
        driver.find_elements_by_tag_name("button")[0].click()

def chooseQue(driver, roughAnsArr, clickedFlag):
    choosableArr = driver.find_elements_by_class_name("choosable")
    for i in range(len(choosableArr)):
        for j in roughAnsArr:
            if difflib.SequenceMatcher(None, choosableArr[i].get_attribute("innerText")[3:], j).ratio() >= 0.8:
                choosableArr[i].click()
                clickedFlag = True

    if (clickedFlag == False):
        choosableArr[1].click()
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
    driver.find_elements_by_tag_name("button")[0].click()

def blankQue(driver, roughAnsArr):
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("question")[0])
    blankArr = driver.find_elements_by_class_name("blank")
    for i in range(len(blankArr)):
        blankArr[i].send_keys(roughAnsArr[i])
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
    driver.find_elements_by_tag_name("button")[0].click()

def otherQue(driver):
    tempArr = []
    falseArr = []

    for ans in driver.find_elements_by_class_name("false"):
        falseArr.append(ans.get_attribute("innerText"))
        print(ans.get_attribute("innerText"))

    for item in driver.find_elements_by_class_name("q-answer"):
        try:
            falseArr.index(item.get_attribute("innerText"))
        except ValueError:
            item.click()
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
    driver.find_elements_by_tag_name("button")[0].click()

def videoQue(driver):
    if (len(driver.find_elements_by_class_name("choosable")) != 0):
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("choosable")[0])
        driver.find_elements_by_class_name("choosable")[0].click()
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
        driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(1)
        driver.find_elements_by_tag_name("button")[0].click()
    else:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("blank")[0])
        videoBlankArr = driver.find_elements_by_class_name("blank")
        for blank in videoBlankArr:
            blank.send_keys("a")
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
        driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(1)
        driver.find_elements_by_tag_name("button")[0].click()

def getRoughAns(driver, roughAnsArr):
    fontArr = driver.find_elements_by_tag_name("font")
    for fontEL in fontArr:
        if (fontEL.get_attribute("innerText") != ""):
            roughAnsArr.append(fontEL.get_attribute("innerText"))

def run(driver, roughAnsArr):
    timer = 0
    clickedFlag = False

    while(timer < 5):
        ++timer
        time.sleep(2)
        roughAnsArr.clear()

        nextPractice(driver)

        if(len(driver.find_elements_by_class_name("tips")) != 0):
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("tips")[0])
            driver.find_elements_by_class_name("tips")[0].click()

            if (driver.find_elements_by_class_name("line-feed")[0].get_attribute("innerText") == "请观看视频"):
                driver.find_elements_by_class_name("tips")[0].click()
                videoQue(driver)

            getRoughAns(driver, roughAnsArr)

            time.sleep(1)
            driver.find_elements_by_class_name("tips")[0].click()
            print(roughAnsArr)

        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("question")[0])
        if len(driver.find_elements_by_class_name("false")) != 0:
            otherQue(driver)
        if len(driver.find_elements_by_class_name("choosable")) != 0:
            chooseQue(driver, roughAnsArr, clickedFlag)
        else:
            blankQue(driver, roughAnsArr)


def main():
    roughAnsArr = []
    print(roughAnsArr)
    clickedFlag = False
    chromeOption = webdriver.ChromeOptions()
    userDataDir = "--user-data-dir=C:\\Users\\17482\\AppData\\Local\\Google\\Chrome\\User Data1"
    chromeOption.add_argument(userDataDir)
    driver = webdriver.Chrome(options=chromeOption, executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
    driver.get("https://www.xuexi.cn/")
    driver.implicitly_wait(5)

    getMyStudyPage(driver)

    getExamPage(driver)

    getExamPracticePage(driver)

    run(driver, roughAnsArr)
    input()




if __name__ == "__main__":
    main()