# import flast module
from flask import Flask, request, render_template, jsonify, url_for, redirect, session
from module.findmatch import FindMatch
from auth.login import valid_login

import chromadb
from module.pdfretireval import HandBookChat
from module.chromadbretrieval import ClassRetreival
import secrets
import string

def generate_secret_key(length=24):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

index_file = "Resource/openai.index"
model_name = "paraphrase-MiniLM-L6-v2"
df_file = "Resource/Brix guest query and response.csv"

match_finder = FindMatch(index_file, model_name, df_file)

# Chroma Client
chroma_client = chromadb.PersistentClient(path="Resource/chroma_db")

# print(os.environ['HF_TOKEN'])
file_path = "Resource/Bells-Revised-Students-Handbook-Updated-version-1.pdf"
llm_id = "mistralai/Mistral-7B-Instruct-v0.2"

chat = HandBookChat(file_path, client=chroma_client, llm_id = llm_id)
RetrivalModel = ClassRetreival(chroma_client)

# instance of flask application
app = Flask(__name__)
app.secret_key = generate_secret_key()

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('user', username = session['username']))
    return redirect(url_for('login'))

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if request.method == 'POST':
        vl = valid_login(request.form['username'],
                       request.form['password'])
        print(len(vl))
        if len(vl) > 0:
            session['username'] = vl["Name"]
            session['Department'] = vl["Department"]

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

    question = data['msg']

    answer, dist = RetrivalModel.get_response(question)
    if dist > 0.5:
        answer = chat.respond(question, type = "refine")
    try:
        response = chat.respond_user(question, session['username'], session['Department'], answer)
    except:
        response = chat.respond_guest(question, answer)
          
    return jsonify({
		"ok": "True",
		"resp": response})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)
