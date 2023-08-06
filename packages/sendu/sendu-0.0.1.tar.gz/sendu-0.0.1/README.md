# sendu
Serverjiang for python.

# Install
```Python
pip install sendu
```

# Getting started
You should go to [Server-Chan](http://sc.ftqq.com/3.version) get a SCKEY and bind WeChat. Your URL will be like 'https://sc.ftqq.com/[SCKEY].send '. You can use following functions to send text, picture, markdown files.
```Python
from sendu import sendu
svc = sendu.sendu(user_URL) # If you're the first time using sendu on this computer
svc = sendu.sendu() # If you're not the first time on this computer
svc.output_to_weixin("ATestMessage.")
svc.output_to_weixin_picture("http://sc.ftqq.com/static/image/bottom_logo.png")
svc.output_to_weixin_markdown("README.md")
```

# Demo

I'm the first time on this computer：
```python
from sendu import sendu
svc = sendu.sendu('https://sc.ftqq.com/{your-key}.send')
svc.output_to_weixin("ATestMessage.")
svc.output_to_weixin_picture("http://sc.ftqq.com/static/image/bottom_logo.png")
svc.output_to_weixin_markdown("README.md")
```

I'm **not** the first time on this computer：
```python
from sendu import sendu
svc = sendu.sendu()
svc.output_to_weixin("ATestMessage.")
svc.output_to_weixin_picture("http://sc.ftqq.com/static/image/bottom_logo.png")
svc.output_to_weixin_markdown("README.md")
```