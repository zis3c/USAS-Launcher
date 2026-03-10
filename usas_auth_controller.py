import os
import time
from dotenv import load_dotenv, set_key
import keyring
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

try:
    import colorama
    from colorama import init, Fore, Style
    init(autoreset=True)
    def print_info(msg): print(f"{Fore.BLUE}[*] {Style.RESET_ALL}{msg}")
    def print_success(msg): print(f"{Fore.GREEN}[+] {Style.RESET_ALL}{msg}")
    def print_warn(msg): print(f"{Fore.YELLOW}[!] {Style.RESET_ALL}{msg}")
    def print_err(msg): print(f"{Fore.RED}[X] {Style.RESET_ALL}{msg}")
    def print_prompt(msg): print(f"{Fore.YELLOW}[>] {Style.RESET_ALL}{msg}")
except ImportError:
    def print_info(msg): print(f"[*] {msg}")
    def print_success(msg): print(f"[+] {msg}")
    def print_warn(msg): print(f"[!] {msg}")
    def print_err(msg): print(f"[X] {msg}")
    def print_prompt(msg): print(f"[>] {msg}")

try:
    import pwinput
    def get_password(prompt): return pwinput.pwinput(prompt, mask='*')
except ImportError:
    import getpass
    def get_password(prompt): return getpass.getpass(prompt)

# --- Configuration Setup ---
ENV_FILE = '.env'
APP_NAME = 'USAS_Launcher'

def setup_credentials():
    """Check for credentials in .env and keyring, prompt if missing."""
    load_dotenv(ENV_FILE)
    
    # Check if IDs exist in .env and passwords exist in keyring
    wifi_id = os.getenv('WIFI_ID')
    lms_id = os.getenv('LMS_ID')
    vcampus_id = os.getenv('VCAMPUS_ID')
    
    wifi_pass = keyring.get_password(APP_NAME, 'WIFI_PASS')
    lms_pass = keyring.get_password(APP_NAME, 'LMS_PASS')
    vcampus_pass = keyring.get_password(APP_NAME, 'VCAMPUS_PASS')

    if not all([wifi_id, lms_id, vcampus_id, wifi_pass, lms_pass, vcampus_pass]):
        print_prompt("First time setup or credentials missing.")
        time.sleep(0.5)
        print_prompt("Please enter your credentials for each platform.")
        time.sleep(0.5)
        print_prompt("IDs will be saved in .env, Passwords will be saved securely in Windows Credential Manager.\n")
        time.sleep(0.5)
        
        wifi_id = input(f"{Fore.CYAN}WiFi / Captive Portal ID:{Style.RESET_ALL} ").strip()
        wifi_pass = get_password(f"{Fore.CYAN}WiFi / Captive Portal Password:{Style.RESET_ALL} ").strip()
        
        print("\n")
        lms_id = input(f"{Fore.CYAN}LMS ID:{Style.RESET_ALL} ").strip()
        lms_pass = get_password(f"{Fore.CYAN}LMS Password:{Style.RESET_ALL} ").strip()
        
        print("\n")
        vcampus_id = input(f"{Fore.CYAN}VCampus ID:{Style.RESET_ALL} ").strip()
        vcampus_pass = get_password(f"{Fore.CYAN}VCampus Password:{Style.RESET_ALL} ").strip()
        
        # Create .env and set ID keys
        with open(ENV_FILE, 'w') as f:
            pass # Create empty file
            
        set_key(ENV_FILE, 'WIFI_ID', wifi_id)
        set_key(ENV_FILE, 'LMS_ID', lms_id)
        set_key(ENV_FILE, 'VCAMPUS_ID', vcampus_id)
        
        # Save passwords securely in keyring
        if wifi_pass: keyring.set_password(APP_NAME, 'WIFI_PASS', wifi_pass)
        if lms_pass: keyring.set_password(APP_NAME, 'LMS_PASS', lms_pass)
        if vcampus_pass: keyring.set_password(APP_NAME, 'VCAMPUS_PASS', vcampus_pass)
        
        print_success("Credentials saved securely!\n")
    
    load_dotenv(ENV_FILE)
    creds = {
        'wifi': (os.getenv('WIFI_ID'), keyring.get_password(APP_NAME, 'WIFI_PASS')),
        'lms': (os.getenv('LMS_ID'), keyring.get_password(APP_NAME, 'LMS_PASS')),
        'vcampus': (os.getenv('VCAMPUS_ID'), keyring.get_password(APP_NAME, 'VCAMPUS_PASS'))
    }
    
    # Simple validation to ensure none of them returned None
    flattened_creds = [item for tuple_pair in creds.values() for item in tuple_pair]
    if not all(flattened_creds):
         raise ValueError("Some credentials are missing. Please check your .env file or delete it to set it up again.")
         
    return creds

