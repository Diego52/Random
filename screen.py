from screeninfo import get_monitors
for m in get_monitors():
    print(m.height,m.width)