# imported libraries


import User_Key
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import actions
from selenium.webdriver import ActionChains
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
action = ActionChains(driver)

# Initializing Global Variables
error_msg = 'No Errors'  # JUST A PLACE HOLDER CURRENTLY
account_balance = '0.00'
starting_balance = '0.00'
time_purchased = []
ERR = 0
i = 0

def fidelity_login():
    global error_msg
    # Initially getting this url to pick up cookies
    driver.get('https://www.fidelity.com/')
    time.sleep(2)  # WAIT ON HOME PAGE
    # Go to login page
    driver.get('https://digital.fidelity.com/prgw/digital/login/full-page')
    try:
        WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.ID, 'userId-input')))
        # Enter Username
        username_input_element = driver.find_element(by=By.ID, value="userId-input")
        username_input_element.click()
        username_input_element.send_keys(User_Key.User)
    except TimeoutException:
        error_msg = 'Could Not Log In'
        driver.close()
        return
    # Enter Password
    password_input_element = driver.find_element(by=By.ID, value="password")
    password_input_element.click()
    password_input_element.send_keys(User_Key.Password)
    # Send Enter After Password
    password_input_element.send_keys(Keys.ENTER)
    time.sleep(5)  # Wait for login to happen


def fidelity_security_purchasing():
    # Global variables
    global account_balance, i
    global starting_balance
    global time_purchased
    global ERR
    global error_msg

    # Go to 'trade' page
    driver.get('https://digital.fidelity.com/ftgw/digital/trade-equity/index/orderEntry')

    for i in range(0, len(User_Key.ETFs)):
        # Default Tade Option is 'Stocks/ETFs' and the whole point of this program is to buy ETFs so no need to change this

        # Selecting an Account
        try:
            WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dest-acct-dropdown"]')))
            driver.find_element(by=By.XPATH, value='//*[@id="dest-acct-dropdown"]').click()
            # Using a profile with only 1 account opened
            driver.find_element(by=By.ID, value='ett-acct-sel-list').click()
        except TimeoutException:
            error_msg = 'Could Not Find An Account'
            ERR = 1
            driver.close()
            return i

        # Finding Account Balance
        # Giving to collect the real time data once and subtract from
        if i == 0:
            try:
                WebDriverWait(driver, timeout=30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="eq-ticket__account-balance"]/div/div[2]/span')))
                account_balance = driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__account-balance"]/div/div[2]/span').text
                account_balance = float(account_balance[1:])  # Omitting the $ in the front of the text to convert string to a float
                starting_balance = account_balance
                print(account_balance)
            except TimeoutException:
                error_msg = 'Could Not Find an Account Balance'
                ERR = 1
                driver.close()
                return i

        # Selecting the ETF to be purchased (WRITE AS A RECURSIVE FUNCTION BASED OF DATA IN USER_KEY.py)
        try:
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.ID, 'eq-ticket-dest-symbol')))
            etf_selector_selector = driver.find_element(by=By.ID, value='eq-ticket-dest-symbol')
            etf_selector_selector.click()
            etf_selector_selector.send_keys(User_Key.ETFs[i])
            etf_selector_selector.send_keys(Keys.ENTER)
        except TimeoutException:
            error_msg = 'Could Not Select an ETF to buy Button'
            ERR = 1
            driver.close()
            return i

        # Buy button
        try:
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="action-buy"]/s-root/div/label')))
            driver.find_element(by=By.XPATH, value='//*[@id="action-buy"]/s-root/div/label').click()
        except TimeoutException:
            error_msg = 'Could Not Find Buy Button'
            ERR = 1
            driver.close()
            return i

        # Dollars button
        try:
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="quantity-type-dollars"]/s-root/div/label')))
            driver.find_element(by=By.XPATH, value='//*[@id="quantity-type-dollars"]/s-root/div/label').click()
        except TimeoutException:
            error_msg = 'Could Not Find Dollars Button'
            ERR = 1
            driver.close()
            return i

        # Market button
        try:
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="market-yes"]/s-root/div/label')))
            driver.find_element(by=By.XPATH, value='//*[@id="market-yes"]/s-root/div/label').click()
        except TimeoutException:
            error_msg = 'Could Not Find Dollars Button'
            ERR = 1
            driver.close()
            return i

        # If statement to ensure that there is enough cash to make the next investment. If not, break from for loop
        next_investment = float(User_Key.ETF_Investments[i])
        if next_investment > account_balance:
            break
        else:
            account_balance -= next_investment
            print(account_balance)

        # Dollar Amount Input
        try:
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.ID, 'eqt-shared-quantity')))
            dollar_amount = driver.find_element(by=By.ID, value='eqt-shared-quantity')
            dollar_amount.send_keys(User_Key.ETF_Investments[i])
        except TimeoutException:
            error_msg = 'Could Not Enter A Dollar Amount'
            ERR = 1
            driver.close()
            return i

        # Preview Order Button
        try:
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="previewOrderBtn"]')))
            preview_order_button = driver.find_element(by=By.XPATH, value='//*[@id="previewOrderBtn"]')
            action.double_click(on_element=preview_order_button).perform()
        except TimeoutException:
            error_msg = 'Could Not Find Preview Order Button'
            ERR = 1
            driver.close()
            return i

        # Place Order Button
        try:
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="placeOrderBtn"]')))
            driver.find_element(by=By.XPATH, value='//*[@id="placeOrderBtn"]').click()
        except TimeoutException:
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="previewOrderBtn"]')))
            action.double_click(on_element=preview_order_button).perform()
            WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="placeOrderBtn"]')))
            driver.find_element(by=By.XPATH, value='//*[@id="placeOrderBtn"]').click()
        except:
            error_msg = 'Could Not Find Place Order Button'
            ERR = 1
            driver.close()
            return i

        # Date and Time the "Place Order" Button is pressed
        time_purchased.append(datetime.now().strftime("%m/%d/%Y %H:%M:%S"))

        # If statement determining whether to continue to the next investment or not
        if i != len(User_Key.ETFs)-1:
            # New Order Button
            try:
                WebDriverWait(driver, timeout=30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="eq-ticket__enter-new-order"]')))
                driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__enter-new-order"]').click()
            except TimeoutException:
                error_msg = 'Could Not Find New Order Button'
                ERR = 1
                driver.close()
                return i
    return i


