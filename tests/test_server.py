from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_test_page():
	return open('./test.html').read()

if __name__ == '__main__':
	app.run(host='localhost', port=8080, debug=True)