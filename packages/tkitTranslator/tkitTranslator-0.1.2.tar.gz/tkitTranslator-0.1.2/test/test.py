
#encoding=utf-8
from __future__ import unicode_literals
import sys
# 切换到上级目录
sys.path.append("../")
# 引入本地库
import tkitTranslator
Demo =src.Translator()

while True:
	text=input("输入文本（自动中英）：")
	print(Demo.render(text))

