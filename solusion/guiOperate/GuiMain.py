import random
import time

import pyautogui
import GuiOperate

# 定义一个变量来控制循环
running = True

# 使用try-except语句来捕获键盘中断异常
try:
    # 当running为True时，循环执行函数
    while running:
        pyautogui.PAUSE = random.uniform(0.5, 1.5)
        GuiOperate.click("model/browser.png")
        GuiOperate.open_inprivate()
        GuiOperate.load_url("https://discord.gg/KK7bF6KAVt")
        GuiOperate.register("coming-" + str(random.uniform(1, 999999)))
        GuiOperate.solv_hCapcha()
        time.sleep(300)

except KeyboardInterrupt:
    # 当按下ctrl+c时，设置running为False并退出循环
    running = False
    print('程序已停止')
