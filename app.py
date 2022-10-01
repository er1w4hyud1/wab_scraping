from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/history/IDR/USD/T')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('div',attrs={'class':'table-responsive'})
row = table.find_all('tr')

row_length = len(row)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
 for i in range(1, row_length):

    #scrapping process
    DayPrice=row[i].find('a').text
    Period=row[i].find('td').text
    temp.append((DayPrice,Period))   
    

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp, columns = ('harga harian','tanggal'))

#insert data wrangling here
data['harga harian'] = data['harga harian'].apply(lambda x: x.replace(',',''))
data['harga harian']=data['harga harian'].astype('float64')
data['tanggal']=data['tanggal'].astype('datetime64')

#end of data wranggling 

@app.route("/")
def index(): 
	
	##card_data = f'{data["____"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(x='tanggal',y='harga harian')
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		#card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)