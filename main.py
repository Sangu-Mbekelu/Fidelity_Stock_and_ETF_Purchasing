# imported libraries
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from undetected_chromedriver import ChromeOptions
import User_Key
import undetected_chromedriver as uc

# Defining the webdriver

opts = uc.ChromeOptions()
# Headless option for running without UI
# opts.add_argument('--headless')
driver = uc.Chrome(version_main=109)

driver.implicitly_wait(20)  # gives an implicit wait for 120 seconds for finding all elements


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
    # Go to 'trade' page
    driver.get('https://digital.fidelity.com/ftgw/digital/trade-equity/index/orderEntry')

    for i in range(0, len(User_Key.ETFs)):
        # Default Tade Option is 'Stocks/ETFs' and the whole point of this program is to buy ETFs so no need to change this
        # Selecting an Account
        account_selection = driver.find_element(by=By.XPATH, value='//*[@id="dest-acct-dropdown"]')
        account_selection.click()
        account_selection = driver.find_element(by=By.ID, value='ett-acct-sel-list')
        account_selection.click()

        # Finding Account Balance
        account_balance = '0.00'
        if i == 0:
            account_balance = driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__account-balance"]/div/div[2]/span').text
            account_balance = float(account_balance)
            print(account_balance)

        # Selecting the ETF to be purchased (WRITE AS A RECURSIVE FUNCTION BASED OF DATA IN USER_KEY.py)
        ETF_selector = driver.find_element(by=By.ID, value='eq-ticket-dest-symbol')
        ETF_selector.click()
        ETF_selector.send_keys(User_Key.ETFs[i])
        ETF_selector.send_keys(Keys.ENTER)
        # Buy button
        buy_button = driver.find_element(by=By.XPATH, value='//*[@id="action-buy"]/s-root/div/label')
        buy_button.click()
        # Dollars button
        dollars_button = driver.find_element(by=By.XPATH, value='//*[@id="quantity-type-dollars"]/s-root/div/label')
        dollars_button.click()
        # Market button
        market_button = driver.find_element(by=By.XPATH, value='//*[@id="market-yes"]/s-root/div/label')
        market_button.click()

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
        time.sleep(2)

        # If statement determining whether to continue to the next investment or not
        if i != len(User_Key.ETFs)-1:
            # New Order Button
            driver.find_element(by=By.XPATH, value='//*[@id="eq-ticket__enter-new-order"]').click()
            time.sleep(2)


# Initially getting this url to pick up cookies
driver.get('https://www.fidelity.com/')
# Function that logs in to Fidelity
fidelity_login()
# Function that loops to purchase the Securities
fidelity_security_purchasing()
