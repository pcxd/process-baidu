#!/usr/bin/env python
#encoding=utf-8
import sys
import os

def splitStr(line_str):
	split_str = '||||||'
	line_str = line_str.replace(',',split_str).replace('，', split_str).replace('。', split_str).replace('！', split_str).replace('？', split_str).replace('；', split_str)
	
	tmp_ret = line_str.strip().split(split_str)
	ret_list = []

	for t in tmp_ret:
		if t.strip():
			ret_list.append(t.strip())
	
	return ret_list


def getStopWordList(filename):
	stop_word_file = open(filename)
	stop_word_list = []

	for line in stop_word_file:
		stop_word_list.append(line.strip())

	return stop_word_list


def containWords(seg_str, words_list, rate = 0.2):
	size = len(words_list)
	count = 0
	for word in words_list:
		if word in seg_str:
			count += 1
#			print word, "+++ ", seg_str
	real_rate = count*1.0/size

	return real_rate>rate and count>1


def preExtract(moses_file, dir_name, stop_word_file, start=1, end=1001):
	line_str_list = open(moses_file).readlines()
	stop_words = getStopWordList(stop_word_file)
#	for word in stop_words:
#		print word

	os.chdir(dir_name)
	print os.getcwd()

	for i in range(start, end):
		dir_str = "sentence_"+str(i)

		print line_str_list[i-1]
		raw_segs = line_str_list[i-1].split('，')
		for raw_seg in raw_segs:
			print raw_seg
		print "------------"

		if not os.path.exists(dir_str):	
			continue

		next_dir_list = os.listdir(dir_str)
		os.chdir(dir_str)
		print os.getcwd()

		for n_dir in next_dir_list:
			if not os.path.isdir(n_dir):
				continue
			
			file_name_list = os.listdir(n_dir)
			if not file_name_list:
				continue
			os.chdir(n_dir)
			print os.getcwd()
			print n_dir
			seg_id = int(n_dir.split('_')[-1])
#			print seg_id
			print "------------"

			raw_seg_words = raw_segs[seg_id-1].split(' ')
			raw_seg_words_list = []
			for seg_word in raw_seg_words:
				if seg_word.strip():
					raw_seg_words_list.append(seg_word.strip())
			if not raw_seg_words_list:
				continue

			seg_words_list = []
#			print len(raw_seg_words_list)
			for seg_word in raw_seg_words_list:
				print seg_word,
				if (seg_word in stop_words) or (not seg_word.strip()):
					continue
				seg_words_list.append(seg_word)
			print
			print "----------------------------------"
#			print len(seg_words_list)
			for seg_word in seg_words_list:
				print seg_word,
			print
			print "----------------------------------"
			print len(file_name_list)

			fw = open("extract.all", 'w')
			for file_name in file_name_list:
				if file_name=="extract.all":
					continue
				fr = open(file_name)
				print file_name, 
				for line in fr:
					line = line.strip()
					if not line:
						continue
					line_segs = splitStr(line)
					for seg_str in line_segs:
						if containWords(seg_str, seg_words_list):
							fw.write(seg_str+'\n')
#							print seg_str
				fr.close()
			fw.close()
			print "\n\n"
			os.chdir('..')
			print os.getcwd()
		os.chdir('..')
		print os.getcwd()


if __name__ == "__main__":
#	raw translation file, diractory of download file, stop word list file
	preExtract(sys.argv[1], sys.argv[2], sys.argv[3])
