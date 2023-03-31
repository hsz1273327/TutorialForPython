import mmap, time, os

with mmap.mmap(os.open("hello.txt", os.O_RDWR), 1) as m:
    last = None
    while True:
        m.resize(m.size())
        data = m.read(m.size())
        if data != last:
            print(data)
            last = data
        time.sleep(5)