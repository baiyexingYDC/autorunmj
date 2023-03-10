import time

import pyautogui


def write_token():
    pyautogui.PAUSE = 1
    pyautogui.FAILSAFE = True

    # 用模板图片找到目标位置
    excelTarget = pyautogui.locateOnScreen('wps_ico.png', confidence=0.8)

    # 如果找到了，就获取中心坐标
    if excelTarget:
        x, y = pyautogui.center(excelTarget)

        # 鼠标移动到目标位置
        pyautogui.moveTo(x, y)

        pyautogui.click()

        tokenTarget = pyautogui.locateOnScreen('excel_flag.png', confidence=0.8)

        if tokenTarget:
            x1, y1 = pyautogui.center(tokenTarget)

            pyautogui.moveTo(x1, y1)

            pyautogui.doubleClick()

            pyautogui.hotkey('ctrl', 'a')

            # 输入AAAA
            pyautogui.write('AAAA')

        else:
            print('没有找到token位置')
    else:
        # 如果没找到，输出日志
        print('没有找到模板图片')



