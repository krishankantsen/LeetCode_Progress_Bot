import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

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
    # Replace with the profile URLs of your friends on LeetCode
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

            level_element = soup.find("div", class_="css-xqvejy-Tag css-1n5s2jr-Tag css-1p0v0sl-Tag css-1hph3kq-Tag css-f7s0cr-Tag")
            if level_element:
                details["Level"] = level_element.text.strip()

            solved_element = soup.find("div", class_="text-[24px] font-medium text-label-1 dark:text-dark-label-1")
            if solved_element:
                details["Solved"] = solved_element.text.strip()

            accuracy_element = soup.find("div", class_="css-1b3bb7o-PercentNumber e5i1odf1")
           
            if accuracy_element:
                details["Accuracy"] = accuracy_element.text.strip()
            submission_element = soup.find("div", class_="css-1xbtzd6-Submissions css-1i0edl6-Submissions")
            if accuracy_element:
                details["Submission"] = submission_element.text.strip()
            easy = soup.find("span", class_="mr-[5px] text-base font-medium leading-[20px] text-label-1 dark:text-dark-label-1")
           
            if accuracy_element:
                details["Easy"] = easy.text.strip()    


            friends_details[profile_url] = details
            


    return friends_details


def compose_email(details):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    body = f"LeetCode Progress - {date}\n\n"
    # for profile_url, profile_details in details.items():
    #     for key, value in profile_details.items():
    #         print(key,value)
    for profile_url, profile_details in details.items():
        body += f"Profile URL: {profile_url}\n"
        for key, value in profile_details.items():
            body += f"{key}: {value}\n"
        body += "\n"
    return body


def main():
    friends_details = get_friends_details()
    email_body = compose_email(friends_details)
    email_subject = "LeetCode Profile Details Report"
    recipient_email = "krishankantsen.bhumca22@gmail.com"
    send_email(email_subject, email_body, recipient_email)


if __name__ == "__main__":
    main()
