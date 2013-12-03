from wgety.wgety import Wgety

try:
    w = Wgety()
    w.execute(url='http://www.python.org', filename='python.html', absolute_link=True);
    w.execute(url='http://www.python.org/images/python-logo.gif');
    exit(1)

except:
    exit(0)
