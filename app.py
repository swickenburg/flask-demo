from flask import Flask, render_template, request, redirect
from pandas_datareader.data import DataReader
import datetime as dt

from bokeh.plotting import figure, show, save
from bokeh.io import output_notebook, output_file
from pandas_datareader.data import DataReader
import datetime as dt


app = Flask(__name__)

#test
# @app.route('/')
# def main():
  # return redirect('/index')
  # return 'Hello World'
  # a =  str(get_price('AAPL')[0])
  # return str(get_price('AAPL')[0])

@app.route('/')
def data_in():
  return render_template('data_in.html')

@app.route('/', methods=['POST'])
def data_out():
  symbol = request.form['symbol']
  a =  get_price(symbol)
  output_file("templates/line.html")
  
  p = figure(title= symbol + " stock price", plot_width=800, plot_height=600,
             x_axis_type="datetime")
  p.line(x=a.index, y=a.values, line_width=2)
  save(p)
  return render_template('line.html')
  # return a

@app.route('/plot')
def plot_line():
  return render_template('line.html')

def get_price(
    symbol,
    start='30 Sep 2013',
    end='today',
    adjusted=True,
    ):
    if end == 'today':
        end = dt.date.today()
    else:
        end = dt.datetime.strptime(end, '%d %b %Y')

    try:
        start = dt.datetime.strptime(start, '%d %b %Y')
    except:
        pass

    if adjusted:
        price_all = DataReader(symbol, 'yahoo', start, end)['Adj Close']
    else:
        price_all = DataReader(symbol, 'yahoo', start, end)['Close']
    return price_all
if __name__ == '__main__':
  # app.run(port=33507)
  app.run(host='0.0.0.0', debug=True, use_reloader=True)
