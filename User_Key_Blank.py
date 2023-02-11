# This file is used to contain all the User profile data and stock/ETF information that will be invested
# Rename to 'User_Key.py' to use in script

def total_purchases(investments):
    tot = 0.0
    for i in range(0, len(investments)):
        purchase = float(investments[i])
        tot += purchase
    return tot

# ==================================================================================================


User = 'Username Here'

Password = 'Password Here'

User_Email = 'GoogleAccount@gmail.com here'  # The personal account that will be checked

BotEmail_Username = 'GmailAccount@gmail.com Here'  # Bot Account

BotEmail_Password = 'GoogleAppPassword Here'  # 2-Factor Google App Password

# There will be 2 lists for the names of the securities and a corresponding list for the Investment amount
""" ** MAKE SURE ETFs[n] MATCHES UP WITH ETF_Investments[n] ** """

# The 1-5 Letter Symbols that represent the Stock/ETF
ETFs = ['Stock/ETF 1', 'Stock/ETF 2', 'Stock/ETF 3', 'Stock/ETF 4']

# Amount in 'dollars.cents' you'd like to invest corresponding to the same index as the stock name
ETF_Investments = ['0.00', '0.00', '0.00', '0.00']



