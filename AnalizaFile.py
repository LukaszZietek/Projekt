
import pandas as pd
from datetime import date, datetime, timedelta
import os
import matplotlib.pyplot as plt
#--------------------------------------------------------------------

# Wczytanie danych z pliku CSV
url = 'https://raw.githubusercontent.com/LukaszZietek/Projekt/master/dde9c647-a1e0-4c7f-b563-4dee517f8ce8_Data.csv'
AdultsRates=pd.read_csv(url, error_bad_lines=False)
url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data" \
      f"/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

dfD = pd.read_csv(url, error_bad_lines=False)

#----------------------------------FUNKCJE-----------------------------------------------

# Usuniecie niepotrzebnych kolumn i wierszy z tabeli AdultsRates oraz posortowanie i zastapienie . na zera
def PrepareAdultsTabel(tabel):
    tabel.drop(tabel.tail(5).index, axis = 0, inplace= True)
    tabel['2020 [YR2020]'] = tabel['2020 [YR2020]'].replace(to_replace='..',value="0.0000")
    tabel['2020 [YR2020]'] = tabel['2020 [YR2020]'].astype(float)
    tabel.drop(['2019 [YR2019]','Series Code', 'Series Name','Country Code'],axis = 1, inplace = True)
    tabel = tabel.sort_values(by='2020 [YR2020]', ascending= False)
    return tabel

def format_date(date: datetime.date): # formatowanie daty aby pasowala do tej podanej w tabeli
    if os.name == "nt":
        return date.strftime('%#m/%#d/%y')
    else:
        return date.strftime('%-m/%-d/%y')

def perdelta(start, end, delta): # zwraca liste dat od okreslonego momentu
    curr = start
    lista = []
    i = 0
    while curr < end:
        lista.append(format_date(curr))
        curr += delta
    lista.append(format_date(curr))
    return lista


def PrepareDfdTable(tabel): #przygotowuje tabele dfD, usuwa z niej niepotrzebne elementy oraz sumuje odpowiednie kolumny
    lista = perdelta(date(2020,1,22),date(2020,3,23),timedelta(days=1))
    tabel['Sum'] = 0
    for i in range(len(lista)):
        tabel['Sum'] += tabel[f'{lista[i]}']
        del tabel[f'{lista[i]}']
    tabel=tabel.groupby('Country/Region', as_index=False).sum()
    tabel = tabel.sort_values(by = "Sum", ascending = False)
    return tabel


def PrepareAdultsPlot(data): # Przygotowuje Wykres dla danych Adults
    ax =data.head(10).plot.bar(x='Country Name', y = '2020 [YR2020]', figsize=(20,10), rot = 0, color='#98A63E',grid = True, fontsize=15)
    ax.set_xlabel("Country", fontsize =28, color='black')
    ax.set_ylabel('Percent of people over 65 [%]',fontsize = 28, color='black')
    ax.set_facecolor('#D2BBE6')
    ax.set_title("How many percent of people over 65 years", fontsize = 40,color = 'black')
    return ax

def PrepareDfdPlot(data): # Przygotowuje Wykres dla danych dfD
    ax =data.head(10).plot.bar(x='Country/Region', y = 'Sum', figsize=(20,10), rot = 0, color='#98A63E',grid = True, fontsize=15)
    ax.set_xlabel("Country", fontsize =28, color='black')
    ax.set_ylabel('Number of death',fontsize = 28, color='black')
    ax.set_facecolor('#D2BBE6')
    ax.set_title("Sum of death since the pandemic started", fontsize = 40,color = 'black')
    return ax

def ReturnSumOfDeath(data): # Zwraca ogolna liczbe smierci od poczatku pandemii
    return data.loc[data['Sum']>0]['Sum'].sum()
# ------------------------------------------------------- KONIEC FUNKCJI

AdultsRates = PrepareAdultsTabel(AdultsRates)
dfD = PrepareDfdTable(dfD)

print("Tabela przedstawiajaca procentowy udzial osob starszych w ludnosci w danych krajach")
print(AdultsRates.head(20))
print ('--------------------------------------------------------\n\n\n')
print("Tabela przedstawiajaca kraje z najwieksza iloscia smierci spowodowana wirusem COVID-19")
print(dfD.head(20))
print ('--------------------------------------------------------\n\n\n')

print(f"Sum of death: {ReturnSumOfDeath(dfD)}") # pokazuje sume smierci przez COVIDA-19
print ('--------------------------------------------------------\n\n\n')

print(AdultsRates.loc[AdultsRates['Country Name'] == 'China']) #pokazuje procent osob starszych w Chinach
print ('--------------------------------------------------------\n\n\n')

ax = PrepareDfdPlot(dfD)
bx = PrepareAdultsPlot(AdultsRates)

plt.show()







