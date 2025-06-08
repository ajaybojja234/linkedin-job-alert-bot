import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText
import smtplib

# === CONFIG ===
LINKEDIN_URL = "https://www.linkedin.com/jobs/search/?keywords=devops&f_TPR=r86400"
TO_EMAIL = "99ajaybojja@gmail.com"
FROM_EMAIL = "99ajaybojja@gmail.com"
APP_PASSWORD = "wenq vyzo blmv vllp"  # <- Paste Gmail app password here
CHECK_INTERVAL = 300  # in seconds (5 minutes)
sent_links = set()
# ==============

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(msg)

def fetch_jobs():
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)
    driver.get(LINKEDIN_URL)
    time.sleep(5)

    job_cards = driver.find_elements(By.CLASS_NAME, "job-search-card")
    new_jobs = []

    for card in job_cards:
        try:
            time_posted = card.find_element(By.CLASS_NAME, "job-search-card__listdate").text.lower()
            print(f"Found job posted: {time_posted}")

            if "just now" in time_posted or "minute" in time_posted:
                link = card.find_element(By.CLASS_NAME, "base-card__full-link").get_attribute("href")
                title = card.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
                company = card.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
                location = card.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()

                if link and link not in sent_links:
                    job_details = f"📌 Title: {title}\n🏢 Company: {company}\n📍 Location: {location}\n🕒 Posted: {time_posted}\n🔗 Apply: {link}"
                    new_jobs.append((f"🚀 New DevOps Job: {title}", job_details))
                    sent_links.add(link)
        except Exception:
            continue

    driver.quit()
    return new_jobs
if __name__ == "__main__":
    while True:
        print("🔍 Checking LinkedIn for new DevOps jobs...")
        jobs = fetch_jobs()
        for subject, body in jobs:
            send_email(subject, body)
            print(f"📨 Sent: {subject}")

        print("Waiting 5 minutes...\n")
        time.sleep(CHECK_INTERVAL)
