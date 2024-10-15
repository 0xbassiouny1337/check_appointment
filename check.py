from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import re
import random 



# Initialize WebDriver
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
wait = WebDriverWait(driver, 20)


def restart_driver():
    global driver
    if driver is not None:
        driver.quit()
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    return driver    


# Helper function to introduce random sleep intervals
def random_sleep(min_seconds, max_seconds):
    sleep_time = random.uniform(min_seconds, max_seconds)
    print(f"Sleeping for {sleep_time:.2f} seconds...")
    time.sleep(sleep_time)


def login(email,password):
    # Navigate to the login page
    driver.get("https://egyiam.almaviva-visa.it/realms/oauth2-visaSystem-realm-pkce/protocol/openid-connect/auth?response_type=code&client_id=aa-visasys-public&state=UHNJNFBKN1kxQnB4c1JzODhVS2tmdTJwR3d2ckpjfndLX19pSDc4T0V0UVVD&redirect_uri=https%3A%2F%2Fegy.almaviva-visa.it%2F&scope=openid%20profile%20email&code_challenge=wgRUk0VhaFjDb66rcolSIpVDtyZyfDxyg2MXe4zTZ-0&code_challenge_method=S256&nonce=UHNJNFBKN1kxQnB4c1JzODhVS2tmdTJwR3d2ckpjfndLX19pSDc4T0V0UVVD")

    # Wait for the page to load
    time.sleep(5)

    # Locate the username and password fields and log in
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")

    username_field.send_keys(email)  # Replace with your email
    password_field.send_keys(password)  # Replace with your password

    # Click the login button
    login_button = driver.find_element(By.ID, "kc-login")
    login_button.click()

    # Wait for the next page to load
    time.sleep(5)

def check_login():
    # Get the current URL after attempting to log in
    current_url = driver.current_url

    # Check if the URL is the expected homepage
    if current_url == "https://egy.almaviva-visa.it/":
        print("Login successful!")
        return True
    else:
        # Check for a message indicating that the login attempt has expired
        page_source = driver.page_source
        if re.search(r'login attempt expired|session timed out', page_source, re.IGNORECASE):
            print("Login attempt expired. Retrying...")
            return False
        else:
            print("Login failed. Check your credentials.")

            return False


def select_center(center_name):
    try:
        select_center_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-0")))
        driver.execute_script("arguments[0].scrollIntoView();", select_center_dropdown)
        select_center_dropdown.click()
        center_option = wait.until(EC.visibility_of_element_located((By.XPATH, f"//mat-option/span[text()='{center_name}']")))
        center_option.click()
        print(f"Selected center: {center_name}")
    except Exception as e:
        print(f"An error occurred while selecting the center: {e}")

def select_service_level(service_level_name):
    try:
        service_level_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-4")))
        driver.execute_script("arguments[0].scrollIntoView();", service_level_dropdown)
        service_level_dropdown.click()
        service_level_option = wait.until(EC.visibility_of_element_located((By.XPATH, f"//mat-option/span[text()='{service_level_name}']")))
        service_level_option.click()
        print(f"Selected service level: {service_level_name}")
    except Exception as e:
        print(f"An error occurred while selecting the service level: {e}")

def select_visa_type(visa_type_name):
    try:
        visa_type_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-2")))
        driver.execute_script("arguments[0].scrollIntoView();", visa_type_dropdown)
        visa_type_dropdown.click()
        visa_type_option = wait.until(EC.visibility_of_element_located((By.XPATH, f"//mat-option/span[text()='{visa_type_name}']")))
        visa_type_option.click()
        print(f"Selected visa type: {visa_type_name}")
    except Exception as e:
        print(f"An error occurred while selecting the visa type: {e}")



def select_trip_date(date):
    try:
        trip_date_input = wait.until(EC.element_to_be_clickable((By.ID, "pickerInput")))

        # Optionally, remove the readonly attribute if it's preventing interaction
        driver.execute_script("arguments[0].removeAttribute('readonly')", trip_date_input)

        # Send the date in the desired format
        trip_date_input.clear()
        trip_date_input.send_keys(date)

    except Exception as e:
        print(f"An error occurred: {e}")

