from selenium import webdriver
from bs4 import BeautifulSoup
import time
import os
import csv
import re
from sys import argv
def my_proxy(PROXY_HOST,PROXY_PORT):
	fp = webdriver.FirefoxProfile()
	# Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
	print PROXY_PORT
	print PROXY_HOST
	fp.set_preference("network.proxy.type", 1)
	fp.set_preference("network.proxy.http",PROXY_HOST)
	fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
	fp.set_preference("network.proxy.ssl",PROXY_HOST)
	fp.set_preference("network.proxy.ssl_port",int(PROXY_PORT))
	fp.set_preference("network.proxy.ftp",PROXY_HOST)
	fp.set_preference("network.proxy.ftp_port",int(PROXY_PORT))
	fp.set_preference("general.useragent.override","whater_useragent")
	fp.update_preferences()
	return webdriver.Firefox(firefox_profile=fp)



def crawl_link_till_end(url):
	browser = webdriver.PhantomJS()
	browser.get(url)
	src_updated = browser.page_source
	src = ""
	lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	match=False
	while(match==False):
		lastCount = lenOfPage
		time.sleep(3)
		lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		if lastCount==lenOfPage:
			match=True
	html_source = browser.page_source
	browser.quit()
	return html_source

def firefox_logged_in(url):
	browser = my_proxy("10.3.100.207",8080)
	
	print "Enter the login credentials"
	x = input()
	browser.get(url)
	src_updated = browser.page_source
	src = ""
	lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	match=False
	while(match==False):
		lastCount = lenOfPage
		time.sleep(3)
		lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		if lastCount==lenOfPage:
			match=True

	html_source = browser.page_source
	browser.quit()
	with open(url+".txt",'w') as f:
		f.write(html_source.encode('utf-8'))

	return html_source



def find_all_question_links_from_html(html_source,user_name,url):
	bs = BeautifulSoup(html_source)
	file_question_urls = open("questions_url"+user_name+".txt","w")
	question_divs = bs.find_all("div",class_='QuestionText')
	count=0
	while(len(question_divs)<=0) and count<5:
		time.sleep(1)
		html_source = crawl_link_till_end(url)
		bs = BeautifulSoup(html_source)
		question_divs = bs.find_all("div",class_='QuestionText')
		print "still trying to find question for "+url
		count = count+1
	if count==5:
		return []
	print question_divs
	url = []
	for question_div in question_divs:
		link_url = "http://www.quora.com" + question_div.a['href']
		print link_url+'\n'
		url.append(link_url)
		file_question_urls.write((link_url+'\n').encode('utf-8'))
	return url

def find_answer_for_user_question_link(url,user_name):
	html_source = crawl_link_till_end(url+"/answer"+"/"+user_name)
	bs = BeautifulSoup(html_source)
	# question_divs = bs.find_all("div",id=re.compile("answer_content"))
	question_divs = bs.find_all("div",class_="Answer AnswerStandalone AnswerBase")
	count = 0
	while len(question_divs)<=0 and count<5:
		time.sleep(1)
		html_source = crawl_link_till_end(url+"/answer"+"/"+user_name)
		bs = BeautifulSoup(html_source)
		question_divs = bs.find_all("div",class_="Answer AnswerStandalone AnswerBase")
		print len(question_divs)
		print "retrying for "+url+"/answer"+"/"+user_name
		count = count+1

	if(count==5):
		return ""
	answer_text = question_divs[0].text

	if(len(bs.find_all("div",class_="AnswerHeader ContentHeader"))>0):
		header_text = bs.find_all("div",class_="AnswerHeader ContentHeader")[0].text
		answer = answer_text.split(header_text)[1]
	else:
		answer = answer_text

	split_text = ""
	if(len(bs.find_all("div",class_="ContentFooter AnswerFooter"))>0):
		split_text  = bs.find_all("div",class_="ContentFooter AnswerFooter")[0].text
		answer = answer.split(split_text)[0]

	# answer_string=""
	# for i in range(0,len(answer)-1):
	# 	answer_string=answer_string+answer[i]
	return answer


if __name__ == '__main__':
	user_file = open("user_name.txt",'r')
	lines = user_file.read().splitlines()
	for url in lines:
		user_name = url.split('/')[-1]
		print user_name
		user_url = "http://www.quora.com/profile/"+user_name+"/answers"
		print user_url
		html_source = firefox_logged_in(user_url)
		questionlist = find_all_question_links_from_html(html_source,user_name,user_url)
		count = 1
		skip = int(argv[1])
		i = 0
		for question_url in questionlist:
			if(i<skip):
				i = i+1
				continue
			answer = find_answer_for_user_question_link(question_url,user_name)
			print answer
			with open("quora_user_answer.csv","a") as f:
				a = csv.writer(f, delimiter=',')
				a.writerow([user_name,answer.encode('utf-8)').strip()])
			count=count+1


	# src_updated = browser.page_source
	# # print BeautifulSoup(src_updated).encode('utf-8').strip()
	# src = ""
	# while src != src_updated:
	# 		time.sleep(.5)
	# 		src = src_updated
	# 		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# 		src_updated = browser.page_source
	# # for i in range(0,5):
	# # 	time.sleep(.5)
	# # 	src = src_updated
	# # 	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	# # 	src_updated = browser.page_source
	# # 	# print BeautifulSoup(src_updated).encode('utf-8').strip()
	# # 	# print "\n\n\n\n"

	# html_source = browser.page_source
	# # print BeautifulSoup(html_source).encode('utf-8').strip()
	# bs = BeautifulSoup(html_source)
	# file_question_urls = open("questions_url.txt","w")


	# print "\n\n*****************END OF BROWSER*****************\n\n"
	# browser.quit()
	# # bs.find_all(attrs={'class':'question_link'})
	# question_divs = bs.find_all("div",class_='QuestionText')
	# for question_div in question_divs:
	# 	link_url = "http://www.quora.com" + question_div.a['href']
	# 	print link_url+'\n'
	# 	file_question_urls.write((link_url+'\n').encode('utf-8'))

	# split_html = html_source.split("<h3>")
	# file_question_urls = open("questions_url.txt","w")
	# for i in range(1,len(split_html)):
	# 	part = split_html[i].split('</h3>')[0]
	# 	part_soup = BeautifulSoup(part)
	# 	if ("<div") in part:
	# 		#print part_soup.get_text()
	# 		for link in part_soup.find_all('a' , href=True):
	# 			link_url = "http://www.quora.com" + link['href'] + "?share=1"
	# 			print link_url
	# 			file_question_urls.write((link_url+'\n').encode('utf-8'))
	# 			total += 1
	# 	print html_source.encode('utf-8').strip()
	# browser.quit()