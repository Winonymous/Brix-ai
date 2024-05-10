# import flast module
from flask import Flask, request, render_template, jsonify, url_for, redirect
from module.findmatch import FindMatch
from auth.login import valid_login

index_file = "Resource/openai.index"
model_name = "paraphrase-MiniLM-L6-v2"
df_file = "Resource/Brix guest query and response.csv"

match_finder = FindMatch(index_file, model_name, df_file)

# instance of flask application
app = Flask(__name__)

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        vl = valid_login(request.form['username'],
                       request.form['password'])
        print(len(vl))
        if len(vl) > 0:
            return redirect(url_for('user', username = vl["Name"]))
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route("/guest")
def guest():
	return chat_interface()

@app.route("/student/<username>")
def user(username):
	return chat_interface(username)

def chat_interface(name = None):
	return render_template("chat_interface.html", name = name)

# route that returns hello world text
@app.route("/question", methods = ['POST'])
def hello_world():
	data = request.json
	response = match_finder.find_match(data['msg'], 1)

	return jsonify({
		"ok": "True",
		"resp": response})


if __name__ == '__main__':
	app.run(debug=True)
