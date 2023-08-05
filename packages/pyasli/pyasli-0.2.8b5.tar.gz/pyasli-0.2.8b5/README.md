## Pyasli
[![codecov](https://codecov.io/gh/outcatcher/pyasli/branch/master/graph/badge.svg?token=SH2I5ZB221)](https://codecov.io/gh/outcatcher/pyasli)
[![Build Status](https://travis-ci.org/outcatcher/pyasli.svg?branch=master)](https://travis-ci.org/outcatcher/pyasli)
[![PyPI version](https://img.shields.io/pypi/v/pyasli.svg)](https://pypi.org/project/pyasli/)

### Simple selenium python wrapper

#### There are two ways to use browser:

##### Use default shared driver:

```python
from pyasli.browsers import browser

browser.base_url = "https://the-internet.herokuapp.com"
browser.open("/disappearing_elements")
element1 = browser.element("div.example p")
assert element1.get_actual() is element1.get_actual(), "Element is found 2 times"
```

##### Use exact driver (can be used as context manager):
```python
from tests.conftest import browser_instance

with browser_instance(base_url="https://the-internet.herokuapp.com") as browser:
    browser.open("/disappearing_elements")
    element1 = browser.element("div.example p")
    assert element1.get_actual() is element1.get_actual(), "Element is found 2 times"
```

In case `browser_instance` is used as context manager, all browser windows will be closed at
exiting context

----

##### There is no documentation currently. For usage please refer to tests

----

Built wheels are available at https://pypi.outcatcher.com/simple/pyasli/

_<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" 			    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" 			    title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>_
