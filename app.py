from flask import Flask
import scoring
import pyodbc
from spellchecker import SpellChecker
from flask import request, jsonify
server = 'vaani.database.windows.net'
database = 'vaani' 
username = 'vaanidb' 
password = 'Krn@8126421436' 
driver= '{ODBC Driver 17 for SQL Server}'

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux"


@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():

	if 'keyword' in request.args:
		keyword = request.args['keyword']
		print(keyword)
	else:
		return "Error: No keyword field provided. Please specify an keyword."

	print("#-----------------------------------------------------------#")

	print("#------------------------- TEXT SCORING --------------------#")
	# Enter keyword and paragraph
	print("#-----------------------------------------------------------#")
	#keyword = input("ENTER KEYWORDS : ")
	print("#############################################################")
	#paragraph = input("ENTER PARAGRAPH : ")
	print("#############################################################")

	paragraph = ""
	with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
		with conn.cursor() as cursor:
			cursor.execute("select Id,Question from dbo.QuestionAnswers where Language = \'eng\'")
			row = cursor.fetchone()
			while row:
				#print (str(row[0]) + " " + str(row[1]))
				paragraph = paragraph + str(row[0]) + " "+ str(row[1])+". "
				row = cursor.fetchone()



	# Initialize the textscoring instance
	print(paragraph)
	scoreTextObj = scoring.scoreText()
	# Paragraph passed will be split inot sentences,
	# Each sentence will be split and it will be compared with keyword and a score is given.
	# Top scored sentence will be displayed as results.
	spellchecked = scoreTextObj.spellcheck(keyword)
	print(spellchecked);
	matchedSentences = scoreTextObj.sentenceMatch(spellchecked,paragraph)
	print()
	print("#-------------------------- RESULTS ------------------------#")
	print("#-------------------BEST MATCHING SENTENCES-----------------#")
	print()
	#print the top scored sentences

	# try:
	count = 1
	finalString = ""
	for text in matchedSentences:
		print(' '+str(count)+' : '+text)
		if (count == 1):
			id = text[0:2]
			with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
				with conn.cursor() as cursor:
					cursor.execute("select Id ,Answer from dbo.QuestionAnswers where Id = " + id )
					row = cursor.fetchone()
					while row:
						print (str(row[0]) + " " + str(row[1]))
						finalString = str(row[1])
						paragraph = paragraph + str(row[0]) + " "+ str(row[1])+". "
						row = cursor.fetchone()
						count += 1
						break
			break
		else:
			print("else")
		#print()
	# except:
		# print('something went wrong')
	return jsonify("{answer : "+finalString+"}")

#app.run(debug=True, host='0.0.0.0')
