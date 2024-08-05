from simplegmail import Gmail
from simplegmail.query import construct_query
from tqdm import tqdm
from colorama import Fore, Style, init
from time import sleep
import re, os, json

contentIn = ["devops", "pipeline", "ci/cd", "cicd", "ci-cd", "aws"]
contentOut = ["usc", "usc gc", "security clearance", "8+", "9+", "10+", "11+", "12+"]
# SUBJECT FILTERING
subjectIn = ["devops", "azure", "aws", "cloud", "cloud engineer", "cloud developer", "terraform", "ansible", "cicd", "ci-ci", "ci/cd", "kubernetes"]
subjectOut = ["admin", "platform", "devsecops", "fullstack", "java", ".net", "analyst", "full stack", "product"]

init()

def cleanTheMail(emailContent):
    firstMessage = emailContent.split("\n")
    cleanedMessage = []
    for line in firstMessage:
        strippedLine = line.strip()
        if strippedLine:
            cleanedLine = re.sub(r'\s+', ' ', strippedLine)
            cleanedMessage.append(cleanedLine)
    
    cleanedMessageJoined = "\n".join(cleanedMessage).replace("""Remove/unsubscribe | Update your contact and subscribed mailing list(s) | Subscribe to mailing list(s) to receive requirements & resumes\nFrom:\n""","")
    # print(Fore.CYAN + cleanedMessageJoined + Style.RESET_ALL)
    return cleanedMessageJoined

def saveToJSON(subject, message):
    fileName = "email_data.json"
    
    if os.path.exists(fileName):
        with open(fileName, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    
    index = len(data)
    key = f"{index}_{subject}"
    data[key] = message
    
    with open(fileName, 'w') as file:
        json.dump(data, file, indent=4)
    
    # print(f"Data saved to {fileName}")

def checkRequirementMatching(taroText, shouldBe, shouldNot):
    for temp1 in shouldBe:
        if temp1 in taroText:
            for temp2 in shouldNot:
                if temp2 in taroText:
                    return False
            return True
    return False

def deleteOldMails():
    keyword = 'powerhouse'
    days = 2
    gmail = Gmail()
    try:
        query_params = {
            "older_than": (days, "day"),
        }
        messages_to_delete = gmail.get_messages(query=construct_query(query_params))
        total_messages = len(messages_to_delete)
        delete_count = 0

        with tqdm(total=total_messages, desc=f"Deleting messages from 'powerhouse'") as pbar:
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

if __name__ == '__main__':
    deleteOldMails()
    gmail = Gmail()
    inboxMessages = gmail.get_unread_inbox()
    totalEmails = len(inboxMessages)
    requirementMatch = 0
    deletedMails = 0

    tqdm.write(Fore.YELLOW + f"Total Emails to Process: {totalEmails}" + Style.RESET_ALL)

    for message in tqdm(inboxMessages, desc="Processing Emails", unit="email"):
        if "powerhouse" in message.sender.lower():
            checkSubject = checkRequirementMatching(message.subject.lower(), subjectIn, subjectOut)
            checkRequirements = checkRequirementMatching(message.plain.lower(), contentIn, contentOut)
            try:
                if checkRequirements and checkSubject:
                    cleanedMail = cleanTheMail(message.plain)
                    saveToJSON(message.subject, cleanedMail)
                    requirementMatch += 1
                    message.mark_as_read()
                    message.star()
                else:
                    deletedMails += 1
                    message.trash()
                # sleep(0.3)
            except:
                print("Something somewhere went wrong boi..")
    # Summary
    tqdm.write(Fore.GREEN + f"Total Emails Parsed: {totalEmails}" + Style.RESET_ALL)
    tqdm.write(Fore.CYAN + f"Requirement Match: {requirementMatch}" + Style.RESET_ALL)
    tqdm.write(Fore.RED + f"Deleted Mails: {deletedMails}" + Style.RESET_ALL)

