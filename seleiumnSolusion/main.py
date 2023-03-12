import time

from seleiumnSolusion import discardOperate

# 定义一个变量来控制循环
running = True

# 使用try-except语句来捕获键盘中断异常
try:
    # 当running为True时，循环执行函数'--inprivate ' \
    while running:
        # cmd = '"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" ' \
        #       '--remote-debugging-port=9222 ' \
        #       '--user-data-dir="C:\selenium\ChromeProfile"'
        # subprocess.run(cmd)
        # p = subprocess.Popen(cmd)  # 创建一个子进程执行ls -l命令
        # time.sleep(3)
        # s = discardOperate.Solution()
        # s.get_title()
        s = discardOperate.Solution("https://discord.gg/KK7bF6KAVt")
        s.set_user_name(10, "say-boy-")
        s.trigger_captcha()
        s.verify_captcha()

        # guiOperate.writeTokenToExcel()
        # 可以在这里添加一些延时或其他操作，例如：
        time.sleep(100)
except KeyboardInterrupt:
    # 当按下ctrl+c时，设置running为False并退出循环
    running = False
    print('程序已停止')