def select_destination(des):
    try:
        destination_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@formcontrolname='tripDestination']")))

        # Send the destination text
        destination_input.clear()  # Clear the field if there's any pre-filled text
        destination_input.send_keys(des)  # Replace 'Rome' with the actual destination
    except Exception as e:
        print(f"An error occurred: {e}")

def handle_checkboxes():
    try:
        checkbox1 = wait.until(
            EC.presence_of_element_located((By.ID, "mat-mdc-checkbox-1-input"))
        )
        if checkbox1.get_attribute("aria-checked") == "false":
            checkbox1.click()
            print("First checkbox checked.")
        else:
            print("First checkbox already checked.")
    except Exception as e:
        print(f"An error occurred with the first checkbox: {e}")

    try:
        checkbox2 = wait.until(
            EC.presence_of_element_located((By.ID, "mat-mdc-checkbox-2-input"))
        )
        if checkbox2.get_attribute("aria-checked") == "false":
            checkbox2.click()
            print("Second checkbox checked.")
        else:
            print("Second checkbox already checked.")
    except Exception as e:
        print(f"An error occurred with the second checkbox: {e}")

def check_availability():
    while True:
        try:

            # Wait for the "Check Availability" button and click it
            check_availability_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'visasys-button') and contains(text(), 'Check availability')]"))
            )
            check_availability_button.click()
            print("Check Availability button clicked successfully!")

            # Wait for the results to load and determine the status
            random_sleep(4,6)  # Adjust this time as needed to ensure the page has loaded

            # Check for the presence of "No appointments" message
            no_appointments_message = driver.find_elements(By.XPATH, "//p[contains(text(), 'No appointments for this number of persons')]")

            if no_appointments_message:
                print("No appointments available. Clicking OK button and retrying...")
                ok_button = driver.find_element(By.XPATH, "//button[contains(@class, 'text-white') and contains(text(), 'OK')]")
                ok_button.click()
                print("OK button clicked.")
                random_sleep(70, 202)
            else:
                # If "Appointments available" message is found
                proceed_button = driver.find_element(By.XPATH, "//button[contains(@class, 'text-white') and contains(text(), 'Proceed with appointment')]")
                proceed_button.click()
                print("Appointments available. Proceed button clicked.")
                break  # Exit the loop as appointments are available and proceed button is clicked.

        except Exception as e:
            print(f"An error occurred while checking availability: {e}")
            random_sleep(60, 199)

def click_appointment():
    try:
        # Locate the <div> element with the specific text content and click it
        appointment_div = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, 'flex') and contains(@class, 'items-center') and contains(@class, 'bg-hue') and contains(@class, 'text-white')]")
            )
        )
        appointment_div.click()
        print("Appointment div clicked successfully!")
    except Exception as e:
        print(f"An error occurred while clicking the appointment div: {e}")



def set_birth_date(date_str):
    try:
        birth_date_input = wait.until(EC.element_to_be_clickable((By.ID, "mat-input-1")))
        driver.execute_script("arguments[0].removeAttribute('readonly')", birth_date_input)
        birth_date_input.clear()
        birth_date_input.send_keys(date_str)
        print(f"Birth date set to: {date_str}")
    except Exception as e:
        print(f"An error occurred while setting the birth date: {e}")

def set_gender(gender):
    try:
        gender_dropdown = wait.until(EC.element_to_be_clickable((By.ID, "mat-select-value-7")))
        gender_dropdown.click()
        gender_option = wait.until(EC.visibility_of_element_located((By.XPATH, f"//mat-option/span[text()='{gender}']")))
        gender_option.click()
        print(f"Gender set to: {gender}")
    except Exception as e:
        print(f"An error occurred while setting the gender: {e}")

def set_residence(residence_address):
    try:
        residence_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@formcontrolname='residenceAddress']")))
        residence_input.clear()
        residence_input.send_keys(residence_address)
        print(f"Residence set to: {residence_address}")
    except Exception as e:
        print(f"An error occurred while setting the residence address: {e}")

def set_passport_number(passport_number):
    try:
        passport_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@formcontrolname='number']")))
        passport_input.clear()
        passport_input.send_keys(passport_number)
        print(f"Passport number set to: {passport_number}")
    except Exception as e:
        print(f"An error occurred while setting the passport number: {e}")

