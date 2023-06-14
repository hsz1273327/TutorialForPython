import signal
signal.signal(signal.SIGALRM,lambda sig,frame:print("闹钟!"))
signal.signal(signal.SIGINT,lambda sig,frame:print("ctrl+C!"))
signal.alarm(10)
print("开始等待信号")
signal.pause()
#sigset = {signal.SIGALRM}
#signal.sigwait(sigset)
print("等待结束")
