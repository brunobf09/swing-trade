from flask import Flask
import pandas as pd
from swing_trade import search


app = Flask(__name__)

def swing_trade():
    carteira = pd.read_csv("https://www.dropbox.com/s/juhwwtpgml3xtrw/B3.csv?dl=1")
    romp = []
    ini = []
    for stock in carteira.Stock:
        try:
            df = search(stock)
            if df.Entrada[-1] > 0 and df.Entrada[-2] == 0:
                romp.append(df.tail(1).set_index("Stock"))
            elif df.Entrada[-1] > 0 and df.Entrada[-2] > 0:
                ini.append(df.tail(1).set_index("Stock"))
            else:
                pass

            if len(romp) == 0:
                op_romp = "\n Não Houve Operações de Rompimento.\n"
            if len(ini) == 0:
                op_ini = "\n Não há Operações Correntes.\n"
            if len(romp) > 0:
                op_romp = pd.concat(romp)
            if len(ini) > 0:
                op_ini = pd.concat(ini)
        except:
            pass
    if type(op_romp)==str and type(op_ini)!=str :
        return op_romp, op_ini.to_html()
    elif type(op_romp)!=str and type(op_ini)==str:
        return op_romp.to_html(), op_ini
    elif type(op_romp)!=str and type(op_ini)!=str:
        return op_romp,op_ini
    else:
        return op_romp.to_html(), op_ini.to_html()

@app.route('/')
def index():
    html1,html2 = swing_trade()
    return """<head><center><h1>Swing Trade</h1></head></center>
        <body>
        <center>Operação Inicializada</center>
        <center><table>
                 {}
        </table></center>
        <center>Operação Corrente</center>
        <center><table>
                 {}
        </table></center>
        </body>""".format(html1,html2)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')

# flask run
