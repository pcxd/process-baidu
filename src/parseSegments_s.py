#!/usr/bin/env python
#encoding=utf-8
import sys
import urllib2
import requests
import os
from bs4 import BeautifulSoup
import time
import socket
import jieba
import StringIO
from time import clock

reload(sys)
sys.setdefaultencoding('utf8')

socket.setdefaulttimeout(10)


def getStopWordsList(filename):
	stop_words_file = open(filename)
	stop_words_list = []

	for line in stop_words_file:
		stop_words_list.append(line.strip())
	
	return stop_words_list



########       PARSE SERACH PAGE      #################################################
def parseSearchPage(searchURL):
#	fw1 = open("tmp/searchResult.html", 'w')
#	fw2 = open("tmp/searchResult.format", 'w')
#	fw3 = open("tmp/searchResult.extract", 'w')

#	orgHtml = StringIO.StringIO()
	formatHtml = StringIO.StringIO()
	extractHtml = StringIO.StringIO()
	
	try:
		response = urllib2.urlopen(searchURL)
		time.sleep(1)
	except:
		return [], ""
	else:
		try:
			pageContent = response.read()
		except:
			return [], ""
	response.close()

	soup = BeautifulSoup(pageContent)
#	fw2.write(soup.prettify())
	formatHtml.write(soup.prettify())
	
#	get next search page's URL
	mdiv = ""
	for div in soup.find_all('div'):
		if(div.get('id') == 'page'):
			mdiv = div
	if(cmp(mdiv, "") == 0):
		return [], ""
	
	try:
		nextPage = mdiv.find_all('a')[-1].get('href')
	except:
		nextPage = ""
	else:
		nextPage = "http://www.baidu.com"+nextPage
	
#	get ten search link from h3 and a tag
#	fr1 = open("tmp/searchResult.format")
	formatHtml.seek(0)
	flag = False
#	for line in fr1.readlines():
	for line in formatHtml.readlines():
		if("<h3" in line):
			flag = True
		if(flag):
#			fw3.write(line)
			extractHtml.write(line)
		if("</h3>" in line):
			flag = False
#	fw3.close()

#	fr2 = open("tmp/searchResult.extract")
#	infoContent = fr2.read()
	extractHtml.seek(0)
	infoContent = extractHtml.read()	
	mSoup = BeautifulSoup(infoContent)
	retList = []
	
	for link in mSoup.find_all('a'):
		retList.append(link.get('href'))

#	return ten linkURL and next page's URL	
#	fw1.close()
#	fw2.close()
#	fr1.close()
#	fr2.close()
	formatHtml.close()
	extractHtml.close()

	return retList, nextPage


#	parse search page and get page content    ########################################
def parseResultPage(resultLink):
	try:
		response = urllib2.urlopen(resultLink)
		time.sleep(1)
	except:
		return ""
	else:
		try:
			pageContent = response.read()
		except:
			return ""
	response.close()
	
	try:
		soup = BeautifulSoup(pageContent)	
	except:
		return ""

	return soup.get_text()

########################################################################################


#	format search string ##############################################################
def getSearchString(sentence, stop_words_list):
#	print len(stop_words_list), '~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
#	print
#	for t in stop_words_list:
#		print t, '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4'
#		print
#	segs = jieba.cut_for_search(sentence)
	segs = sentence.split(' ')
	retStr = ""
	stringSegList = []

	for seg in segs:
		seg = seg.strip()
		if (not seg) or seg in stop_words_list:
			continue
		
		retStr = retStr + "\"" + seg+ "\"%2B"
		stringSegList.append(seg)
	
	return retStr[0:-3], stringSegList

#######################################################################################



#	sentence contains all seg words?###################################################
def inSentence70(segList, sentence):
	size = len(segList)
	count = 0
#	for t in segList:
#		print t, '###'
	for i in range(len(segList)):
		count += int(segList[i] in sentence)
