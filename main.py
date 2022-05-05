from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("hi")
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form['appt']
    return (data)

@app.route('/open', methods=['GET', 'POST'])
def home():
    print("hello")
    return ("hi")

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)