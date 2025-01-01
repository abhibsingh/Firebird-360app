import pytest
import time
import logging
import os
import glob
from appium import webdriver
from browserstack_config import BROWSERSTACK_USERNAME, BROWSERSTACK_ACCESS_KEY, BROWSERSTACK_CAPABILITIES

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def cleanup_screenshots():
    """Delete all previous error screenshots"""
    try:
        files = glob.glob("error_*.png")
        for f in files:
            os.remove(f)
        logger.info("Cleaned up previous error screenshots")
    except Exception as e:
        logger.warning(f"Screenshot cleanup failed: {str(e)}")

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