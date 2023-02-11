# imported libraries
import User_Key
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import time
from datetime import datetime
from datetime import timedelta
from email.message import EmailMessage
import ssl
import smtplib


# Defining the webdriver
opts = uc.ChromeOptions()
# Headless option for running without UI
# opts.add_argument('--headless')
driver = uc.Chrome(version_main=109)
driver.implicitly_wait(20)  # gives an implicit wait for 120 seconds for finding all elements

# Initializing Global Variables
error_msg = 'No Errors'  # JUST A PLACE HOLDER CURRENTLY
account_balance = '0.00'
starting_balance = '0.00'
time_purchased = []
ERR = 0

def fidelity_login():
    # Go to login page
    driver.get('https://digital.fidelity.com/prgw/digital/login/full-page')
    # Enter Username
    username_input_element = driver.find_element(by=By.ID, value="userId-input")
    username_input_element.click()
    username_input_element.send_keys(User_Key.User)
    # Enter Password
    password_input_element = driver.find_element(by=By.ID, value="password")
    password_input_element.click()
    password_input_element.send_keys(User_Key.Password)
    # Send Enter After Password
    password_input_element.send_keys(Keys.ENTER)
    time.sleep(3)


def fidelity_security_purchasing():
    # Global variables
    global account_balance
    global starting_balance
    global time_purchased
    global ERR
    global error_msg
    
    # Initially getting this url to pick up cookies
    driver.get('https://www.fidelity.com/')

    # Go to 'trade' page
    driver.get('https://digital.fidelity.com/ftgw/digital/trade-equity/index/orderEntry')

    for i in range(0, len(User_Key.ETFs)):
        # Default Tade Option is 'Stocks/ETFs' and the whole point of this program is to buy ETFs so no need to change this
        # Selecting an Account
        account_selection = driver.find_element(by=By.XPATH, value='//*[@id="dest-acct-dropdown"]').click()
        # Using a profile with only 1 account opened
        driver.find_element(by=By.ID, value='ett-acct-sel-list').click()

        # Finding Account Balance
        # Giving to collect the real time data once and subtract from
        if i == 0:
            account_balance = driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__account-balance"]/div/div[2]/span').text
            account_balance = float(account_balance[1:])  # Omitting the $ in the front of the text to convert string to a float
            starting_balance = account_balance
            print(account_balance)

        # Selecting the ETF to be purchased (WRITE AS A RECURSIVE FUNCTION BASED OF DATA IN USER_KEY.py)
        etf_selector_selector = driver.find_element(by=By.ID, value='eq-ticket-dest-symbol')
        etf_selector_selector.click()
        etf_selector_selector.send_keys(User_Key.ETFs[i])
        etf_selector_selector.send_keys(Keys.ENTER)
        # Buy button
        buy_button = driver.find_element(by=By.XPATH, value='//*[@id="action-buy"]/s-root/div/label').click()
        # Dollars button
        dollars_button = driver.find_element(by=By.XPATH, value='//*[@id="quantity-type-dollars"]/s-root/div/label').click()
        # Market button
        driver.find_element(by=By.XPATH, value='//*[@id="market-yes"]/s-root/div/label').click()

        # If statement to ensure that there is enough cash to make the next investment. If not, break from for loop
        next_investment = float(User_Key.ETF_Investments[i])
        if next_investment > account_balance:
            break
        else:
            account_balance -= next_investment
            print(account_balance)

        # Dollar Amount Input
        dollar_amount = driver.find_element(by=By.ID, value='eqt-shared-quantity')
        dollar_amount.send_keys(User_Key.ETF_Investments[i])
        time.sleep(2)
        # Preview Order Button
        driver.find_element(by=By.XPATH, value='//*[@id="previewOrderBtn"]').click()
        # Place Order Button
        driver.find_element(by=By.XPATH, value='//*[@id="placeOrderBtn"]').click()
        # Date and Time the "Place Order" Button is pressed
        time_purchased.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        time.sleep(2)

        # If statement determining whether to continue to the next investment or not
        if i != len(User_Key.ETFs)-1:
            # New Order Button
            driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__enter-new-order"]').click()
            time.sleep(2)
    return i


def email():
    
    global time_purchased
    global ERR
    global error_msg

    email_sender = User_Key.BotEmail_Username           # Bot email
    email_password = User_Key.BotEmail_Password         # Google App Password
    email_receiver = User_Key.User_Email                # Real Email that will be checked
    subject = 'Bot Purchase Report'                     # Email Subject
    if ERR == 0:
        # Email Body
        body = """  Starting Cash Balance = ${INIT_ACC_BAL} 
                    Cash Balance Left = ${ACC_BAL}
                    
                    Purchases:
                    {SEC1} for ${SEC1_INV} @ {TIME1}
                    {SEC2} for ${SEC2_INV} @ {TIME2}
                    {SEC3} for ${SEC3_INV} @ {TIME3}
                    {SEC4} for ${SEC4_INV} @ {TIME4}
                    Total Amount Purchased = ${MONEY_TRADED}
                    
                    ERRORS: {ERROR_MESSAGE}
                    
                    Next Purchases date ~ {TIME5}
        """.format(INIT_ACC_BAL=starting_balance, ACC_BAL=account_balance, SEC1=User_Key.ETFs[0], SEC2=User_Key.ETFs[1],
                   SEC3=User_Key.ETFs[2], SEC4=User_Key.ETFs[3], SEC1_INV=User_Key.ETF_Investments[0],
                   SEC2_INV=User_Key.ETF_Investments[1], SEC3_INV=User_Key.ETF_Investments[2], SEC4_INV=User_Key.ETF_Investments[3],
                   MONEY_TRADED=User_Key.total_purchases(User_Key.ETF_Investments), ERROR_MESSAGE=error_msg, TIME1=time_purchased[0],
                   TIME2=time_purchased[1], TIME3=time_purchased[2], TIME4=time_purchased[3],
                   TIME5=((datetime.now() + timedelta(days=7)).strftime("%m/%d/%Y %H:00:00")))
    else:
        body = """ ERROR RECEIVED, DO SOMETHING HERE """

    # Formatting Email
    mail = EmailMessage()
    mail['From'] = email_sender
    mail['To'] = email_receiver
    mail['subject'] = subject
    mail.set_content(body)

    # Logging in and Sending Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smpt:
        smpt.login(email_sender, email_password)
        smpt.sendmail(email_sender, email_receiver, mail.as_string())


# Function that logs in to Fidelity
fidelity_login()
# Function that loops to purchase the Securities
num_of_purchases = fidelity_security_purchasing()
num_of_purchases += 1




