# shipment_tracking_project

# Install Python Dependencies
pip install selenium scrapy pyautogui

# Browser Requirements
This parser uses chromium for browser automation

# Run the script
python script.py

# Important Notes
Keep the browser in focus → required for pyautogui
Script uses a 60-second wait for CAPTCHA solving
Do not run in headless mode
Internet connection must be stable

# Output
Extracted data is saved to output.json using the write_json helper
