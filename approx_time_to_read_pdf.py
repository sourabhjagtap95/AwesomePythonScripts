#!/usr/bin/env python3
import os
import sys
import re
import time
import PyPDF2
 
def getPageCount(pdf_file):
	pdfFileObj = open(pdf_file, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pages = pdfReader.numPages
	return pages
 
def extractData(pdf_file, page):
	pdfFileObj = open(pdf_file, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pageObj = pdfReader.getPage(page)
	data = pageObj.extractText()
	return data
 
def getWordCount(data):
	data=data.split()
	return len(data)
 
def calculateSpeed():
	print (
		"""There had been some speculation on the dangers of landing
some hours before. The planetary target was a huge one for an
oxygen-water world. Though it lacked the size of the
uninhabitable hydrogen-ammonia planets and its low density
made its surface gravity fairly normal, its gravitational forces fell
off but slowly with distance. In short, its gravitational potential
was high and the ship's Calculator was a run-of-the-mill model
not designed to plot landing trajectories at that potential range.
That meant the Pilot would have to use manual controls.
		""")
	t0=time.time()
	inp=input()
	if inp=="ok":
		t1 = time.time()
		totalTime = t1-t0
	else: print("\nYou had to type \"ok\" before pressing Enter!!\n")
	speed = int(100/totalTime)	
	return speed
 
def main():
	if len(sys.argv)!=2:
		print('command usage: python know_count.py FileName')
		exit(1)
	else:
		pdfFile = sys.argv[1]
		# check if the specified file exists or not
		try:
			if os.path.exists(pdfFile):
				print("\nfile found!\n")
		except OSError as err:
			print(err.reason)
			exit(1)
		# get the word count in the pdf file
		print("Loading pdf...\n")
		totalWords = 0
		numPages = getPageCount(pdfFile)
		for i in range(numPages):
			text = extractData(pdfFile, i)
			totalWords+=getWordCount(text)
		time.sleep(1)
		#print (totalWords)
		print ("PDF loaded\n")
		print("\nType \"ok\" and press Enter after you complete reading the paragraph displayed\n")
		speed=calculateSpeed()
		seconds = totalWords/speed
		minutes, seconds = divmod(seconds, 60)
		hours, minutes = divmod(minutes, 60)
		if hours>1:
			print("You will take approximately %d hours to complete the book\n" % (hours+1))
		else:
			print("You will take approximately %d minutes to complete the book\n" % (minutes+1))
	
if __name__ == '__main__':
	main()
