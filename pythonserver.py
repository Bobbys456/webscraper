from flask import Flask
from flask import send_file
import data2

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello, World!"

@app.route('/return-files/')
def return_files_tut():
	print('jhell')
	data2.main()
	try:
		return send_file(r'C:\Users\bobby\OneDrive\Documents\python projects\webscraper\reviews\good\summary.csv', as_attachment='words.csv')
	except Exception as e:
		return str(e)
    
if __name__ == "__main__":
    app.run(debug=True)