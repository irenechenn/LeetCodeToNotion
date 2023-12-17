from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os
import time

# Replace with your LeetCode username and password
leetcode_username = os.getenv('LEETCODE_USERNAME')
leetcode_password = os.getenv('LEETCODE_PASSWORD')

def login_to_leetcode(driver, username, password):
    driver.get("https://leetcode.com/accounts/login/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'login')))
    
    username_field = driver.find_element_by_name('login')
    password_field = driver.find_element_by_name('password')
    username_field.send_keys(username)
    password_field.send_keys(password)

    login_button = driver.find_element_by_xpath('//button[@type="submit"]')
    login_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'after-login-class')))  # Update with a class that appears after login

def scrape_problems(driver):
    # Update with the URL of the page that lists the problems
    driver.get("https://leetcode.com/problemset/all/")
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'problem-list-selector')))  # Update with actual selector

    problems = []
    problem_links = driver.find_elements_by_css_selector('a.problem-list-item')  # Update with actual selector
    for link in problem_links:
        driver.get(link.get_attribute('href'))
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'title_selector')))  # Update with actual selector

        title = driver.find_element_by_css_selector('title_selector').text
        description = driver.find_element_by_css_selector('description_selector').text
        difficulty = driver.find_element_by_css_selector('difficulty_selector').text
        sample_test_case = driver.find_element_by_css_selector('sample_test_case_selector').text

        problems.append((title, description, difficulty, sample_test_case))

    return problems

def main():
    chrome_options = Options()
    # Configure ChromeOptions if needed (e.g., headless mode)
    driver = webdriver.Chrome(options=chrome_options)

    try:
        login_to_leetcode(driver, leetcode_username, leetcode_password)
        problems = scrape_problems(driver)

        # TODO: Add the code to push this data to Notion using Notion's API
        # Example: push_to_notion(problems)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
