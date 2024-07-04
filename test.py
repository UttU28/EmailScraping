from simplegmail import Gmail
from simplegmail.query import construct_query
from tqdm import tqdm
from colorama import Fore, Style, init
from time import sleep
import re

init()
gmail = Gmail()

requiredKeywords = ["devops", "pipeline", "ci/cd", "cicd", "ci-cd"]

queryParams = {
    "newer_than": (1, "day")
}

# messages = gmail.get_messages(query=construct_query(queryParams))
messages = gmail.get_unread_inbox()
print(messages[1].subject)

if messages:
    firstMessage = messages[1].plain.split("\n")
    
    cleanedMessage = []
    for line in firstMessage:
        # Strip leading/trailing whitespace
        strippedLine = line.strip()
        # Remove lines that are empty or contain only whitespace
        if strippedLine:
            # Replace multiple spaces with a single space
            cleanedLine = re.sub(r'\s+', ' ', strippedLine)
            cleanedMessage.append(cleanedLine)
    
    # Print cleaned message
    for line in cleanedMessage:
        print(Fore.CYAN + line + Style.RESET_ALL)
else:
    print(Fore.RED + "No messages found." + Style.RESET_ALL)

def processEmails(messages):
    totalEmails = len(messages)
    requirementMatch = 0
    deletedMails = 0

    tqdm.write(Fore.YELLOW + f"Total Emails to Process: {totalEmails}" + Style.RESET_ALL)

    for message in tqdm(messages, desc="Processing Emails", unit="email"):
        if "powerhouse" in message.sender.lower():
            checkOccurrence = any(keyword in message.plain.lower() for keyword in requiredKeywords)
            if checkOccurrence:
                requirementMatch += 1
                # print(message.)
            else:
                deletedMails += 1
                # message.trash()
            sleep(0.3)

    # Summary
    tqdm.write(Fore.GREEN + f"Total Emails Parsed: {totalEmails}" + Style.RESET_ALL)
    tqdm.write(Fore.CYAN + f"Requirement Match: {requirementMatch}" + Style.RESET_ALL)
    tqdm.write(Fore.RED + f"Deleted Mails: {deletedMails}" + Style.RESET_ALL)

# processEmails(messages)
