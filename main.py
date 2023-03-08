import time

from selenium import webdriver
from selenium.webdriver.common.by import By



def setUserName():
  # 定义用户名
  userNamePre = "say-so-"
  num = 1
  # 邀请链接
  url = "https://discord.gg/KK7bF6KAVt"

  options = webdriver.EdgeOptions()
  options.add_argument("-inprivate")
  driver = webdriver.Edge(options=options)
  # 反爬虫
  driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
      // 修改navigator.webdriver检测
      Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
      })
      // 修改window.navigator属性值
      window.navigator.chrome = {
        runtime: {},
        // etc.
      }
      // 修改插件信息
      const originalQuery = window.navigator.permissions.query;
      window.navigator.permissions.query = (parameters) => (
        parameters.name === 'notifications' ?
          Promise.resolve({ state: Notification.permission }) :
          originalQuery(parameters)
      );
    """
  })
  driver.get(url)
  inputElement = driver.find_element(By.NAME, "username")
  num = num + 1
  userName = userNamePre + str(num)
  inputElement.send_keys(userName)
  time.sleep(1)
  # 定位到button type="submit"的元素
  button = driver.find_element(By.XPATH, "//button[@type='submit']")
  # 点击该元素
  button.click()
  time.sleep(20)

setUserName()