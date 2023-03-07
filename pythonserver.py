from flask import Flask, make_response, redirect, render_template, url_for, request
from flask import send_file
import data2
import os 

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"

@app.route('/companies',methods = ['POST', 'GET'])
def addCompany():
	if(request.method == 'POST'):
		company = request.form['name']
		f = open("companies.txt", "w")
		f.write(company.strip() + "\n")
		f.close()

		data2.main()
		return redirect("http://127.0.0.1:5000/get", code=302)

@app.route('/get',methods = ['POST', 'GET'])	
def getcompany(): 
	##gjsdihbgfuoeh	
	try:
		return send_file(r'C:\Users\bobby\OneDrive\Documents\python projects\webscraper\reviews\good\summary.csv', as_attachment='words.csv')
	except Exception as e:
		return str(e)

@app.route('/done',methods = ['GET'])	
def status(): 	
	print(os.listdir('reviews/good'))
	
    

	
if __name__ == "__main__":
    app.run(debug=True)