# local_mutex

```
本地锁,通过fcntl针对文件加锁实现的. 需要强烈注意的是,多线程下是无效的,原因? [查看链接](http://xiaorui.cc)
```


## Install:

`source install`

```
python setup.py install
```

`pypi install`

```
pip install local_mutex
````

## Usage:

`最简单的例子,适合一个程序同时跑一个的场景.`

```
import sys
from local_mutex import LocalMutex

try:
    lock = LocalMutex('app.lock')
except LockError:
    sys.exit('already running')

try:
    print 'doing'
finally:
    lock.release()
```

`使用wait参数不停的试图获取Lock, 直到获取锁.`

```
lock = LocalMutex('/var/run/app.lock', wait = True)
try:
    print 'doing'
finally:
    lock.release()
```

`使用with关键词`

```
with LocalMutex('app.lock', wait = True):
    print 'doing'
```

`如果是多线程环境,直接用threading的Lock`

```
import threading
lock = threading.Lock()
with lock:
    pass
```

END
