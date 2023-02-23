from flask import Flask, make_response, redirect, render_template, url_for, request
from flask import send_file
import data2

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"

@app.route('/companies',methods = ['POST'])
def addCompany():
	if(request.method == 'POST'):
		company = request.form['name']
		f = open("companies.txt", "w")
		f.write(company.strip() + "\n")
		f.close()

		data2.main()
		csv_path = 'reviews/good/summary.csv'

    	# Return the file using send_file
		resp = make_response(render_template('error.html'), 404)
	

    # Path to the pre-made CSV fie
    

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file(r'C:\Users\bobby\OneDrive\Documents\python projects\webscraper\reviews\good\summary.csv', as_attachment='words.csv')
	except Exception as e:
		return str(e)
    
if __name__ == "__main__":
    app.run(debug=True)