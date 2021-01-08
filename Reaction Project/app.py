from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/likes')
def likes():
    return data


@app.route('/', methods=['POST','GET'])
def index():
    if request.method == "POST":
        global data
        data = request.data
        return data
    else:
        return render_template('Ins Reaction.html')


if __name__ == '__main__':
    app.run(debug=True)
