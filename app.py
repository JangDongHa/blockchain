import base64
import os

from flask import Flask, render_template, jsonify, request, scaffold
from matplotlib import pyplot as plt
from io import BytesIO
import test
import json

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('main.html')


@app.route('/chart/<mode>/<type>', methods=['GET'])
@app.route('/json/<mode>/<type>', methods=['GET'])
@app.route('/db/<mode>', methods=['GET'])
def getChartJson(mode, type='d'):
    return render_template('index.html', mode=mode, type=type)


@app.route('/db', methods=['POST'])
def dbPost():
    mode = request.form['mode'].upper()
    pngs = ['CBC test', 'CTR test']
    imgStart = f"<img src='/static/result/db/"
    imgEnd = ".png'/>"
    if mode == 'CBC':
        return jsonify(img=imgStart + pngs[0] + imgEnd)
    elif mode == 'CTR':
        return jsonify(img=imgStart + pngs[1] + imgEnd)


@app.route("/chart", methods=['POST'])
def chartPost():
    mode = request.form['mode'].upper()
    type = request.form['type']
    dir = os.getcwd() + '/result' + '/png/'
    pngs = ['encryptAesCbc', 'decryptAesCbc', 'encryptAesCtr', 'decryptAesCtr']
    imgStart = f"<img src='/static/result/png/"
    imgEnd = ".png'/>"
    if mode == 'CBC':
        if type == 'e':
            return jsonify(img=imgStart + pngs[0] + imgEnd)
        elif type == 'd':
            return jsonify(img=imgStart + pngs[1] + imgEnd)
    elif mode == 'CTR':
        if type == 'e':
            return jsonify(img=imgStart + pngs[2] + imgEnd)
        elif type == 'd':
            return jsonify(img=imgStart + pngs[3] + imgEnd)
    return jsonify(img=f"<p>can't find data</p>")


@app.route('/json', methods=['POST'])
def jsonPost():
    mode = request.form['mode'].upper()
    type = request.form['type']
    dir = os.getcwd() + '/static/result/json/'
    jsons = ['encryptAesCbc.json', 'decryptAesCbc.json', 'encryptAesCtr.json', 'decryptAesCtr.json']

    if mode == 'CBC':
        if type == 'e':
            with open(dir + jsons[0]) as f:
                jsonData = json.load(f)
            return jsonify(result=jsonData)
        elif type == 'd':
            with open(dir + jsons[1]) as f:
                jsonData = json.load(f)
            return jsonify(result=jsonData)
    elif mode == 'CTR':
        if type == 'e':
            with open(dir + jsons[2]) as f:
                jsonData = json.load(f)
            return jsonify(result=jsonData)
        elif type == 'd':
            with open(dir + jsons[3]) as f:
                jsonData = json.load(f)
            return jsonify(result=jsonData)

    return jsonify(result=f"<p>can't find data</p>")


'''
@app.route("/run/chart", methods=['POST'])
def runChartPost():
    mode = request.form['mode'].upper()
    type = request.form['type']
    # Generate plt
    plt.clf()
    fig = test.aes(type, mode)

    plt.xlabel('File Size')
    plt.ylabel('time (s)')
    plt.title(fig[2] + ' Time according to file size with using AES-128(' +mode +')')
    plt.plot(fig[0], fig[1])
    # Save it to a temporary buffer.
    buf = BytesIO()
    plt.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return jsonify(img=f"<img src='data:image/png;base64,{data}'/>")


@app.route('/run/json', methods=['POST'])
def runJsonPost():
    mode = request.form['mode'].upper()
    type = request.form['type']
    result = test.aes(type, mode)
    time = result[1]
    size = result[0]
    data = []

    for i in range(0, len(time)):
        json = {
            'time': time[i],
            'size': size[i]
        }
        data.append(json)

    return jsonify(result=data)
'''

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
