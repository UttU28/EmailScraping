from simplegmail import Gmail
from simplegmail.query import construct_query
from tqdm import tqdm
from colorama import Fore, Style, init
from time import sleep
import re, os, json

# Initialize Colorama
init()

class EmailProcessor:
    def __init__(self):
        self.content_in = ["devops", "pipeline", "ci/cd", "cicd", "ci-cd", "aws"]
        self.content_out = ["usc", "usc gc", "security clearance", "8+", "9+", "10+", "11+", "12+"]
        self.subject_in = ["devops", "azure", "aws", "cloud", "cloud engineer", "cloud developer", "terraform", "ansible", "cicd", "ci-ci", "ci/cd", "kubernetes"]
        self.subject_out = ["admin", "platform", "devsecops", "fullstack", "java", ".net", "analyst", "full stack", "product"]
        self.file_name = "email_data.json"
        self.gmail = Gmail()
        
    def clean_the_mail(self, email_content):
        first_message = email_content.split("\n")
        cleaned_message = []
        for line in first_message:
            stripped_line = line.strip()
            if stripped_line:
                cleaned_line = re.sub(r'\s+', ' ', stripped_line)
                cleaned_message.append(cleaned_line)
        
        cleaned_message_joined = "\n".join(cleaned_message).replace(
            """Remove/unsubscribe | Update your contact and subscribed mailing list(s) | Subscribe to mailing list(s) to receive requirements & resumes\nFrom:\n""",
            ""
        )
        return cleaned_message_joined

    def save_to_json(self, subject, message):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                data = json.load(file)
        else:
            data = {}
        
        index = len(data)
        key = f"{index}_{subject}"
        data[key] = message
        
        with open(self.file_name, 'w') as file:
            json.dump(data, file, indent=4)

    def check_requirement_matching(self, taro_text, should_be, should_not):
        for temp1 in should_be:
            if temp1 in taro_text:
                for temp2 in should_not:
                    if temp2 in taro_text:
                        return False
                return True
        return False

    def delete_old_mails(self):
        keyword = 'powerhouse'
        days = 2
        try:
            query_params = {
                "older_than": (days, "day"),
            }
            messages_to_delete = self.gmail.get_messages(query=construct_query(query_params))
            total_messages = len(messages_to_delete)
            delete_count = 0

            with tqdm(total=total_messages, desc=f"Deleting messages from '{keyword}'") as pbar:
                for message in messages_to_delete:
                    sender = message.sender.lower() if message.sender else ''
                    if keyword.lower() in sender:
                        try:
                            message.trash()
                            delete_count += 1
                        except Exception as e:
                            print(f"Error deleting message: {str(e)}")

                    pbar.update(1)

            print(f"\nDeleted {delete_count} messages from '{keyword}' senders older than {days} days.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def process_emails(self):
        self.delete_old_mails()
        inbox_messages = self.gmail.get_unread_inbox()
        total_emails = len(inbox_messages)
        requirement_match = 0
        deleted_mails = 0

        tqdm.write(Fore.YELLOW + f"Total Emails to Process: {total_emails}" + Style.RESET_ALL)

        for message in tqdm(inbox_messages, desc="Processing Emails", unit="email"):
            if "powerhouse" in message.sender.lower():
                check_subject = self.check_requirement_matching(message.subject.lower(), self.subject_in, self.subject_out)
                check_requirements = self.check_requirement_matching(message.plain.lower(), self.content_in, self.content_out)
                try:
                    if check_requirements and check_subject:
                        cleaned_mail = self.clean_the_mail(message.plain)
                        self.save_to_json(message.subject, cleaned_mail)
                        requirement_match += 1
                        message.mark_as_read()
                        message.star()
                    else:
                        deleted_mails += 1
                        message.trash()
                    # sleep(0.3)
                except:
                    print("Something somewhere went wrong boi..")
        
        # Summary
        tqdm.write(Fore.GREEN + f"Total Emails Parsed: {total_emails}" + Style.RESET_ALL)
        tqdm.write(Fore.CYAN + f"Requirement Match: {requirement_match}" + Style.RESET_ALL)
        tqdm.write(Fore.RED + f"Deleted Mails: {deleted_mails}" + Style.RESET_ALL)

if __name__ == '__main__':
    processor = EmailProcessor()
    processor.process_emails()
