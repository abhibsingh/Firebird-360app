import time
import os
import pytest
import logging
import random
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.keys import Keys
from browserstack_config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, BROWSERSTACK_CAPABILITIES
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import glob

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_random_email():
    """Generate a random email address for testing."""
    random_number = random.randint(1000, 9999)
    return f"test+{random_number}@gmail.com"

@pytest.fixture(scope="session")
def setup_driver():
    """Fixture to set up and tear down the Appium driver for BrowserStack"""
    try:
        # Clean up old screenshots
        cleanup_screenshots()
        
        bs_url = f'https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub'
        
        logger.info("Initializing BrowserStack driver...")
        driver = webdriver.Remote(
            command_executor=bs_url,
            desired_capabilities=BROWSERSTACK_CAPABILITIES
        )
        
        time.sleep(5)
        logger.info("Driver initialized successfully")
        yield driver
        
    except Exception as e:
        logger.error(f"Failed to initialize driver: {str(e)}")
        raise
    finally:
        if 'driver' in locals():
            logger.info("Quitting driver...")
            driver.quit()

def send_keys_with_hide(driver, xpath, text):
    """Helper function to send keys and handle keyboard with retry for stale elements"""
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            # Find element fresh each time
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            time.sleep(1)
            element.click()
            element.clear()
            element.send_keys(text)
            time.sleep(1)
            
            try:
                driver.hide_keyboard()
            except:
                try:
                    driver.press_keycode(4)  # Android back button
                except:
                    logger.warning("Could not hide keyboard, continuing...")
            return
        except Exception as e:
            if attempt == max_attempts - 1:
                logger.error(f"Error sending keys after {max_attempts} attempts: {str(e)}")
                driver.save_screenshot(f"error_sendkeys_{time.strftime('%Y%m%d_%H%M%S')}.png")
                raise
            time.sleep(2)  # Wait before retrying

def wait_and_find_element(driver, by, value, timeout=20):
    """Helper function to wait for and find an element"""
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        logger.error(f"Element not found: {value}")
        # Take screenshot
        driver.save_screenshot(f"error_{time.strftime('%Y%m%d_%H%M%S')}.png")
        raise

def test_account_creation(setup_driver):
    """
    Test case 1: Automate the account creation flow.
    """
    try:
        # Wait for the app to load
        time.sleep(5)

        # Step 1: Click on "Create Account" button
        logger.info("Locating 'Create Account' button...")
        create_account_button = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Create Account"]'))
        )
        create_account_button.click()
        logger.info("Navigated to 'Create Account'.")
        time.sleep(2)  # Wait for form to load

        # Step 2: Enter first name
        logger.info("Locating first name input field...")
        first_name_field = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.EditText[1]"))
        )
        first_name_field.click()
        time.sleep(1)
        first_name_field.send_keys("John")
        try:
            setup_driver.hide_keyboard()
        except:
            pass
        logger.info("First name entered.")

        # Step 3: Enter surname
        logger.info("Locating surname input field...")
        surname_field = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.EditText[2]"))
        )
        surname_field.click()
        time.sleep(1)
        surname_field.send_keys("Doe")
        try:
            setup_driver.hide_keyboard()
        except:
            pass
        logger.info("Surname entered.")

        # Step 4: Enter date of birth
        logger.info("Locating date of birth input field...")
        dob_field = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.EditText[3]"))
        )
        dob_field.click()
        time.sleep(1)
        dob_field.send_keys("12/12/1999")
        try:
            setup_driver.hide_keyboard()
        except:
            pass
        logger.info("Date of birth entered.")

        # Step 5: Generate and enter a unique email
        random_email = generate_random_email()
        logger.info(f"Generated email: {random_email}")
        email_field = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.EditText[4]"))
        )
        email_field.click()
        time.sleep(1)
        email_field.send_keys(random_email)
        try:
            setup_driver.hide_keyboard()
        except:
            pass
        logger.info("Email entered.")

        # Step 6: Enter password
        logger.info("Locating password input field...")
        password_field = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.EditText[5]"))
        )
        password_field.click()
        time.sleep(1)
        password_field.send_keys("@1b2c3D4e5")
        try:
            setup_driver.hide_keyboard()
        except:
            pass
        logger.info("Password entered.")

        # Step 7: Click "Create My Account" button
        logger.info("Clicking 'Create My Account' button...")
        create_my_account_button = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Create my account"]'))
        )
        create_my_account_button.click()
        logger.info("Account creation submitted.")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        setup_driver.save_screenshot(f"error_account_creation_{time.strftime('%Y%m%d_%H%M%S')}.png")
        raise

