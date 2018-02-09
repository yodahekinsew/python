from flask import Flask, render_template, json, request
import webbrowser

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/6.009.html")
def programming_page():
	return render_template('6.009.html')

@app.route("/8.02.html")
def physics_page():
	return render_template('8.02.html')

@app.route("/21L.011.html")
def hass_page():
	return render_template('21L.011.html')

@app.route("/6.042.html")
def math_page():
	return render_template('6.042.html')

webbrowser.open('http://127.0.0.1:5000/')

if __name__ == "__main__":
    app.run()