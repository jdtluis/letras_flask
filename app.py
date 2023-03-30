from flask import Flask, render_template, request
import os
import requests
import pandas as pd
from utils import letras as lt
import sqlite3
from enum import Enum

app = Flask(__name__)


class tipoletra(Enum):
	ledes = 1
	lecer = 2

@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def index(chartID = 'chart_ID', chart_height = 400): #
	if request.method == 'GET':
		return render_template('/ticker_block.html', chartID='', series=[], title='', container=[])

	if request.method == "POST":
		letras = request.form['letra']
		if letras == 'both':
			letras = ['ledes', 'lecer']
		else:
			letras = [letras]
		date = request.form['date']

		series = {}
		title = {}
		container = {}

		for s in letras:
			data = getdata(s, date)

			if data.empty:
				series[s] = [[0,0],[0,0]]
			else:
				data['TIR'] = round(data['TIR'], 4)
				dm, fit = lt.fitCurve(data['DM'], data['TIR'])
				fitted = [list(d) for d in zip(dm.tolist(), fit.round(2).tolist())]
				series[s] = [data[['DM', 'TIR']].values.tolist(), fitted]
			title[s] = {"text": s}
			container[s] = s
		return render_template('/ticker_block.html', chartID=chartID, series=series, title=title, container=container)


def getdata(letra, date):
	con = sqlite3.connect('data/letras.db')
	data = con.execute(f'SELECT Especie, FechaPrecio, CAST(DM as int) DM, TIR FROM {letra} WHERE FechaPrecio = "{date}" ORDER BY cast(DM as int) asc').fetchall()
	con.close()
	if not data:
		return pd.DataFrame([])
	else:
		data = pd.DataFrame(data, columns=['Especie', 'FechaPrecio', 'DM', 'TIR'])
		data = data[~data['DM'].isna()]
		return data


#if __name__ == "__main__":
	#app.run(debug = True, passthrough_errors=True) #, host='0.0.0.0', port=8080