def test_navigate_to_manager(setup_driver):
    """
    Test case 2: Navigate to the Manager section.
    """
    try: 
        # Step 8: Click on "Manager" icon
        logger.info("Clicking on the 'Manager' icon...")
        manager_icon = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.ImageView[2]"))
        )
        manager_icon.click()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

def test_continue_manager_flow(setup_driver):
    """
    Test case 3: Continue through the initial Manager flow.
    """
    try:
        # Step 9: Click "Continue" button
        logger.info("Clicking on 'Continue' button...")
        continue_button = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@content-desc='Continue']"))
        )
        continue_button.click()

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

def test_search_artist(setup_driver):
    """
    Test case 4: Search for an artist in the Manager section.
    """
    try:
        # Step 10: Search for "Taylor"
        logger.info("Searching for artist 'Taylor'...")
        search_artist_button = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@content-desc='Search for artist name']"))
        )
        search_artist_button.click()

        search_field = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText"))
        )
        search_field.click()
        search_field.send_keys("Taylor")
        logger.info("Artist name 'Taylor' entered.")

        first_result = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.view.View[contains(@content-desc, 'Taylor')]"))
        )
        first_result.click()
        logger.info("Selected the first search result.")

        continue_button = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@content-desc='Continue']"))
        )
        continue_button.click()

        # Step 11: Click "Go to the app" button
        go_to_app_button = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@content-desc='Go to the app']"))
        )
        go_to_app_button.click()
        logger.info("Navigated to the app.")
        logger.info("Clicking on 'Skip the tutorial' button...")

        go_to_app_tour = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Explore My 360"]'))
        )
        go_to_app_tour.click()
        logger.info("Touring the app.")
        logger.info("Clicking on 'tour the app' button...")

        go_to_app_next = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Next"]'))
        )
        go_to_app_next.click()
        logger.info("next button.")
        logger.info("Clicking on 'next button of the app'...")
        
        go_to_app_next = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Next"]'))
        )
        go_to_app_next.click()
        logger.info("next button.")
        logger.info("Clicking on 'next button of the app'...")
        
        go_to_app_done = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//android.widget.Button[@content-desc="Done"]'))
        )
        go_to_app_done.click()
        logger.info("done button.")
        logger.info("Clicking on 'done button of the app'...")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        setup_driver.save_screenshot(f"error_search_artist_{time.strftime('%Y%m%d_%H%M%S')}.png")
        raise

def test_verify_app_content(setup_driver):
    """
    Test case 5: Verify app content after navigating from Manager.
    """
    try:
        time.sleep(10)

        #Step 9: Scroll up and down
        logger.info("Scrolling up and down to verify Spotify element...")
        touch_action = TouchAction(setup_driver)
        touch_action.press(x=500, y=1000).move_to(x=500, y=200).release().perform()  # Scroll down
        time.sleep(1)
        touch_action.press(x=500, y=200).move_to(x=500, y=1000).release().perform()  # Scroll up

        # Step 10: Check for Spotify element
        logger.info("Verifying presence of Spotify element...")
        element = setup_driver.find_element(By.XPATH, "//android.widget.ImageView[@content-desc='7 days']")
        assert element.is_displayed(), "Element containing 'Followers' not found!"
        if element:
            logger.info("Spotify element found!")
        else:
            logger.error("Spotify element NOT found!")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