# --- Browser Automation ---
def setup_browser():
    """Initialize Chrome webdriver with detach to keep browser open."""
    chrome_options = webdriver.ChromeOptions()
    # "detach" keeps Chrome open after the script ends
    chrome_options.add_experimental_option("detach", True)
    
    # "eager" means WebDriver will interact as soon as the DOM is ready, 
    # without waiting for heavy external images, scripts, or CSS.
    chrome_options.page_load_strategy = 'eager'
    
    # Stability and security flags to prevent the driver from crashing/resetting on the university network
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--ignore-certificate-errors")
    
    # Suppress verbose terminal logs from Selenium/webdriver manager
    chrome_options.add_argument("--log-level=3") 
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Isolate Chrome's driver process entirely from the Command Prompt window
    # so the terminal doesn't hang waiting for the browser to be closed.
    import subprocess
    service = Service()
    service.creation_flags = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
    
    # Selenium 4.6+ has a built-in Selenium Manager that automatically handles drivers
    # Defaulting back to standard ephemeral Chrome profiles to prevent locking and freezing
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Wait up to 10 seconds for elements to appear before throwing error
    driver.implicitly_wait(10) 
    return driver

def login_generic(driver, url, username, password, step_name):
    """Generic attempt to fill login forms using common standard element names/ids."""
    print_info(f"[{step_name}] Navigating to: {url}")
    try:
        if len(driver.window_handles) > 0 and driver.current_url == "data:,":
            # Very first launch, use existing open empty tab
            driver.get(url)
        else:
            # Need to open a new tab
            driver.execute_script(f"window.open('{url}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])

        # Wait a moment for page to load visually
        time.sleep(2)
        
        # Check if we are ALREADY logged in (specifically for the Mikrotik captive portal)
        # The user provided HTML showing a "log off" submit button and a "status refresh" text
        if "log off" in driver.page_source.lower() and "status refresh" in driver.page_source.lower():
             print_success(f"[{step_name}] Already connected/logged in!")
             try:
                 # Click 'Continue to use Internet' button
                 continue_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Continue to use Internet')]")
                 continue_btn.click()
                 time.sleep(1) # Brief pause for it to process
                 
                 # IMPORTANT: If we close the ONLY tab in Chrome, Selenium terminates the whole scraping session.
                 # So we need to open a dummy blank tab first, switch to it, then close the captive portal tab.
                 if len(driver.window_handles) == 1:
                     driver.execute_script("window.open('');")
                 
                 # Close the captive portal tab
                 driver.close()
                 
                 # Switch focus to the remaining tab so Selenium can continue
                 driver.switch_to.window(driver.window_handles[-1])
             except NoSuchElementException:
                 pass
             return

        # Attempt to find the username field
        # We look for common names/ids corresponding to standard HTML login forms
        username_field = None
        for selector in ['username', 'email', 'login', 'userid', 'login_username']:
            try:
                username_field = driver.find_element(By.NAME, selector)
                break
            except NoSuchElementException:
                try:
                    username_field = driver.find_element(By.ID, selector)
                    break
                except NoSuchElementException:
                    continue
        
        # Attempt to find password field (easier since it's almost always type='password' or name='password')
        password_field = None
        for selector in ['password', 'pass', 'login_password', 'pwd']:
            try:
                password_field = driver.find_element(By.NAME, selector)
                break
            except NoSuchElementException:
                try:
                    password_field = driver.find_element(By.ID, selector)
                    break
                except NoSuchElementException:
                    try:
                        password_field = driver.find_element(By.XPATH, "//input[@type='password']")
                        break
                    except NoSuchElementException:
                         continue
                         
        # Attempt to find a submit button
        submit_button = None
        # Often buttons are input type='submit', or button type='submit', or have words like Login/Submit
        try:
             submit_button = driver.find_element(By.XPATH, "//button[@type='submit' or contains(translate(text(), 'LOGIN', 'login'), 'login') or contains(translate(text(), 'SUBMIT', 'submit'), 'submit')]")
        except NoSuchElementException:
             try:
                 submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
             except NoSuchElementException:
                 pass # We'll just press Enter instead

        if username_field and password_field:
            print_info(f"[{step_name}] Filling credentials...")
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)
            
            # Submit the form
            time.sleep(1) # Brief pause like a human
            if submit_button:
                 submit_button.click()
            else:
                 # If no button found, try hitting enter on the password field
                 password_field.submit()
            
            print_success(f"[{step_name}] Login submitted!")
        else:
            print_warn(f"[{step_name}] Warning: Could not automatically detect standard login fields.")
            print_warn("Please perform login manual for this tab, or inspect the input names to improve this script.")
            
    except Exception as e:
        print_err(f"[{step_name}] Error during automation: {e}")

