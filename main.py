import time
import discardOperate
import guiOperate

# 定义一个变量来控制循环
running = True

# 使用try-except语句来捕获键盘中断异常
try:
    # 当running为True时，循环执行函数
    while running:
        discardOperate.setUserName(14)
        # guiOperate.writeTokenToExcel()
        # 可以在这里添加一些延时或其他操作，例如：
        time.sleep(100)
except KeyboardInterrupt:
    # 当按下ctrl+c时，设置running为False并退出循环
    running = False
    print('程序已停止')
