from simplegmail import Gmail
from simplegmail.query import construct_query
from tqdm import tqdm
from colorama import Fore, Style, init
from time import sleep
import re, os, json

requiredKeywords = ["devops", "pipeline", "ci/cd", "cicd", "ci-cd"]
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
    
    print(f"Data saved to {fileName}")


if __name__ == '__main__':
    gmail = Gmail()
    inboxMessages = gmail.get_unread_inbox()
    totalEmails = len(inboxMessages)
    requirementMatch = 0
    deletedMails = 0

    tqdm.write(Fore.YELLOW + f"Total Emails to Process: {totalEmails}" + Style.RESET_ALL)

    for message in tqdm(inboxMessages, desc="Processing Emails", unit="email"):
        if "powerhouse" in message.sender.lower():
            checkOccurrence = any(keyword in message.plain.lower() for keyword in requiredKeywords)
            if checkOccurrence:
                cleanedMail = cleanTheMail(message.plain)
                saveToJSON(message.subject, cleanedMail)
                requirementMatch += 1
                # message.mark_as_read()
                message.star()
            else:
                deletedMails += 1
                message.trash()
            sleep(0.3)

    # Summary
    tqdm.write(Fore.GREEN + f"Total Emails Parsed: {totalEmails}" + Style.RESET_ALL)
    tqdm.write(Fore.CYAN + f"Requirement Match: {requirementMatch}" + Style.RESET_ALL)
    tqdm.write(Fore.RED + f"Deleted Mails: {deletedMails}" + Style.RESET_ALL)

