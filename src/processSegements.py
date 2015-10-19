#!/usr/bin/env python
#eccoding=utf-8
import sys
import os


def getStopWordsList(filename):
	stop_words_file = open(filename)
	stop_words_list = []

	for line in stop_words_file:
		if line.strip():
			stop_words_list.append(line.strip())
	
	return stop_words_list


def containWords(line_str, words_list):
	size = len(words_list)
	count = 0
	for word in words_list:
		if word in line_str:
			count += 1
	
	return count==size


def getDistance(a, b):
	if len(a)!= len(b):
		print "LENGTH NOT ALLOWED"
		return

	count = 0
	for i in range(len(a)):
		count += abs(a[i]-b[i])
	
	return count


def getNewSegWords(seg_words_list, lines_str_list):
	seg_words_id_list = range(len(seg_words_list))

	new_seg_words_list = []
	for seg_word in seg_words_list:
		new_seg_words_list.append(seg_word)
#	new_seg_words_id_list = []
	distance = 0x0fffffff

	for line in lines_str_list:
		line_str = line.strip()
		new_seg_words_id_list = []

		if containWords(line_str, seg_words_list):
#			print "GET! \t",
#			print line_str
			
			for seg_word in seg_words_list:
#				print seg_word,
				new_seg_words_id_list.append(line_str.find(seg_word))
#			print 
#			print new_seg_words_id_list, 
#			print "------",
			tmp_list = sorted(new_seg_words_id_list)
			new_seg_words_id_list = [tmp_list.index(x) for x in new_seg_words_id_list]
			
#			print new_seg_words_id_list,
#			print seg_words_id_list

			new_distance = getDistance(seg_words_id_list, new_seg_words_id_list)
#			print new_distance
			if new_distance < distance:
				distance = new_distance
				for t in range(len(seg_words_list)):
					new_seg_words_list[new_seg_words_id_list[t]] = seg_words_list[t]
				
	return new_seg_words_list



def getNewSegment(new_seg_words_list, raw_seg_words):
	new_segment_list = []
	j = 0
	for i in range(len(raw_seg_words)):
		if raw_seg_words[i] not in new_seg_words_list:
			new_segment_list.append(raw_seg_words[i].strip())
		else:
			new_segment_list.append(new_seg_words_list[j].strip())
			j += 1

	return new_segment_list	



def processSegments(moses_file, dir_name, stop_words_file, start=1, end=1001):
	fw = open("newSentence.txt", 'w')
	line_str_list = open(moses_file).readlines()
	stop_words = getStopWordsList(stop_words_file)
	os.chdir(dir_name)
#	print os.getcwd()
	seg_count = 0
	size = 0
	change = 0

	for x in range(start, end):
		dir_str = "sentence_"+str(x)
		if not os.path.exists(dir_str):
			continue
		print dir_str
		os.chdir(dir_str)

		raw_segs = line_str_list[x-1].split('，')

		for i in range(len(raw_segs)):
			raw_seg_words = raw_segs[i].split(' ')
			raw_seg_words_list = []
			for seg_word in raw_seg_words:
				if seg_word.strip():
					print seg_word.strip(), 
					
					raw_seg_words_list.append(seg_word.strip())
			print 
			seg_words_list = []
			print "OLD SEG WORDS:", 
			for seg_word in raw_seg_words_list:
				if (seg_word in stop_words) or (not seg_word.strip()):
					continue
				print seg_word,
				seg_words_list.append(seg_word)
			print

			next_dir_str = "segment_"+str(i+1)
			if (not os.path.exists(next_dir_str)) or (not raw_seg_words_list):
				continue	
			os.chdir(next_dir_str)
#			print os.getcwd()

			try:
				fr = open("extract.all")
			except:
				os.chdir('..')
				continue

			lines_str_list = fr.readlines()
######
			new_seg_words_list = getNewSegWords(seg_words_list, lines_str_list)
			new_segment = raw_seg_words
			size += 1
			if not(new_seg_words_list==seg_words_list):
				change += 1
				new_segment = getNewSegment(new_seg_words_list, raw_seg_words)
				print "CHANGEED!!!"
			
			print "NEW SEG WORDS:", 
			for seg_words in new_seg_words_list:
				print seg_words, 
			print
			print " ".join(new_segment)
			print 
			fw.write((' '.join(new_segment)).strip())
			if i != len(raw_segs):
				fw.write(str(i))
#				fw.write('，')
				fw.write('，')

######
#			count = 0
#			new_seg_words_list = seg_words_list[]
#			new_segment = raw_segs[i]
#			for line in fr:
#				if containWords(line, seg_words_list):
#					count += 1
#					print line
#			print count
#			if count:
#				seg_count += 1
			fr.close()

			os.chdir('..')
#			print os.getcwd()
		os.chdir('..')
#		print os.getcwd()
		print "--------------------------------"
		fw.write('。\n')
#	print '\n\n\ncount:',	
#	print seg_count
#	print "rate:",
#	print seg_count*1.0/(end-start)
	print size
	print change
	print change*1.0/size
		


if __name__ == '__main__':
#	moses file, work dir, stop words file
	processSegments(sys.argv[1], sys.argv[2], sys.argv[3])
