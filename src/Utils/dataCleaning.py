
import re

def parse_email(text):    
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    
    return [{
            "email": email,
            "username": email.split("@")[0],
            "domain": email.split("@")[1]
        } for email in emails]
        

def parse_contactNumber():
    return


def parse_address():
    return 


if __name__ == "__main__":
    text = "Contact us at support@example.com or sales@company.org."
    print (parse_email(text))