#		if(not(segList[i] in sentence)):
#			flag = False
#			break
	if count*1.0/size > 0.4: flag = 1
	else: flag = 0

	return flag

#	search page and return sentence if exists!!######################################
def searchPage(pageContent, segList):
	lines = pageContent.split('\n')
	retSentence = ""
	flag = False

	for line in lines:
		line = line.strip()
		if(cmp(line, "") == 0):
			continue

		flag = False
		retSentence = ""
		lineSentences = line.split('。')
		for lineSentence in lineSentences:
			tflag = inSentence70(segList, lineSentence)
			if(tflag):
				flag = True
				retSentence = lineSentence
				break

		if(flag):
			break

	return flag, retSentence

#######################################################################################


#	improve translation according search page	######################################
def process(originalFileName, stop_words_list):
	fr = open(originalFileName)
#	fw = open("result100.txt", 'w')
#	ttttt = 0
	os.chdir("download")
	if not os.path.exists("segments_s"):
		os.mkdir("segments_s")
	os.chdir("segments_s")
	sentence_id = 1
	
	for line in fr.readlines():
		rawStr = line.strip()[0:-1]
		segments = rawStr.split("，")
		seg_length = len(segments)

		if not os.path.exists("sentence_"+str(sentence_id)):
			os.mkdir("sentence_"+str(sentence_id))
		os.chdir("sentence_"+str(sentence_id))

		for i in range(seg_length):
			if not os.path.exists("segment_"+str(i+1)):
				os.mkdir("segment_"+str(i+1))
			os.chdir("segment_"+str(i+1))
		
#		fw.write(rawStr+'\n'+"NOT EXSIST IN PAGE: ")
			searchStr, strSegList = getSearchString(segments[i], stop_words_list)
			print searchStr
#		ttttt += 1
			print "------------------------%d-------------------------" %(sentence_id)
			nextSearchURL = "http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=SE_hldp04290_mt35whgs&wd="+searchStr+"&rsv_t=393aMJYfVWscbB4FQ59IV4dKAiRkGpDxhkZsaNS%2FGozzGj9fJCkZxnb2fYcVPHqvllwQxHCd8ekH%2B0Ux&rsv_enter=1&rsv_sug3=6&rsv_sug1=4"
#		print "--nextSearchURL: %s" %(nextSearchURL)
		
#		if not os.path.exists("sentence_"+str(sentence_id)):
#			os.mkdir("sentence_"+str(sentence_id))
#		os.chdir("sentence_"+str(sentence_id))
#		flag = False
			page_count = 0
#		while(flag == False):
			search_page_id = 1
			while(True):
				searchURLList, nextSearchURL = parseSearchPage(nextSearchURL)
#			fw = open(str(search_page_id)+'.txt', 'w')
				for i in range(len(searchURLList)):
					fw = open(str(search_page_id)+'.txt', 'w')
#				print searchURLList[i]
					pageContent = parseResultPage(searchURLList[i])
					if not pageContent:
						continue
					else:
						fw.write(pageContent)
						search_page_id += 1
				
#				tFlag, sentence = searchPage(pageContent, strSegList)
#				if(tFlag):
#					flag = True
#					fw.write('\n'+sentence+'\n\n')
#					break
#				else:
#					fw.write("%d" %(count*10+i+1))
#					print(count*10+i+1)
#					print "***********"
#					fw.write(" ")
				if not nextSearchURL:
					print "NO MORE PAGE!!!"
					break
			
				page_count += 1
				if(page_count == 5):
					break
			os.chdir("..")

		sentence_id += 1
		os.chdir("..")
#		fw.write('\n')
#	return
#########################################################################################

if __name__ == "__main__":
	stop_words_list = getStopWordsList(sys.argv[1])
#	for i in range(len(stop_words_list)):
#		print stop_words_list[i]
#	print len(stop_words_list)
	process(sys.argv[2], stop_words_list)	

