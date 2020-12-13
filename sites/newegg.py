
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager
from chromedriver_py import binary_path
from utils import random_delay, send_webhook, create_msg
from utils.selenium_utils import change_driver
import settings, time


class NewEgg:
    def __init__(self, task_id, status_signal, image_signal, product, profile, proxy, monitor_delay, error_delay):
        self.task_id, self.status_signal, self.image_signal, self.product, self.profile, self.monitor_delay, self.error_delay = task_id, status_signal, image_signal, product, profile, float(
            monitor_delay), float(error_delay)

        starting_msg = "Starting Newegg"
        self.browser = self.init_driver()
        self.product_image = None
        self.TIMEOUT_LONG = 20

        if settings.dont_buy:
            starting_msg = "Starting Newegg in dev mode; will not actually checkout"

        self.status_signal.emit(create_msg(starting_msg, "normal"))
        self.status_signal.emit(create_msg("Logging In..", "normal"))
        self.login()
        self.monitor()
        #self.atc()
        #self.checkout()
        #self.submit_billing()

        if not settings.dont_buy:
            self.submit_order()
            send_webhook("OP", "Newegg", self.profile["profile_name"], self.task_id, self.product_image)
        else:
            self.status_signal.emit(create_msg("Mock Order Placed", "success"))

    
    def init_driver(self):
        driver_manager = ChromeDriverManager()
        driver_manager.install()
        browser = webdriver.Chrome(binary_path)

        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                  Object.defineProperty(navigator, 'webdriver', {
                   get: () => undefined
                  })
                """
        })

        return browser

    def login(self):
        self.browser.get("https://newegg.com")
        wait(self.browser, self.TIMEOUT_LONG).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".nav-complex-title"))).click()
        wait(self.browser, self.TIMEOUT_LONG).until(EC.element_to_be_clickable((By.ID, "labeled-input-signEmail"))).send_keys(settings.bestbuy_user)
        wait(self.browser, self.TIMEOUT_LONG).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-orange"))).click()
        wait(self.browser, self.TIMEOUT_LONG).until(EC.element_to_be_clickable((By.ID, "labeled-input-password"))).send_keys(settings.bestbuy_pass)
        wait(self.browser, self.TIMEOUT_LONG).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-orange"))).click()
        time.sleep(random_delay(self.monitor_delay, settings.random_delay_start, settings.random_delay_stop))

    
    

    def monitor(self):
        img_found = False
        in_stock = False

        self.browser.get(self.product)
        wait(self.browser, self.TIMEOUT_LONG).until(lambda _: self.browser.current_url == self.product)

        while not img_found:
            try:
                if not img_found:
                    product_img = self.browser.find_elements_by_class_name('swiper-zoom-container')[0].find_element_by_tag_name("img")
                    print(product_img)
                    self.image_signal.emit(product_img.get_attribute("src"))
                    self.product_image = product_img.get_attribute("src")
                    img_found = True
            except Exception as e:
                continue

        while not in_stock:
            add_to_cart_btn = None
            if len(self.browser.find_elements_by_xpath('//button[@data-test= "orderPickupButton"]')) > 0:
                add_to_cart_btn = self.browser.find_element_by_xpath('//button[@data-test= "orderPickupButton"]')
            elif len(self.browser.find_elements_by_xpath('//button[@data-test= "shipItButton"]')) > 0:
                add_to_cart_btn = self.browser.find_element_by_xpath('//button[@data-test= "shipItButton"]')
            else:
                self.status_signal.emit(create_msg("Waiting on Restock", "normal"))
                time.sleep(random_delay(self.monitor_delay, settings.random_delay_start, settings.random_delay_stop))
                self.browser.refresh()
                continue
            self.browser.execute_script("return arguments[0].scrollIntoView(true);", add_to_cart_btn)
            add_to_cart_btn.click()
            in_stock = True
            self.status_signal.emit(create_msg("Added to cart", "normal"))


    def checkout(self):
        did_checkout = False
        self.status_signal.emit(create_msg("Checking out", "normal"))

        while not did_checkout:
            try:
                self.browser.find_element_by_xpath('//button[@data-test= "checkout-button"]').click()
                did_checkout = True
                time.sleep(random_delay(self.monitor_delay, settings.random_delay_start, settings.random_delay_stop))
            except:
                continue


    def submit_billing(self):
        added_cc = False
        added_cvv = False

        self.status_signal.emit(create_msg("Entering CC #", "normal"))

        while not added_cc:
            try:
                cc_input = self.browser.find_element_by_id("creditCardInput-cardNumber")
                cc_input.send_keys(self.profile["card_number"])
                if len(self.browser.find_elements_by_xpath('//button[@data-test= "verify-card-button"]')) > 0:
                    self.browser.find_element_by_xpath('//button[@data-test= "verify-card-button"]').click()
                added_cc = True
            except:
                self.status_signal.emit(create_msg("CC Verification not needed", "normal"))
                break

        while not added_cvv:
            try:
                cvv_input = self.browser.find_element_by_id("creditCardInput-cvv")
                self.status_signal.emit(create_msg("Entering CC Last 3", "normal"))
                cvv_input.send_keys(self.profile["card_cvv"])

                if len(self.browser.find_elements_by_xpath('//button[@data-test= "save-and-continue-button"]')) > 0:
                    self.browser.find_element_by_xpath('//button[@data-test= "save-and-continue-button"]').click()
                added_cvv = True
            except:
                self.status_signal.emit(create_msg("No need to enter last 3", "normal"))
                break

    def submit_order(self):
        did_submit = False

        self.status_signal.emit(create_msg("Submitting Order", "normal"))
        while not did_submit:
            try:
                if len(self.browser.find_elements_by_id('creditCardInput-cvv')) > 0:
                    self.browser.find_element_by_id('creditCardInput-cvv').send_keys(self.profile["card_cvv"])
                self.browser.find_element_by_xpath('//button[@data-test= "placeOrderButton"]').click()
                self.status_signal.emit(create_msg("Order Placed", "success"))
                send_webhook("OP", "Target", self.profile["profile_name"], self.task_id, self.product_image)
                did_submit = True
            except:
                continue
    

    '''
    def buy_device(url):
        self.browser.get(url)
        time.sleep(2)
        try:
            element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "popup-close")))
            element.click()
        except:
            pass
        time.sleep(1)
        driver.find_element_by_css_selector(".nav-complex-title").click()
        time.sleep(1)
        uname = driver.find_element_by_id("labeled-input-signEmail")
        uname.send_keys(username)
        time.sleep(.5)
        driver.find_element_by_css_selector(".btn-orange").click()
        time.sleep(.5)
        passwd = driver.find_element_by_id("labeled-input-password")
        passwd.send_keys(password)
        time.sleep(.5)
        driver.find_element_by_css_selector(".btn-orange").click()
        time.sleep(1)
        driver.get(url)
        time.sleep(1)
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-wide")))
        element.click()
        #drive.find_element_by_css_selector(".btn-wide").click()
        time.sleep(1)
        modal_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal-lg")))
        try:
            modal_element.find_element_by_xpath("//*[contains(text(), 'No, thanks')]").click()
        except:
            modal_element.find_element_by_css_selector(".btn-primary").click()
        time.sleep(1)
        modal_element.find_element_by_css_selector(".btn-primary").click()
        time.sleep(1)
        driver.find_element_by_css_selector(".btn-wide").click()
        time.sleep(1)
        summary_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".checkout-step-action")))
        element = summary_element.find_element_by_xpath("//*[contains(text(), 'Continue to payment')]")
        driver.execute_script("arguments[0].click();", element) 
        time.sleep(1)
        cvv_element=driver.find_element_by_css_selector(".mask-cvv-4")
        driver.execute_script("arguments[0].scrollIntoView();", cvv_element)
        time.sleep(1)
        cvv_element.click()
        cvv_element.send_keys(cvv_code)
        time.sleep(1)
        checkout_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".checkout-step-action-done")))
        element = checkout_element.find_element_by_xpath("//*[contains(text(), 'Review your order')]")    
        driver.execute_script("arguments[0].click();", element)
        time.sleep(1)
        driver.find_element_by_id("btnCreditCard").click()

        time.sleep(50)
        
        service.stop()
        '''