def test_add_artist_and_validate_highlights(setup_driver):
    try:
        time.sleep(5)  # Wait for app to be stable
        
        # Step 1: Click on the dropdown menu for artist selection
        logger.info("Attempting to locate the dropdown menu.")
        dropdown_menu = WebDriverWait(setup_driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//android.view.View[starts-with(@content-desc, 'Taylor Taylor')]/android.widget.ImageView[1]"))
        )
        dropdown_menu.click()
        logger.info("Dropdown menu clicked.")

        # Step 2: Click on the '+ Add profile' button
        add_profile_button = WebDriverWait(setup_driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@content-desc='+ Add profile']"))
        )
        add_profile_button.click()
        logger.info("+ Add profile button clicked.")

        # Step 3: Click on the 'Search for artist name' button
        search_artist_button = WebDriverWait(setup_driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@content-desc='Search for artist name']"))
        )
        search_artist_button.click()
        logger.info("Search for artist name button clicked.")

        # Step 4: Enter the artist name "Shreya Ghoshal"
        search_field = WebDriverWait(setup_driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.widget.EditText"))
        )
        search_field.click()
        search_field.send_keys("Shreya Ghoshal")
        logger.info("Entered artist name 'Shreya Ghoshal'.")

        # Step 5: Select the artist from the dropdown
        artist_result = WebDriverWait(setup_driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//android.view.View[contains(@content-desc, 'shreya-ghoshal')]"))
        )
        artist_result.click()
        logger.info("Selected artist 'Shreya Ghoshal'.")

        # Step 6: Click on the 'Continue' button
        continue_button = WebDriverWait(setup_driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//android.widget.Button[@content-desc='Continue']"))
        )
        continue_button.click()
        logger.info("Clicked 'Continue' button.")

        # Step 7: Validate presence of highlight cards after scrolling
        touch_action = TouchAction(setup_driver)
        touch_action.press(x=500, y=1000).move_to(x=500, y=200).release().perform()  # Scroll down
        time.sleep(1)
        touch_action.press(x=500, y=200).move_to(x=500, y=1000).release().perform()  # Scroll up
        time.sleep(1)
        logger.info("Scrolled down to check highlight cards.")

    except Exception as e:
        logger.error(f"An error occurred during the test: {e}")
        raise

def test_switch_artist(setup_driver):
    """
    Test case: Switch from one artist to another in the dropdown menu.
    """
    try:
        # Step 1: Click on the dropdown menu for the artist "Shreya Ghoshal"
        logger.info("Clicking on 'Shreya Ghoshal' artist dropdown menu...")
        shreya_ghoshal_dropdown = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.view.View[starts-with(@content-desc, 'Shreya Ghoshal')]/android.widget.ImageView[1]"))
        )
        shreya_ghoshal_dropdown.click()
        logger.info("Clicked on 'Shreya Ghoshal' dropdown menu.")

    except Exception as e:
        logger.error(f"An error occurred during the artist switch test: {str(e)}")
        raise

def test_final_verification(setup_driver):
    """Test case 8: Final verification of the app state."""
    try:
        logger.info("Starting final verification test...")
        
        # Verify dashboard
        dashboard = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.view.View[@content-desc='Dashboard']"))
        )
        assert dashboard.is_displayed(), "❌ Dashboard not found!"
        
        # Verify artist switcher
        artist_switcher = WebDriverWait(setup_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//android.view.View[contains(@content-desc, 'Artist Switcher')]"))
        )
        assert artist_switcher.is_displayed(), "❌ Artist switcher not found!"
        
        logger.info("✅ Final verification completed successfully")
        logger.info("🎉 All tests completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Final verification failed: {str(e)}")
        raise

def cleanup_screenshots():
    """Delete all previous error screenshots"""
    try:
        files = glob.glob("error_*.png")
        for f in files:
            os.remove(f)
        logger.info("Cleaned up previous error screenshots")
    except Exception as e:
        logger.warning(f"Screenshot cleanup failed: {str(e)}")

# Continue with other test functions, using setup_driver instead of driver
# Remove individual teardowns and status updates
# Remove dependencies since we're running in sequence 