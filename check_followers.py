import requests
import smtplib
import os
import sys
from email.mime.text import MIMEText

# ---- CONFIG ----
GITHUB_USERNAME = "Aksadio"   # <-- tomar GitHub username diye replace koro jodi change hoy
FOLLOWER_THRESHOLD = 88

# ---- Environment variables (GitHub Secrets theke ashbe) ----
EMAIL_USERNAME = os.environ["EMAIL_USERNAME"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
TO_EMAIL = os.environ["TO_EMAIL"]


def get_follower_count(username):
    url = f"https://api.github.com/users/{username}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return data["followers"]


def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USERNAME
    msg["To"] = TO_EMAIL

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, [TO_EMAIL], msg.as_string())


def main():
    followers = get_follower_count(GITHUB_USERNAME)
    print(f"Current followers: {followers}")

    if followers >= FOLLOWER_THRESHOLD:
        subject = f"🎉 Tumi {followers} followers cross korecho!"
        body = (
            f"Congrats! Tomar GitHub account '{GITHUB_USERNAME}' er follower "
            f"count ekhon {followers}, jeta {FOLLOWER_THRESHOLD} threshold cross korese.\n\n"
            f"Ekhon committers.top er 'Most active GitHub users in Bangladesh' list e "
            f"check koro, tumi ekhon eligible hote paro!\n\n"
            f"Link: https://committers.top/bangladesh.html"
        )
        send_email(subject, body)
        print("Email sent!")
    else:
        print(f"Ekhono threshold cross hoyni ({followers}/{FOLLOWER_THRESHOLD}). Email pathano hoyni.")


if __name__ == "__main__":
    main()
