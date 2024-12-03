import locale

# Set locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def format_currency(amount):
    return locale.currency(amount, grouping=True) if amount is not None else "$0.00"
