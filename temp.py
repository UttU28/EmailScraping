from simplegmail import Gmail
from simplegmail.query import construct_query
from tqdm import tqdm
from colorama import Fore, Style, init
from time import sleep
import re, os, json

init()

query_params = {
    "older_than": (2, "day"),
}

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


def checkRequirementMatching(taroText, shouldBe, shouldNot):
    for temp1 in shouldBe:
        if temp1 in taroText:
            for temp2 in shouldNot:
                if temp2 in taroText:
                    return False
            return True
    return False

if __name__ == '__main__':
    gmail = Gmail()
    inboxMessages = gmail.get_messages(query=construct_query(query_params))
    totalEmails = len(inboxMessages)
    print(totalEmails)

    # requirementMatch = 0
    # deletedMails = 0

    # tqdm.write(Fore.YELLOW + f"Total Emails to Process: {totalEmails}" + Style.RESET_ALL)

    # for message in tqdm(inboxMessages, desc="Processing Emails", unit="email"):
    #     if "powerhouse" in message.sender.lower():
    #         checkSubject = checkRequirementMatching(message.subject.lower(), subjectIn, subjectOut)
    #         checkRequirements = checkRequirementMatching(message.plain.lower(), contentIn, contentOut)
    #         try:
    #             if checkRequirements and checkSubject:
    #                 cleanedMail = cleanTheMail(message.plain)
    #                 saveToJSON(message.subject, cleanedMail)
    #                 requirementMatch += 1
    #                 message.mark_as_read()
    #                 message.star()
    #             else:
    #                 deletedMails += 1
    #                 message.trash()
    #             # sleep(0.3)
    #         except:
    #             print("Something somewhere went wrong boi..")
    # # Summary
    # tqdm.write(Fore.GREEN + f"Total Emails Parsed: {totalEmails}" + Style.RESET_ALL)
    # tqdm.write(Fore.CYAN + f"Requirement Match: {requirementMatch}" + Style.RESET_ALL)
    # tqdm.write(Fore.RED + f"Deleted Mails: {deletedMails}" + Style.RESET_ALL)

