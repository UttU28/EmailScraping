from simplegmail import Gmail
from simplegmail.query import construct_query
from datetime import datetime, timedelta

gmail = Gmail()

try:
    # Define the query parameters
    query_params = {
        "older_than": (2, "day"),
    }

    # Get all messages older than 2 days
    messages_to_delete = gmail.get_messages(query=construct_query(query_params))

    # Iterate through each message to check sender and delete if condition matches
    delete_count = 0
    print(len(messages_to_delete))
    for message in messages_to_delete:
        sender = message.sender.lower() if message.sender else ''
        if 'powerhouse' in sender:
            try:
                message.trash()
                delete_count += 1
                print("Deleted")
            except Exception as e:
                print(f"Error deleting message: {str(e)}")

    # Print confirmation
    print(f"Deleted {delete_count} messages from 'powerhouse' senders older than 2 days.")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    gmail.logout()
