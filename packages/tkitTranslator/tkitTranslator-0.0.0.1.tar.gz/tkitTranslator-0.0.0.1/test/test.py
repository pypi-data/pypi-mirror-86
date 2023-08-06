
#encoding=utf-8
from __future__ import unicode_literals
import sys
# 切换到上级目录
sys.path.append("../")
# 引入本地库
import src
text="""The effect of such changes is unpredictable. If you want to break a for loop before its normal termination, use break."""
Demo =src.Translator()
print(Demo.render(text))

