import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import schedule
import time

def send_email(subject, body, to_email):
    from_email = "skrishan111213@gmail.com"
    password = "wRaHQA1FgfUMGTE7"
    smtp_server = "smtp-relay.sendinblue.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))


def get_friends_details():
    friends_details = {}
    friend_profiles = [
        "https://leetcode.com/Krishan36/",
        "https://leetcode.com/as727243/",
        "https://leetcode.com/anurag_119/",
        "https://leetcode.com/abhishekbhu/",
    ]

    for profile_url in friend_profiles:
        response = requests.get(profile_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            details = {}

            # Extract profile information
            name_element = soup.find("div", class_="text-label-1 dark:text-dark-label-1 break-all text-base font-semibold")
            if name_element:
                details["Name"] = name_element.text.strip()

            rank = soup.find("span", class_="ttext-label-1 dark:text-dark-label-1 font-medium")
            if rank:
                details["Rank"] = rank.text.strip()

            solved_element = soup.find("div", class_="text-[24px] font-medium text-label-1 dark:text-dark-label-1")
            if solved_element:
                details["Solved"] = solved_element.text.strip()

            submission_element = soup.find("div", class_="mr-[5px] text-base font-medium lc-md:text-xl")
            if submission_element:
                details["Submission"] = submission_element.text.strip()

            all_details = soup.find("div", class_="flex w-full flex-col space-y-4 lc-xl:max-w-[228px]")
            if all_details:
                all_text = all_details.text.strip()
                details["All"] = all_text.replace("%", "%\n").replace("Beats", " Beats")

            last_submit = soup.find("span", class_="text-label-3 dark:text-dark-label-3 hidden whitespace-nowrap lc-md:inline")
            if last_submit:
                details["Last_Submit_Time"] = last_submit.text.strip()

            friends_details[profile_url] = details

    return friends_details


def compose_email(details):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    body = f"LeetCode Progress - {date}\n\n"

    for profile_url, profile_details in details.items():
        body += f"Profile URL: {profile_url}\n"
        for key, value in profile_details.items():
            body += f"{key}: {value}\n"
        body += "\n"

    return body


def send_daily_email():
    friends_details = get_friends_details()
    email_body = compose_email(friends_details)
    email_subject = "LeetCode Profile Details Report"
    recipient_email = "krishankantsen.bhumca22@gmail.com"
    # recipient_email1 = "krishankantsen.bhumca22@gmail.com"
  
    send_email(email_subject, email_body, recipient_email)
    # send_email(email_subject, email_body, recipient_email)


# Schedule the daily email
# schedule.every().day.at("00:00").do(send_daily_email)
schedule.every(1).minutes.do(send_daily_email)

# Keep the program running to allow scheduled tasks to be executed
while True:
    schedule.run_pending()
    time.sleep(1)
# def main():
#     friends_details = get_friends_details()
#     email_body = compose_email(friends_details)
#     email_subject = "LeetCode Profile Details Report"
#     recipient_email = "krishankantsen.bhumca22@gmail.com"
#     send_email(email_subject, email_body, recipient_email)


# if __name__ == "__main__":
#     main()
