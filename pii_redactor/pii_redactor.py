import spacy
import re


nlp = spacy.load("en_core_web_sm")


with open('PII_Redaction.txt', 'r') as file:                            # Change file as needed
    content = file.read()
    doc = nlp(content)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

    # Matches Emails 
    # [a-zA-Z0-9_.+-]+ - Repeated one or more times: Any lowercase/capital letter, number, underscore, period, plus sign, and dash
    # @ - Symbol splitting local part and domain 
    # [a-zA-Z0-9-]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
    # \. - Matches one period
    # [a-zA-Z0-9-.]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+' 

    # Matches Phone numbers
    # \(? - Escapes parenthesis so it's taken as a literal character '(' instead of grouping
    # [0-9]{3} - Exactly 3 numbers in range of 0-9
    # \)? - Escapes parenthesis so it's taken as a literal character ')' instead of grouping
    # [-\s]? - Can choose one or none of the symbols (dash or space) to go in between groupings of numbers
    # [0-9]{3} - Exactly 3 numbers in range of 0-9
    # [-\s]? - Can choose one or none of the symbols (dash or space) to go in between groupings of numbers
    # [0-9]{4} - Exactly 4 numbers in range of 0-9
    phone_pattern = r'\(?[0-9]{3}\)?[-\s]?[0-9]{3}[-\s]?[0-9]{4}'
    
    # Macthes SSN
    # [0-9]{3} - Exactly 3 numbers in range of 0-9
    # \- - Exactly one dash
    # [0-9]{2} - Exactly 2 numbers in range of 0-9
    # \- - Exactly one dash
    # [0-9]{4} - Exactly 4 numbers in the range of 0-9
    social_pattern = r'[0-9]{3}\-[0-9]{2}\-[0-9]{4}'

    # Macthes Credit Card Numbers
    # [0-9]{4} - Exactly 4 numbers in range of 0-9
    # [\s] - macthes one space
    # [0-9]{4} - Exactly 4 numbers in range of 0-9
    # [\s] - macthes one space
    # [0-9]{4} - Exactly 4 numbers in range of 0-9
    # [\s] - macthes one space
    # [0-9]{4} - Exactly 4 numbers in range of 0-9
    credit_card_pattern = r'[0-9]{4}[\s][0-9]{4}[\s][0-9]{4}[\s][0-9]{4}'

    # Matches Bank Account Numbers
    # [0-9]{9} - Exactly 9 numbers in range of 0-9
    bank_account_pattern = r'[0-9]{9}'
    
    # Matches Addresses
    # [0-9]{1,5} - 1 to 5 numbers in the range of 0-9
    # [\sA-Za-z]+,\s - Matches one or more letters or whitespace, then a comma followed by a whitespace
    # [\sA-Za-z]+,\s - Matches one or more letters or whitespace, then a comma followed by a whitespace
    # [A-Z]{2}\s - Matches the state, two capital letters
    # [0-9]{5} - Matches the zip code, five numbers in range of 0-9
    address_pattern = r'[0-9]{1,5} [\sA-Za-z]+,\s[\sA-Za-z]+,\s[A-Z]{2}\s[0-9]{5}'

    ipv4_address_pattern = r'[0-255]{1}.[0-255]{1}.[0-255]{1}.[0-255]{1}'

    ipv6_address_pattern = r'[A-Fa-f0-9]{1-4}:[A-Fa-f0-9]{1-4}:[A-Fa-f0-9]{1-4}:[A-Fa-f0-9]{1-4}:[A-Fa-f0-9]{1-4}:[A-Fa-f0-9]{1-4}:[A-Fa-f0-9]{1-4}:[A-Fa-f0-9]{1-4}'

    vin_pattern = r'[A-HJ-NPR-Z0-9]{17}'

    phone_redaction = '###-###-####'
    ssn_redaction = '***_**_****'
    credit_card_redaction = '#### #### #### ####'
    bank_account_redaction = '#########'
    name_redaction = '[NAME]'
    email_redaction = '[EMAIL]'
    address_redaction = '[ADDRESS]'

    content = re.sub(phone_pattern, phone_redaction, content, flags=re.M)
    content = re.sub(social_pattern, ssn_redaction, content, flags=re.M)
    content = re.sub(credit_card_pattern, credit_card_redaction, content, flags=re.M)
    content = re.sub(bank_account_pattern, bank_account_redaction, content, flags=re.M)
    content = re.sub(email_pattern, email_redaction, content, flags=re.M)
    content = re.sub(address_pattern, address_redaction, content, flags=re.M)

    for name in names:
        content = content.replace(name, name_redaction)



    with open('PII_redacted.txt', 'w') as file:                         # Change file as needed
        file.write(content)