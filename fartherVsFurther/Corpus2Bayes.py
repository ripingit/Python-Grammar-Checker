
'''                                                                                                                 
Farther vs Further
Fri Dec 18 11:07:54 AEDT 2015

A simple grammar checker for this single rule. 
'''
#import nltk
from textblob import TextBlob
import csv 
from Sentence import Sentence

#TODO get rid of lower cases
#TODO add more features.

class WordMangle(object):
	"""Sun Dec 20 07:43:55 AEDT 2015"""
#Created a better way to find tags before and after a key.
#This new method is scalable because it can accept any number of surrounding features.
#TODO I could develop this method to collect other features like word frequencies.

	def __init__(self):
		#self.mangle = MangleData()
		pass

	def tagSentence(self, sentence):
		"""Turn a sentence into an array of (words, tags)"""
		return TextBlob(sentence).tags

	def loadCSV(self, fileName="fartherVsFurther.csv"):
		"""Load training set"""
		f = open(fileName, "rb")
		reader = csv.reader(f)
		newData = []
		for line in reader:
			newData += [line]
		f.close()
		return newData


	def addTags(self, sentence=[("further", "JJ"), ("Elephant", "NNP")], factors=5):	
		""""
		Buffer a list of (word, tag) with NAs of any factor
		[(x1,y1), (x2,y2)], 1 ----> [(na,na), (x1,y1), (x2,y2), (na,na)]
		"""
		newVars = []
		for i in range(factors):
			newVars.append(("na", "na"))
		sentence += newVars
		newVars += sentence
		return newVars

	def extractTags(self, sentence=[("NA","NA"),("run","VB"),("further", "JJ"), ("Elephant", "NNP"),("Hotel","NNP"),("NA","NA")], keys=["further", "farther"], factors=2):
		"""Get tags that surround a key """
		count = 0
		listOfTags = []
		for i in sentence:
			# Wait till you find one of the keys
			if i[0] in keys:
				iterNum = 0
				#Get words before key
				for z in range(factors):

					listOfTags.append(sentence[(count - factors) + iterNum][1])
					iterNum += 1
				iterNum = 1
				#Get words after key
				for z in range(factors):

					listOfTags.append(sentence[count + iterNum][1])
					iterNum += 1
				return listOfTags	
			count += 1
		return listOfTags

	def processWords(self, sentence="I can not take it much farther.", keys=["further", "farther"], factors=5):
		"""Turns a sentence into a list of words with buffer of N factors"""
		#Tag sentence
		X = self.tagSentence(sentence)
		#Add NAs to front and back
		X = self.addTags(X, factors)
		#Reduce to a list of tags
		return self.extractTags(X, keys, factors)
	
	def addTags4Words(self, sentence=["here", "is", "a", "word"], factors=5):	
		""""
		Buffer a list of (word, tag) with NAs of any factor
		[(x1,y1), (x2,y2)], 1 ----> [(na,na), (x1,y1), (x2,y2), (na,na)]
		"""
		newVars = []
		for i in range(factors):
			newVars += ["na"]
		sentence += newVars
		newVars += sentence
		return newVars

	def extractTags4Words(self, sentence, keys, factors):
		"""
		Return the words around a key
		["na", "I", "run", "na"], "run", 1 -----> ["I", "run", "na"]
		"""
		listOfTags = []
		count = 0
		for i in sentence:
			if i in keys:
				iterNum = 0
				#Get words before key
				for z in range(factors):
					listOfTags += [sentence[(count - factors) + iterNum]]
					iterNum += 1
				iterNum = 1
				for z in range(factors):
					listOfTags += [sentence[count + iterNum]]
					iterNum += 1
				return listOfTags
			count += 1
		return listOfTags

	def processWords4Words(self, sentence="I can not take it much farther.", keys=["further", "farther"], factors=5):
		"""Turns a sentence into a list of words with buffer of N factors"""
		#Tag sentence
		X = sentence.lower().split(" ")
		X = [x[0] for x in self.tagSentence(sentence)]
		#Add NAs to front and back
		X = self.addTags4Words(X, factors)
		#Reduce to a list of tags
		return self.extractTags4Words(X, keys, factors)