def set_issue_date(issue_date_str):
    try:
        issue_date_input = wait.until(EC.element_to_be_clickable((By.ID, "mat-input-2")))
        driver.execute_script("arguments[0].removeAttribute('readonly')", issue_date_input)
        issue_date_input.clear()
        issue_date_input.send_keys(issue_date_str)
        print(f"Issue date set to: {issue_date_str}")
    except Exception as e:
        print(f"An error occurred while setting the issue date: {e}")



def set_expiration_date(expiration_date_str):
    try:
        expiration_date_input = wait.until(EC.element_to_be_clickable((By.ID, "mat-input-3")))
        driver.execute_script("arguments[0].removeAttribute('readonly')", expiration_date_input)
        expiration_date_input.clear()
        expiration_date_input.send_keys(expiration_date_str)
        print(f"Expiration date set to: {expiration_date_str}")
    except Exception as e:
        print(f"An error occurred while setting the expiration date: {e}")


def fill_form(birth_date_input, gender_input, residence, passport_number, issue_date, expiration_date):
    set_birth_date(birth_date_input)
    set_gender(gender_input)
    set_residence(residence)
    set_passport_number(passport_number)
    set_issue_date(issue_date)
    set_expiration_date(expiration_date)

def upload_file(file_path):
    try:

        

        # Wait for the file input element to be present in the DOM
        file_input = wait.until(EC.presence_of_element_located((By.ID, "100")))
        
        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", file_input)
        
        # Send the file path to the file input element
        file_input.send_keys(file_path)
        
        print(f"File uploaded successfully: {file_path}")

        time.sleep(20)
        # Wait for the submit button with the text 'SUBMIT' to be clickable and click it
        submit_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='SUBMIT']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        submit_button.click()
        
        print("Form submitted successfully.")



    except Exception as e:
        print(f"An error occurred while uploading the file: {e}")


def OTP():
    try:
        # Debugging: print a message to indicate the start of the function
        print("Starting OTP function...")
        
        otp_button = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@dir='ltr']//button[@class='visasys-button w-72 lg:w-64 xl:w-72 mt-6']"))
        )        
        print("OTP button found and clickable.")
        
        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", otp_button)
        print("Scrolled into view of the OTP button.")
        
        # Optional: Wait a moment to ensure the button is fully rendered
        driver.implicitly_wait(1)  # Wait for 1 second (adjust as needed)
        
        # Click the OTP button
        otp_button.click()
        print("OTP button clicked.")
        
        print("OTP button clicked successfully.")

        Request_OTP = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@class='visasys-button w-72' and normalize-space(text())='Request OTP code']")))
        Request_OTP.click()
        print("OTP button requested successfully.")




    
    except Exception as e:
        # Provide detailed information in case of an error
        print(f"An error occurred while clicking the OTP button: {e}")
        print("Make sure the button text and XPath are correct, and that the button is visible and enabled.")

        


def first_page(email,password,center,service_level,visa_type,trip_date,destination):

    login_successful = False
    while not login_successful:
        login(email,password)
        login_successful = check_login()

    # Proceed to the appointment page if login is successful
    if login_successful:
        print("Proceeding to the appointment page...")

        while True:
            random_sleep(1,3)
            driver.get("https://egy.almaviva-visa.it/appointment")
            random_sleep(4,15)

            if driver.current_url == "https://egy.almaviva-visa.it/appointment":
                print("Successfully reached the appointment page!")
                break
            else:
                print("Redirected away from the appointment page. Retrying...")

    
        # Perform the rest of the setup and form filling
        select_center(center)
        time.sleep(1.5)

        select_service_level(service_level)
        
        time.sleep(1.2)
        

        select_visa_type(visa_type)
        #select_visa_type("Employment Visa (D)")
        
        time.sleep(1.9)
        
        select_trip_date(trip_date)
        
        time.sleep(0.8)
        
        select_destination(destination)
        
        time.sleep(0.4)
        
        handle_checkboxes()
        
        random_sleep(1,3)
        
        check_availability()    
        
        click_appointment()

        random_sleep(1,3)
    else:
        print("Unable to proceed. Login failed.")    
            

def second_page(birth_date,gender,residence,passport_no,issue_date,expiration_date,file):
    fill_form(birth_date,gender,residence,passport_no,issue_date,expiration_date)

    time.sleep(4)
    print(file)

    upload_file(file)
    time.sleep(5)

    OTP()









    






