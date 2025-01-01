# BrowserStack Credentials
BROWSERSTACK_USERNAME = "abhisheksingh_uPLMkW"
BROWSERSTACK_ACCESS_KEY = "W4zaazKziFuu6qhuDyN7"

# BrowserStack Capabilities
BROWSERSTACK_CAPABILITIES = {
    # Basic capabilities
    'platformName': 'Android',
    'platformVersion': '12.0',
    'deviceName': 'Samsung Galaxy S22',
    'app': 'bs://6a76d1df7014f89d3f352dcfee23d613d9ce82fa',
    
    # Visual/Headed mode settings
    'browserstack.video': True,
    'browserstack.debug': True,
    'browserstack.networkLogs': True,
    'browserstack.deviceLogs': True,
    'browserstack.visual': True,
    'browserstack.local': False,
    'browserstack.appium_version': '2.0.0',
    'browserstack.maskCommands': "setValues, getValues, setCookies, getCookies",
    
    # Additional settings
    'newCommandTimeout': 900,
    'noReset': True,
    'fullReset': False,
    'autoAcceptAlerts': True,
    'waitForIdleTimeout': 0,
    
    # Keyboard handling
    'unicodeKeyboard': True,
    'resetKeyboard': True,
    'autoGrantPermissions': True,
    
    # Project capabilities
    'project': 'Mobile App Testing',
    'build': 'Build 1.0',
    'name': 'App Automation Tests',
    
    # Performance settings
    'androidInstallTimeout': 120000,
    'adbExecTimeout': 120000,
    'uiautomator2ServerLaunchTimeout': 120000,
    'uiautomator2ServerInstallTimeout': 120000,
    
    # Add stability settings
    'enablePerformanceLogging': True,
    'skipUnlock': True,
    'automationName': 'UiAutomator2',
}

# Additional stability settings
BROWSERSTACK_CAPABILITIES.update({
    'autoGrantPermissions': True,
    'automationName': 'UiAutomator2',
    'uiautomator2ServerInstallTimeout': 120000,
    'androidInstallTimeout': 120000,
    'adbExecTimeout': 120000,
    'skipServerInstallation': False,
    'skipDeviceInitialization': False,
    'disableWindowAnimation': True,
    'recreateChromeDriverSessions': True
}) 