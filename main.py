import requests
import tkinter as tk
from tkinter import ttk, messagebox

def get_exchange_rates():
    """Fetch exchange rates from the API using USD as the base currency."""
    url = "https://api.exchangerate-api.com/v4/latest/USD"  # Fixed base currency as USD
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Error fetching data from the API.")

    return response.json()

def convert_currency(amount, from_currency, to_currency, rates):
    """Convert currency using the fetched rates."""
    if from_currency == to_currency:
        return amount

    # Convert amount to base currency (USD)
    base_amount = amount / rates['rates'][from_currency]

    # Convert base currency to target currency
    converted_amount = base_amount * rates['rates'][to_currency]
    return converted_amount

def perform_conversion():
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_combo.get()
        to_currency = to_currency_combo.get()

        if not from_currency or not to_currency:
            messagebox.showerror("Error", "Please select both currencies.")
            return

        converted_amount = convert_currency(amount, from_currency, to_currency, rates)
        result_label.config(text=f"{amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
    except KeyError:
        messagebox.showerror("Error", "Invalid currency code entered.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Fetch exchange rates
try:
    rates = get_exchange_rates()
except Exception as e:
    messagebox.showerror("Error", str(e))
    exit()

# Create the main window
root = tk.Tk()
root.title("Currency Converter")
root.geometry("400x300")

# Title label
title_label = tk.Label(root, text="Currency Converter", font=("Arial", 18))
title_label.pack(pady=10)

# Amount entry
amount_label = tk.Label(root, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack(pady=5)

# From currency selection
from_currency_label = tk.Label(root, text="From Currency:")
from_currency_label.pack()
from_currency_combo = ttk.Combobox(root, values=list(rates['rates'].keys()), state="readonly")
from_currency_combo.pack(pady=5)

# To currency selection
to_currency_label = tk.Label(root, text="To Currency:")
to_currency_label.pack()
to_currency_combo = ttk.Combobox(root, values=list(rates['rates'].keys()), state="readonly")
to_currency_combo.pack(pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert", command=perform_conversion)
convert_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Arial", 14), fg="green")
result_label.pack(pady=10)

# Bindings for faster response
def optimize_selection(event):
    event.widget.update_idletasks()

from_currency_combo.bind("<Button-1>", optimize_selection)
to_currency_combo.bind("<Button-1>", optimize_selection)

# Run the main event loop
root.mainloop()





