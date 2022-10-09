from tkinter import *
from tkinter import ttk
import requests
from tinydb import TinyDB, Query
from datetime import datetime
from sys import exit

db = TinyDB('db.json')

_today = datetime.now()
today = _today.date()


class Rates:
    '''Class to save fresh rates to a TinyDB'''

    @staticmethod
    def refresh_rates():
        rates = {}
        data = requests.get('http://api.nbp.pl/api/exchangerates/tables/c/?format=json').json()
        # Extracting only the rates from the json data
        for i in data[0]['rates']:
            rates[i['code']] = i['bid']
        db.insert({str(today): rates})

    def get_last_rates(self):
        return db.all()[-1][str(today)]

    @staticmethod
    def get_current_rate_date():
        try:
            return next(iter(db.all()[-1].keys()))
        except IndexError:
            return 'no rates in DataBase'

    def remove_from_db(self):
        pass

    def search_in(self, date):
        Date = Query()
        return db.search(Date.date == date)


class CurrencyConvertor:

    def __init__(self):
        try:
            self.rates = db.all()[-1]
        except IndexError:
            print('No db excist')

    def print_rates(self):
        try:
            print(self.rates)

        except AttributeError:
            print('No rates to print')

    def convert(self, num, convert_from, convert_to):
        rates = self.rates[str(today)]
        if convert_from == 'PLN':
            rate = rates[convert_to.upper()]
            return round(num / rate, 2)

        elif convert_to == 'PLN':

            # from_rate = rates[convert_from.upper()]
            # rate_to = rates[convert_to.upper()]
            return round(num * rates[convert_from.upper()], 2)

        else:
            amount = round(num * rates[convert_from.upper()])
            # from_rate = rates[convert_from.upper()]
            # rate_to = rates[convert_to.upper()]
            return round(amount / rates[convert_to.upper()], 2)


# Driver code
if __name__ == "__main__":
    rates = Rates()
    rates.refresh_rates()


def calculate(*args):
    try:
        c = CurrencyConvertor()
        value = float(amount.get())
        convert_to = on_select_to(args)
        convert_from = on_select_from(args)
        result.set(c.convert(value, convert_from, convert_to))
    except ValueError:
        pass


def refresh():
    rates.refresh_rates()


def on_select_to(event):
    current_value_selected = currency_to_convert_chosen.get()
    ttk.Label(mainframe, text=current_value_selected, padding="5 5 5 5").grid(column=3, row=2, sticky=W)
    return current_value_selected


def on_select_from(event):
    current_value_selected = currency_from_convert_chosen.get()
    ttk.Label(mainframe, text=current_value_selected, padding="5 5 5 5").grid(column=1, row=2, sticky=W)
    return current_value_selected


root = Tk()
root.title("Currency converter")


mainframe = ttk.Frame(root, width=1200, height=800, style='Danger.TFrame', padding="5 5 22 22")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=2)
root.rowconfigure(0, weight=2)

amount = StringVar()
currency_from_convert_chosen = StringVar()
currency_to_convert_chosen = StringVar()


currency_from_convert = ttk.Combobox(mainframe, textvariable=currency_from_convert_chosen, width=5)
currency_from_convert.grid(column=1, row=1)
currency_from_convert['values'] = ('PLN', 'USD', 'AUD', 'CAD', 'EUR', 'HUF', 'CHF', 'GBP', 'JPY', 'CZK', 'DKK', 'NOK', 'SEK', 'XDR')  # ustawienie elementów zawartych na liście rozwijanej
currency_from_convert.current(0)
current_value_from = currency_from_convert.get()

currency_to_convert = ttk.Combobox(mainframe, textvariable=currency_to_convert_chosen, width=5)
currency_to_convert.grid(column=2, row=1)
currency_to_convert['values'] = ('USD', 'PLN', 'AUD', 'CAD', 'EUR', 'HUF', 'CHF', 'GBP', 'JPY', 'CZK', 'DKK', 'NOK', 'SEK', 'XDR')  # ustawienie elementów zawartych na liście rozwijanej
currency_to_convert.current(0)
current_value = currency_to_convert.get()


amount_entry = ttk.Entry(mainframe, width=4, textvariable=amount)
amount_entry.grid(column=4, row=1, sticky=(W, E))

result = StringVar()
ttk.Label(mainframe, textvariable=result).grid(column=4, row=2, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=4, row=3, sticky=W)
ttk.Button(mainframe, text="Exit", command=exit).grid(column=4, row=5, sticky=W)

ttk.Label(mainframe, text="amount").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="equivalent to").grid(column=2, row=2, sticky=E)
ttk.Label(mainframe, text=current_value).grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text=current_value_from).grid(column=1, row=2, sticky=W)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

amount_entry.focus()


currency_to_convert.bind("<<ComboboxSelected>>", on_select_to)
currency_from_convert.bind("<<ComboboxSelected>>", on_select_from)
root.bind("<Return>", calculate)

root.mainloop()

