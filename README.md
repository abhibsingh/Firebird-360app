# Mobile App Test Automation Suite

Automated test suite for mobile application using Python, Pytest, and BrowserStack.

## Overview
This test suite automates the testing of mobile application functionalities including account creation, artist search, profile management, and content verification using BrowserStack's App Automate.

## Prerequisites
- Python 3.11 or higher
- BrowserStack account access (invitation required)
- Git

## Setup Instructions

1. **Clone Repository**
bash
git clone <repository-url>
cd <project-directory>
2. **Set Up Python Environment**
bash
Create virtual environment
python -m venv venv
Activate virtual environment
For Windows:
venv\Scripts\activate
For macOS/Linux:
source venv/bin/activate

3. **Install Dependencies**
bash
pip install -r requirements.txt

## Test Execution

### Run All Tests
bash
pytest test_app.py -v --log-cli-level=INFO -s

### Run Specific Test
```bash
pytest test_app.py -v -k "test_account_creation" --log-cli-level=INFO -s
```

## Test Cases

1. **Account Creation** (`test_account_creation`)
   - Creates new user account
   - Validates registration process

2. **Manager Navigation** (`test_navigate_to_manager`)
   - Tests navigation to Manager section

3. **Manager Flow** (`test_continue_manager_flow`)
   - Validates Manager setup process

4. **Artist Search** (`test_search_artist`)
   - Tests artist search functionality
   - Validates artist selection

5. **Content Verification** (`test_verify_app_content`)
   - Verifies app content and UI elements

6. **Artist Profile** (`test_add_artist_and_validate_highlights`)
   - Tests adding new artist profile
   - Validates highlight cards

7. **Artist Switching** (`test_switch_artist`)
   - Tests profile switching functionality

8. **Final Verification** (`test_final_verification`)
   - Validates final app state

## Project Structure
```
project_root/
├── test_app.py            # Main test file
├── conftest.py           # Test fixtures
├── browserstack_config.py # BrowserStack settings
└── requirements.txt      # Dependencies
```

## BrowserStack Integration

- Tests run on Samsung Galaxy S22 (Android 12.0)
- App is pre-uploaded to BrowserStack
- Configuration pre-set in browserstack_config.py
- Live test execution viewable on BrowserStack dashboard

## Monitoring Tests

1. **BrowserStack Dashboard**
   - View live test execution
   - Access video recordings
   - View device logs
   - Check network logs
   - View screenshots

2. **Local Monitoring**
   - Console logs with -s flag
   - Error screenshots in project directory
   - Detailed logging with INFO level

## Troubleshooting

### Common Issues
1. **Test Start Issues**
   - Verify BrowserStack access
   - Check Python version
   - Verify dependencies

2. **Element Location Issues**
   - Check app state
   - Verify element selectors
   - Review error screenshots

3. **Connection Issues**
   - Check internet connection
   - Verify BrowserStack status

### Error Screenshots
- Automatically captured on failure
- Saved as error_*.png
- Previous screenshots cleaned before new run

## Support

- BrowserStack Status: https://status.browserstack.com/
- BrowserStack Docs: https://www.browserstack.com/docs/
- Contact development team for app-specific issues

## Dependencies
```
pytest==8.2.2
Appium-Python-Client==3.1.1
selenium==4.18.1
pytest-html==4.1.1
pytest-metadata==3.1.1
```

## Notes
- Tests run in sequence due to state dependencies
- Each test builds on previous test's state
- Screenshots capture failure points
- BrowserStack provides live monitoring
- Pre-configured for optimal stability