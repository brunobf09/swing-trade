import warnings
warnings.filterwarnings('ignore')
import yfinance as yf

def search(stock):
  for stocks in [stock]:
    day = yf.Ticker(stocks).history(period="max", interval="1d")
  for na in [day]:
    na.dropna(axis=0, inplace=True)
    na['mal'] = na["Close"].rolling(window=34).quantile(0.025)
    na['mah'] = na["Close"].rolling(window=34).quantile(0.975)

  day["sinal"] = 0
  df = day[["Close","mal","mah","sinal"]]
  df.dropna(axis=0,inplace=True)
  sinal = []
  for i in range(df.shape[0]):
    if df.Close[i]>df.mah[i]:
      a = 1
    else:
      a = 0
    sinal.append(a)
  df.sinal = sinal

  entrada=[]
  stop=[]
  alvo=[]
  ganho=[]
  perda=[]
  e=0
  s=0
  a=0
  for i in range(df.shape[0]):
    if df.sinal[i-1]==0 and df.sinal[i]==1 and e==0:
      e = df.Close[i]
      s = e*0.97
      a = e*1.07
      p=0
      g=0
    elif e>0 and df.Close[i]<s:
      p=1
      e=0
      s=0
      a=0
    elif e>0 and df.Close[i]>a:
      g=1
      e=0
      s=0
      a=0
    else:
      g=0
      p=0
    entrada.append(e)
    stop.append(s)
    alvo.append(a)
    ganho.append(g)
    perda.append(p)
  df["Entrada"] = entrada
  df["Stop"] = stop
  df["Alvo"] = alvo
  df["Perda"] = perda
  df["Ganho"] = ganho
  df["Stock"] = stock

  return df[["Stock","Close","Entrada","Stop","Alvo"]]

