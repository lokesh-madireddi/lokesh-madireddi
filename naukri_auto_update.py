import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import subprocess

load_dotenv()

NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL")
RESUME_FILE_PATH = os.getenv("RESUME_FILE_PATH")

def clone_resume():
    if not os.path.exists("resume_repo"):
        subprocess.run(["git", "clone", GITHUB_REPO_URL, "resume_repo"])
    else:
        subprocess.run(["git", "-C", "resume_repo", "pull"])

def upload_resume(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Go to Naukri Login Page
    page.goto("https://www.naukri.com/mnjuser/login")
    page.fill("input[placeholder='Enter your active Email ID / Username']", NAUKRI_EMAIL)
    page.fill("input[placeholder='Enter your password']", NAUKRI_PASSWORD)
    page.click("button[type='submit']")

    page.wait_for_timeout(5000)  # Wait for login to complete, adjust as needed

    # Navigate to Profile > Resume Upload Section
    page.goto("https://www.naukri.com/mnjuser/profile")
    page.wait_for_selector("input[type='file']")

    resume_path = os.path.join("resume_repo", RESUME_FILE_PATH)
    page.set_input_files("input[type='file']", resume_path)

    page.wait_for_timeout(5000)
    browser.close()

if __name__ == "__main__":
    clone_resume()
    with sync_playwright() as playwright:
        upload_resume(playwright)
