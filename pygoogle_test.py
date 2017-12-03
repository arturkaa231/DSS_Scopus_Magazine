import re, sys
import urllib.request
from urllib import request
from urllib.parse import quote
import html2text

# Введем поисковый запрос и получим в переменную doc страницу с поисковой выдачей от mail.ru

print("\n---------\n")
z=input("Введите ваш вопрос: ")
print("\n---------\n")
s = 'http://go.mail.ru/search?fm=1&q='+quote(z)
doc = urllib.request.urlopen(s).read().decode('cp1251',errors='ignore')

# В список sp получим все ссылки на результаты поиска из этой страницы

o=re.compile('"url":"(.*?)"')
l=o.findall(doc)
sp=[]
for x in l:
	if((x.rfind('youtube')==-1) and(x.rfind('yandex')==-1) and(x.rfind('mail.ru')==-1) and(x.rfind('.jpg')==-1) and(x.rfind('.png')==-1) and(x.rfind('.gif')==-1)):
		sp.append(x)
print(sp)
