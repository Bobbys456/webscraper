from flask import Flask
from flask import send_file

app = Flask(__name__)

@app.route("/hello")
def home():
    return "Hello, World!"

@app.route('/return-files/')
def return_files_tut():
	try:
		return send_file(r'C:\Users\bobby\OneDrive\Documents\python projects\webscraper\reviews\good\summary.csv', as_attachment='words.csv')
	except Exception as e:
		return str(e)
    
if __name__ == "__main__":
    app.run(debug=True)