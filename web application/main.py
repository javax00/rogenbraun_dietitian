from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods =["GET", "POST"])
def login():
	if not session.get("session_name"):
		if request.method == "POST":
			uname = request.form.get("user")
			pword = request.form.get("pass")
			session["session_name"] = request.form.get("user")

			return redirect(url_for('index'))
		return render_template('login.html')
	return redirect(url_for('index'))

@app.after_request
def after_request(response):
	response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
	return response

@app.route('/main')
def index():
	if session.get("session_name"):
		return render_template('index.html')
	return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session["session_name"] = None
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True)


try:
	pass
except Exception as e:
	raise e