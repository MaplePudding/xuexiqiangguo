from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import difflib
import time

def main():
    timer = 0
    roughAnsArr = []
    clickedFlag = False
    chromeOption = webdriver.ChromeOptions()
    userDataDir = "--user-data-dir=C:\\Users\\17482\\AppData\\Local\\Google\\Chrome\\User Data1"
    chromeOption.add_argument(userDataDir)
    driver = webdriver.Chrome(options=chromeOption, executable_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")
    driver.get("https://www.xuexi.cn/")
    driver.implicitly_wait(10)
    driver.find_elements_by_class_name("linkItem")[1].click()
    driver.switch_to.window(driver.window_handles[-1])
    for link in driver.find_elements_by_xpath("//*[@href]"):
        if(link.get_attribute("href") == "https://pc.xuexi.cn/points/exam-index.html"):
            link.click()
    driver.switch_to.window(driver.window_handles[-1])
    driver.find_elements_by_class_name("block")[0].click()
    driver.switch_to.window(driver.window_handles[-1])

    while(timer < 20):
        time.sleep(2)
        clickedFlag = False
        if(driver.find_elements_by_tag_name("button")[0].get_attribute("innerText") == "再来一组"):
            driver.find_elements_by_tag_name("button")[0].click()
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("tips")[0])
        driver.find_elements_by_class_name("tips")[0].click()
        if(driver.find_elements_by_class_name("tips")[0].get_attribute("innerText") == "请观看视频"):
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("blank")[0])
            videoBlandArr = driver.find_elements_by_class_name("blank")
            for blank in videoBlandArr:
                blank.send_keys("a")
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("button")[0])
            driver.find_elements_by_tag_name("button")[0].click()
        fontArr = driver.find_elements_by_tag_name("font")
        roughAnsArr.clear()
        for fontEL in fontArr:
            roughAnsArr.append(fontEL.get_attribute("innerText"))
        if(len(driver.find_elements_by_class_name("tips")) == 0):
            driver.find_elements_by_class_name("choosable")[0].click()
            time.sleep(1.5)
            driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(1)
        driver.find_elements_by_class_name("tips")[0].click()
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("question")[0])
        if len(driver.find_elements_by_class_name("choosable")) != 0:
            choosableArr = driver.find_elements_by_class_name("choosable")
            for i in range(len(choosableArr)):
                for j in roughAnsArr:
                    if difflib.SequenceMatcher(None, choosableArr[i].get_attribute("innerText")[3:], j).ratio() >= 0.8:
                        choosableArr[i].click()
                        clickedFlag = True

            if(clickedFlag == False):
                choosableArr[1].click()
            driver.find_elements_by_tag_name("button")[0].click()

        else:
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("question")[0])
            blankArr = driver.find_elements_by_class_name("blank")
            for i in range(len(blankArr)):
                blankArr[i].send_keys(roughAnsArr[i])
            driver.find_elements_by_tag_name("button")[0].click()
        ++timer
    input()




if __name__ == "__main__":
    main()