class CheckGrammar(object):
	"""
	Calculate Naive Bayes on any sample provided.
	This class reads Bayes data and calculates the algorithm based on this data.
	"""
	def __init__(self):
		self.mangle = WordMangle()

	def quickLoop(self, fileName, keys, factors):
		while (True):
			x = raw_input(">> ")
			self.testSentence(x, fileName, keys, factors)

	def testSentence(self, sentence="You could not be further from the truth.", fileName="finalFurther.csv", keys = ["further", "farther"], factors = 2, class1=3192.0, class2=1078.0):
		sentence = sentence.lower()
		# Get the tag list of surrounding words
		X = self.mangle.processWords(sentence, keys, factors)
		print sentence, X

		# Load dataset with probabilities
		Y = self.mangle.loadCSV(fileName)

		# Calculate class probabilities
		trueCond = class1 / (class1 + class2)
		falseCond = class2 / (class1 + class2)

		# Loop over tags
		count = 1
		for z in X:
			# Find tag in dataset
			for i in Y:
				if z == i[0]:
					print float(i[count]), float(i[count+1])
					trueCond *= float(i[count])
					falseCond *= float(i[count+1])
			count += 2
		print "class_1 " + keys[0] + " " + str(trueCond / (trueCond + falseCond))
		print "class_2 " + keys[1] + " " + str(falseCond / (trueCond + falseCond))

class ComputeBayes(object):
	"""
	Create a CSV spreadsheet of all the Bayes data.
	"""
	#TODO create a dict of dicts to allow for more features to be dynamically added.
	def __init__(self):
		# load MangleData class
		self.feature1 = {"CC": 1.0, "CD": 1.0, "na": 1.0, "DT": 1.0, "EX": 1.0, "FW": 1.0, "IN": 1.0, "JJ": 1.0, "JJR": 1.0, "JJS": 1.0, "LS": 1.0, "MD": 1.0, "NN": 1.0, "NNP": 1.0, "NNPS": 1.0, "NNS": 1.0, "PDT": 1.0, "POS": 1.0, "PRP": 1.0, "PRP$": 1.0, "RB": 1.0, "RBR": 1.0, "RBS": 1.0, "RP": 1.0, "SYM": 1.0, "TO": 1.0, "UH": 1.0, "VB": 1.0, "VBD": 1.0, "VBG": 1.0, "VBN": 1.0, "VBP": 1.0, "VBZ": 1.0, "WDT": 1.0, "WP": 1.0, "WP$": 1.0, "WRB": 1.0, "total": 37.0}
		self.mangle = MangleData()
		#self.initDicts()

	def setupDicts(self, factors = 2):
		"""Setup feature dicts for any number of features """
		# Class 1 dict
		self.features = {}
		self.factors = factors
		factors *= 2
		for i in range(factors):
			self.features[i] = {k:v for k,v in self.feature1.items()}
		
		# Class 2 dict
		self.featuresClass2 = {}
		#factors *= 2
		for i in range(factors):
			self.featuresClass2[i] = {k:v for k,v in self.feature1.items()}

	def clearDict(self):
		"""Clears the one dict to rule them all."""
		self.features.clear()

	def countAllFeatures(self, fileName = "farther.csv"):
		"""Create a dict of feature counts"""
		self.class1Name = fileName
		X = self.mangle.loadCSV(fileName)
		# rows - intances
		for i in X:
			count = 0
			# columns - features
			for z in i:
				# Add count for each item according to column and row
				if count < (len(i) - 1): 
					self.features[count][z] += 1
					self.features[count]['total'] += 1
				count += 1

	def countAllFeaturesClass2(self, fileName = "further.csv"):
		"""Create a dict of feature counts"""
		self.class2Name = fileName
		X = self.mangle.loadCSV(fileName)
		# rows - intances
		for i in X:
			count = 0
			# columns - features
			for z in i:
				# Add count for each item according to column and row
				if count < (len(i) - 1): 
					self.featuresClass2[count][z] += 1
					self.featuresClass2[count]['total'] += 1
				count += 1

	def intersect(self, X, Y):
		"""
		Join two lists in an overlaping fashion 
		[x1, x2, x3], [y1, y2, y3] ----> [x1, y1, x2, y2, x3, y3]
		"""
		result = [None] * (len (X) + len(Y))
		result[::2] = X
		result[1::2] = Y
		return result

	def createSheet(self):
		"""Create spreadsheet of data for (features * tags)"""
		# Create header string
		# e.g. "tag,f1_c1,f1_c2,f2_c1,f2_c2,f3_c1,f3_c2,f4_c1,f4_c2"
		A = ["f" + str(x + 1) + "_c1" for x in range(self.factors * 2)]
		B = ["f" + str(x + 1) + "_c2" for x in range(self.factors * 2)]
		C = ','.join(["tags"] + self.intersect(A, B))
		print C

		# Calculate class totals
		class1_total = self.features[0]['total']
		class2_total = self.featuresClass2[0]['total']

		# Loop over every tag in order
		for i in self.getTagList():
			# Get list of features for each class for each tag
			X = [str(self.features[x][i] / class1_total) for x in range(self.factors * 2)]
			Y = [str(self.featuresClass2[x][i] / class2_total) for x in range(self.factors * 2)]
			Z = ','.join([i] + self.intersect(X, Y))
			print Z

		# Print totals for data
		print "class_1," + str(class1_total)
		print "class_2," + str(class2_total)

	def getTagList(self):
		#TODO Sort tags so that they're easier to view in spreadsheet
		return ['WRB', 'PRP$', 'VBG', 'FW', 'CC', 'PDT', 'RBS', 'PRP', 'CD', 'WP$', 'VBP', 'VBN', 'EX', 'JJ', 'IN', 'WP', 'VBZ', 'DT', 'MD', 'NNPS', 'RP', 'NN', 'na', 'RBR', 'VBD', 'JJS', 'JJR', 'SYM', 'VB', 'TO', 'UH', 'LS', 'RB', 'WDT', 'NNS', 'POS', 'NNP']
			
	def printOutTags(self):
		"""Make printable version of tag names"""
		for i in self.feature1:
			print "'" + i + "',",	

