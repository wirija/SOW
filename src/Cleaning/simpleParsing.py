import re
import phonenumbers


def parse_email(text):
    emails = re.findall(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)

    return [
        {
            "email": email,
            "username": email.split("@")[0],
            "domain": email.split("@")[1],
        }
        for email in emails
    ]


def parse_contact_number(
    text:str,
    digits:int=6,
):
    text = text.translate(str.maketrans('', '', ' ()'))
    
    regrex_pattern = r"\+?\d{" + str(digits) +  r",}"
    contact_numbers = re.findall(regrex_pattern, text)

    return [
        {
            "numbers": numbers,
            "Country Code": numbers.split("@")[0],
            "Area Code": numbers.split("@")[1],
            "Main Number": numbers.split("@")[1],
        }
        for numbers in contact_numbers
    ]


def parse_address():
    return


def parse_names():
    return


if __name__ == "__main__":
    text = "Contact us at support@example.com or sales@company.org."
    text = "My Phone number is <<12345>>> 4556622313"
    print(parse_contact_number(text))