def email_purchases_creator(num_purchases):
    purchases = ""
    for i in range(0, num_purchases):
        purchase = "{SEC} for ${SEC_INV} @{TIME}\n".format(SEC=User_Key.ETFs[i], SEC_INV=User_Key.ETF_Investments[i], TIME=time_purchased[i])
        purchases += purchase
    purchases += "Total Amount Purchased = ${MONEY_TRADED}".format(MONEY_TRADED=User_Key.total_purchases(User_Key.ETF_Investments))
    return purchases


def email_error_msg_creator():
    global error_msg
    global ERR
    if ERR == 1:
        error_msg_body = """\n
                            THERE WAS AN ERROR RUNNING THE PROGRAM
                            Error Message: {ERR}""".format(ERR=error_msg)
    else:
        error_msg_body = """\n\nTHERE WAS NO ERROR"""
    return error_msg_body


def email(purchase_summary):
    
    global time_purchased
    global ERR
    global error_msg

    email_sender = User_Key.BotEmail_Username           # Bot email
    email_password = User_Key.BotEmail_Password         # Google App Password
    email_receiver = User_Key.User_Email                # Real Email that will be checked
    subject = 'Bot Purchase Report'                     # Email Subject

    # Email Body (EDIT IF NEEDED)
    body = """Starting Cash Balance = ${INIT_ACC_BAL}\nCash Balance Left = ${ACC_BAL}\n\nPurchases:\n{PURCHASES}\n\nNext Purchases date ~ {TIME}""".format(INIT_ACC_BAL=starting_balance, ACC_BAL=account_balance, PURCHASES=purchase_summary, TIME=((datetime.now() + timedelta(days=7)).strftime("%m/%d/%Y %H:00:00")))  # Default next purchase date in seven days. This can be changed. All depends on when you run script

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

# Functions that create the body of Email
purchase_sum = email_purchases_creator(num_of_purchases)
error_msg_sum = email_error_msg_creator()

purchase_sum += error_msg_sum

email(purchase_sum)
