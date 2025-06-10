from flask import Flask, request, render_template, json
#=nb

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/api/data', methods=['GET', 'POST'])
def data():
    data = request.get_json()
    with open('img.json', 'w') as f:
        json.dump(data, f, indent=4)
    return data