class MangleData(object):
	"""
	Convert a raw corpus into a dataset.
	"""  
#TODO I've created better methods to do some of these tasks in the new class called WordMangle()
  
        def __init__(self):
		# use a dictionary to store tags e.g. {"vvb": 1.0, "jj": 2}
		self.mangle = WordMangle()

	#def getListOfTags(self):
		#"""Use this to get a list of all nltk tags printed 2 screen."""
		#print nltk.help.upenn_tagset()

        def tagSentence(self, sentence):
		"""Turn a sentence into an array of (words, tags)"""
		return TextBlob(sentence).tags

	def loadCSV(self, fileName="fartherVsFurther.csv"):
		"""Load training set"""
		f = open(fileName, "rb")
		reader = csv.reader(f)
		newData = []
		for line in reader:
			newData += [line]

		f.close()
		return newData

	def trainLargeCorpus(self, fileName="sentenceExamples/furtherKindleSmall.txt", factors = 2, key = "further"):
		"""Convert a training set to an array of values."""
		X = open(fileName, 'r').read().lower().split("\n")			
		count = 0
		for i in X:
			if len(i) < 2: 
				#count += 1
				continue

			X[count] = self.mangle.processWords(i, [key], factors)
			print ','.join(X[count] + [key])
			count += 1

	def setupDicts(self, factors = 2):
		"""Setup feature dicts for any number of features """
		# Class 1 dict
		self.features = {}
		self.factors = factors
		factors *= 2
		for i in range(factors):
			self.features[i] = {}

	def trainWordCorpus(self, fileName="sentenceExamples/furtherKindleSmall.txt", factors = 2, key = "further"):
		"""Convert a training set to an array of values."""
		X = open(fileName, 'r').read().lower().split("\n")	
		newData = []		
		self.setupDicts(factors)
		count = 0
		for i in X:
			if len(i) < 2: 
				#count += 1
				continue
			X[count] = self.mangle.processWords4Words(i, [key], factors)
			newData += [X[count]]
			wordCount = 0
			for z in X[count]: 
				if z in self.features[wordCount]: 
					self.features[wordCount][z] += 1
				else: self.features[wordCount][z] = 1
				wordCount += 1
			#print ','.join(X[count] + [key])
			count += 1
		print self.features[2]
		print; print self.features[3]

def main():

	"""Step 4: Looping over examples"""
	#loopTest = CheckGrammar()
	#loopTest.quickLoop("model3/sheet.csv", ["further", "farther"], 20)

	"""Step 3: Check real life example"""
	#testModel = CheckGrammar()
	#testModel.testSentence("If you complain further, I'm going to shoot you out of the airlock.", "output/kindleSmall_sheet.csv", ["further", "farther"], 2)

	"""Step 2: Compute Bayes"""
	#TODO calculate the features dynamically to allow for any number of features.
	#computeBayes = ComputeBayes()
	#computeBayes.setupDicts(20)
	#computeBayes.countAllFeatures("model3/furthertag.txt")
	#computeBayes.countAllFeaturesClass2("model3/farthertag.txt")
	#computeBayes.createSheet()
	
	"""Step 1: Mangle Data"""
	mangleData = MangleData()
	#mangleData.trainLargeCorpus("model2/fartherKindleSmall.txt", 20, "farther")
	
	# Part B: Word Corpus
	mangleData.trainWordCorpus("model2/fartherKindleSmall.txt", 5, "farther")

	"""Step 0: Get Data"""
	#getSentences = Sentence()
	#getSentences.findSentence("farther", "/home/juke/prog/booksKindle")


if __name__ == '__main__':main()
