from simplegmail import Gmail
from simplegmail.query import construct_query

gmail = Gmail()
keyWords = ["azure", "aws", "devops", "pipeline"]

queryParams = {
    "newer_than": (1, "day")
}

# messages = gmail.get_messages(query=construct_query(queryParams))
messages = gmail.get_unread_inbox()

print(len(messages))

for message in messages:
    if "powerhouse" in message.sender:
        print("sender", message.sender)
        checkOccurance = any(keyword in message.plain.lower() for keyword in keyWords)
        if checkOccurance:
            print("subject", message.subject)
        else:
            print("Delete", message.subject)
            print(message.trash())
        # print("plain", message.plain)
        # print("headers", message.headers)