def login_vcampus(driver, url, username, password):
    print_info(f"[VCampus] Navigating to: {url}")
    try:
        driver.execute_script(f"window.open('{url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        
        # Use implicitly_wait defined globally instead of explicit arbitrary time sleeps
        uname_field = driver.find_element(By.ID, "username")
        pass_field = driver.find_element(By.ID, "password")
        submit_btn = driver.find_element(By.ID, "btnLogin")
        
        print_info("[VCampus] Filling credentials...")
        uname_field.clear()
        uname_field.send_keys(username)
        pass_field.clear()
        pass_field.send_keys(password)
        submit_btn.click()
        
        print_info("[VCampus] Waiting for Student Portal authentication...")
        try:
            # Wait for the AJAX login to complete and the menu to become fully visible
            portal1_btn = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@onClick=\"document.forms['form-student1'].submit();\"]"))
            )
            # Add a short delay to ensure the AJAX callback finishes populating the hidden credentials
            time.sleep(0.5)
            portal1_btn.click()
            print_success("[VCampus] Portal Pelajar 1 selected and logged in!")
        except TimeoutException:
            print_warn("[VCampus] Warning: Could not find Portal Pelajar 1 button after login. You may need to click it manually.")

    except Exception as e:
        print_err(f"[VCampus] Error during automation: {e}")

def login_lms(driver, url, username, password):
    print_info(f"[LMS] Navigating to: {url}")
    try:
        driver.execute_script(f"window.open('{url}', '_blank');")
        driver.switch_to.window(driver.window_handles[-1])
        
        uname_field = driver.find_element(By.ID, "username")
        pass_field = driver.find_element(By.ID, "password")
        submit_btn = driver.find_element(By.ID, "loginbtn")
        
        print_info("[LMS] Filling credentials...")
        uname_field.clear()
        uname_field.send_keys(username)
        pass_field.clear()
        pass_field.send_keys(password)
        submit_btn.click()
        print_success("[LMS] Login submitted!")
    except Exception as e:
        print_err(f"[LMS] Error during automation: {e}")

def main():
    print_info("=== USAS Workspace Launcher Started ===")
    try:
        creds = setup_credentials()
        driver = setup_browser()
        
        # Step 1: Captive Portal
        login_generic(driver, "http://wifi.usas/login", creds['wifi'][0], creds['wifi'][1], "Captive Portal")
        
        # Step 2: LMS
        login_lms(driver, "https://lms.usas.edu.my/my/", creds['lms'][0], creds['lms'][1])
        
        # Step 3: VCampus
        login_vcampus(driver, "http://vcampus.usas.edu.my/", creds['vcampus'][0], creds['vcampus'][1])
        
        # Step 4: Additional Study Tools
        print_info("[ChatGPT] Navigating to: https://chatgpt.com/")
        driver.execute_script("window.open('https://chatgpt.com/', '_blank');")
        
        # Cleanup: Close the temporary "about:blank" dummy tab if it exists
        # We loop through all window handles in reverse to find and close it safely
        handles = driver.window_handles
        for handle in handles:
            driver.switch_to.window(handle)
            if driver.current_url == "about:blank":
                driver.close()
                break # Only close one dummy tab
        
        # Switch focus back to whatever the right-most tab is now
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[-1])
        
        print_success("\n=== Automation Complete ===")
        print_info("Browser tabs have been opened. You may close this terminal window.")
        
    except Exception as e:
        print_err(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
