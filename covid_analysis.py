import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
from PyQt5 import QtGui, QtCore, QtWidgets
import covid_gui
import sys


class guiInput(QtWidgets.QMainWindow, covid_gui.Ui_MainWindow):
    def __init__(self, parent=None, states=None, counties=None):
        super(guiInput, self).__init__(parent)
        self.setupUi(self, states=states, counties=counties)
        self.pushButton.clicked.connect(self.chart)

    def chart(self):
        results = []
        to_view = self.cb1.currentText()
        covid = prep_place(to_view)
        covid3 = prep_place_2(to_view)
        covid4 = pd.merge(covid, covid3, how='outer', on=['date', 'place'])

        if to_view in get_states():
            header_labels = ['Date', 'Tests', 'Cases', 'Deaths', 'Hospitalizations', '% Positive']
            for rows in covid4.itertuples():
                my_list = [rows.date.strftime('%m/%d/%y'), str(rows.totalTestResultsIncrease),
                           str(rows.positiveIncrease),
                           str(rows.deathIncrease),
                           str(rows.hospitalizedIncrease),
                           str(round((rows.positiveIncrease / rows.totalTestResultsIncrease) * 100, 2))]
                results.append(my_list)
        else:
            for rows in covid4.itertuples():
                my_list = [rows.date.strftime('%m/%d/%y'), str(rows.cases), str(rows.change_in_cases),
                           str(rows.deaths),
                           str(rows.change_in_deaths), '']
                results.append(my_list)
            header_labels = ['Date', 'Cases', 'Change in Cases', 'Deaths', 'Change in Deaths', '']
        self.display_results(results, header_labels)
        plot_data(covid, covid4, to_view)


cut_off_days = 10
start_date = date.today() - timedelta(days=cut_off_days)
start_date = pd.Timestamp(start_date)
plt.rcParams['figure.figsize'] = (12.0, 12.0)


def add_columns(df):
    df.date = pd.to_datetime(df['date'].astype('str'), format='%Y-%m-%d')
    df.date = df.date.dt.date
    df['change_in_cases'] = df.cases.diff().fillna(0).astype(int)
    df['change_in_deaths'] = (df.deaths.diff()).fillna(0).astype(int)
    return df[df.date >= start_date]


def plot_data(df, df3, to_view):
    if to_view in get_states():
        chart1 = df3.plot(x='date',
                          y=['positiveIncrease', 'deathIncrease', 'hospitalizedIncrease', 'totalTestResultsIncrease', ],
                          title="{} - in the last {} days".format(to_view, cut_off_days),
                          kind='bar',
                          use_index=True, logy=True)
        chart1.set_xlabel("{} - in the last {} days".format(to_view, cut_off_days))
        labels = ['Cases', 'Deaths', 'Hospitalizations', 'Tests']
        for index, value in enumerate(df3['positiveIncrease']):
            plt.text(index, value, str(value))
        for index, value in enumerate(df3['deathIncrease']):
            plt.text(index, value, str(value))
        for index, value in enumerate(df3['hospitalizedIncrease']):
            plt.text(index, value, str(value))
        for index, value in enumerate(df3['totalTestResultsIncrease']):
            plt.text(index, value, str(value))
    else:
        chart1 = df.plot(x='date', y=['change_in_cases', 'change_in_deaths'],
                         kind='bar',
                         title="{} - in the last {} days".format(to_view, cut_off_days),
                         use_index=True, logy=True)
        labels = ['Cases', 'Deaths']

        for index, value in enumerate(df['change_in_cases']):
            plt.text(index, value, str(value))
        for index, value in enumerate(df['change_in_deaths']):
            plt.text(index, value, str(value))
    chart1.legend(labels)
    plt.show()


def combine_data():
    df1 = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    df1.rename(columns={'state': 'place'}, inplace=True)
    df2 = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv')
    df2.rename(columns={'county': 'place'}, inplace=True)
    return pd.concat([df1, df2], sort=False)


def prep_place(to_view):
    df = combine_data()
    try:
        county, st = to_view.split(',')
        df = df.loc[(df['state'] == st) & (df['place'] == county)]
    except:
        df = df.loc[(df['place'] == to_view)]
    df.sort_values(by=['place', 'date'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = add_columns(df)
    df.date = pd.to_datetime(df['date'].astype('str'), format='%Y-%m-%d')
    return df


def prep_place_2(to_view):
    df3 = pd.read_csv('https://covidtracking.com/api/v1/states/daily.csv')
    df3.loc[(df3.state == translate_states().get(to_view)), 'state'] = to_view
    df3.date = pd.to_datetime(df3['date'].astype('str'), format='%Y%m%d')
    df3 = df3.loc[df3['state'] == to_view]
    df3 = df3[df3.date >= start_date]
    df3.rename(columns={'state': 'place'}, inplace=True)
    df3.sort_values(by=['place', 'date'], inplace=True)
    df3.reset_index(drop=True, inplace=True)
    return df3


def translate_states():
    states_dict = {'Florida': 'FL', 'California': 'CA', 'Georgia': 'GA'}
    return states_dict


def get_states():
    states = ['Florida', 'California', 'Georgia']
    return states


def get_counties():
    counties = ['Miami-Dade,Florida', 'Broward,Florida', 'Palm Beach,Florida', 'Monroe,Florida','Denver,Colorado','Los Angeles,California']
    return counties


def main():
    states = get_states()
    counties = get_counties()
    app = QtWidgets.QApplication(sys.argv)
    form = guiInput(states=states, counties=counties)
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
