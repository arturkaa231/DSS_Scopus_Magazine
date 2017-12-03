from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django.template.context_processors import csrf
import json
from bs4 import BeautifulSoup
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from DSS.forms import ReqForm,FileForm
import pprint
import re, sys
import urllib.request
from urllib import request
from urllib.parse import quote
import html2text
import xlrd
import random
from langdetect import detect
import re, sys
# Create your views here.
def get_clickhouse_data(query,host,connection_timeout=1500):
		r=requests.post(host,params={'query':query},timeout=connection_timeout)
		return r.text
@csrf_exempt
def download_file(request):
	def handle_uploaded_file(f):
		with open('/home/artur/venv/clickhouseAPI/DSS/test.xlsx', 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
		rb = xlrd.open_workbook('/home/artur/venv/clickhouseAPI/DSS/test.xlsx')
		sheet = rb.sheet_by_index(0)
		query="INSERT INTO DSSDB.Mag VALUES "

		for rownum in range(1,sheet.nrows):
			row = sheet.row_values(rownum)
			q=[]
			theme=''
			for c_el in range(15):
				if c_el>9:
					if row[c_el] == "":
						continue
					else:
						theme=theme+' '+row[c_el].lower()
						continue
				else:	
					if c_el == 4:
						year = random.randrange(1996, 2016)
						month = random.randrange(1, 12)
						day = random.randrange(1, 30)
						if day<10:
							day='0'+str(day)
						if month<10:
							month='0'+str(month)
						date = str(year) + "-" + str(month) + "-" + str(day)
						q.append("'" + date + "'")
						continue
		
		
		
					elif row[c_el]=="" :
						q.append("'none'")
						continue
					else:
			 			q.append("'"+str(row[c_el]).lower()+"'")
			if theme=='':
				continue
			q.append("'"+theme+"'")
			#добавляем ссылку на журнал
			print("'"+q[1]+q[6]+"'")
	
			req=query+"("+','.join(q)+")"
			get_clickhouse_data(req,'http://127.0.0.1:8123')
	handle_uploaded_file(request.FILES['Exc'])
	
	args={}
	args.update(csrf(request))
	args['form']=ReqForm
	args['file_form']=FileForm
	return render_to_response('magazine.html',args)
@csrf_exempt
def main(request):
	
	def mail_search(query):
		#opener = urllib.request.build_opener()
		#opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		#doc=opener.open('http://go.mail.ru/search?fm=1&q='+quote(query)).read().decode('cp1251',errors='ignore')
		
		url ='http://www.google.com/search?q='
		page = requests.get(url + query)
		soup = BeautifulSoup(page.text)
		h3 = soup.find_all("h3",class_="r")
		l=[]
		for elem in h3:
			elem=elem.contents[0]
			link=("https://www.google.com" + elem["href"])
			l.append(link)
		
		#s = requests.Session()
		#s.proxies = {"http": "http://82.137.250.78:55555"}
		#r = s.get('http://go.mail.ru/search?fm=1&q='+quote(query))
		
		#doc = urllib.request.urlopen('http://go.mail.ru/search?fm=1&q='+quote(query)).read().decode('cp1251',errors='ignore')
		#print(r.text)
		# В список sp получим все ссылки на результаты поиска из этой страницы
		#print('http://go.mail.ru/search?fm=1&q='+quote(query))
		#o=re.compile('"url":"(.*?)"')
		#l=o.findall(doc)
		#print(l)
		#sp=[]
		#for x in l:
			#if((x.rfind('youtube')==-1) and(x.rfind('yandex')==-1) and(x.rfind('mail.ru')==-1) and(x.rfind('.jpg')==-1) and(x.rfind('.png')==-1) and(x.rfind('.gif')==-1)):
				#sp.append(x)
		#print(sp)
		return l[0]
	
	if request.method=='POST':
		
		where=[]
		id=request.POST.get('id')
		if id!="":
			where.append('id ='+"'"+id+"'")
		title=request.POST.get('title')
		if title!="":
			where.append('title LIKE'+"'%"+title+"%'")
		ISSN=request.POST.get('ISSN')
		if ISSN!="":
			where.append('ISSN='+"'"+ISSN+"'")
		E_ISSN=request.POST.get('E_ISSN')
		if E_ISSN!="":
			where.append('E_ISSN='+"'"+E_ISSN+"'")

		date1=request.POST.get('date1')
		date2=request.POST.get('date2')
		if date1!="" and date2!="":
			where.append("date BETWEEN '%s' AND '%s'"%(date1,date2))
		source_type=request.POST.get('source_type')
		if source_type!="":
			where.append('source_type='+"'"+source_type+"'")	
		publisher=request.POST.get('publisher')
		if publisher!="":
			where.append('publisher='+"'"+publisher+"'")
		country=request.POST.get('country')
		if country!="":
			where.append('country='+"'"+country+"'")
		ASJS=request.POST.get('ASJS')
		if ASJS!="":
			where.append('ASJS LIKE'+"'%"+ASJS+"%'")
		language=request.POST.get('language')
		if language!="":
			where.append('language='+"'"+language+"'")
		Theme=request.POST.get('Theme')
		if Theme!="":
			where.append('Theme LIKE'+"'%"+Theme+"%'")
		where=' AND '.join(where)
		#print(where)
		q=''' SELECT title,'Издательство:', publisher FROM DSSDB.Mag WHERE {where} ORDER BY id FORMAT JSON'''.format(where=where)
		journals=[]
		links=[]
		resp=json.loads(get_clickhouse_data(q,'http://127.0.0.1:8123'))['data']
		
		if resp==[]:
			journals.append('К сожалению, совпадений не найдено')
		
		k=0
		for i in resp:
			
			journals.append(i['title'])
			#print(i['title']+' '+i['publisher'])
			#if k==0:
				#try:
					#links.append(mail_search(i['title']+' '+i['publisher']))
				#except:
					#links.append('#')
					#k=1
			#else:
				#links.append('#')
			
			#print(mail_search(resp[i]))
			
			links.append(mail_search(i['title']+' '+i['publisher']))
		r=[journals,links]
			
		
		
		#resp='\n'.join(resp)
		
		
		return JsonResponse(r,safe=False)
	else:
		args={}
		args.update(csrf(request))
		args['form']=ReqForm
		args['file_form']=FileForm

		return render_to_response('magazine.html',args)
