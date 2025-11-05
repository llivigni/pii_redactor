import spacy
import re
import os
from pypdf import PdfReader
import docx2txt
from pdfminer.high_level import extract_text
from fpdf import FPDF
from docx import Document


class PiiRedactor():
    def __init__(self):
        self.__nlp = spacy.load("en_core_web_sm")
        self.__patterns = [
            # Pattern, Replacement, [Optional additional flags]

            # Email Addresses 
            # [a-zA-Z0-9_.+-]+ - Repeated one or more times: Any lowercase/capital letter, number, underscore, period, plus sign, and dash
            # @ - Symbol splitting local part and domain 
            # [a-zA-Z0-9-]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
            # \. - Matches one period
            # [a-zA-Z0-9-.]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
            ( r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', "[EMAIL]" ),

            # Phone Number
            # \(? - Escapes parenthesis so it's taken as a literal character '(' instead of grouping
            # [0-9]{3} - Exactly 3 numbers in range of 0-9
            # \)? - Escapes parenthesis so it's taken as a literal character ')' instead of grouping
            # [-\s]? - Can choose one or none of the symbols (dash or space) to go in between groupings of numbers
            # [0-9]{3} - Exactly 3 numbers in range of 0-9
            # [-\s]? - Can choose one or none of the symbols (dash or space) to go in between groupings of numbers
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            ( r'\(?[0-9]{3}\)?[-\s]?[0-9]{3}[-\s]?[0-9]{4}', "[PHONE]" ),

            # Social Security Number
            # [0-9]{3} - Exactly 3 numbers in range of 0-9
            # \- - Exactly one dash
            # [0-9]{2} - Exactly 2 numbers in range of 0-9
            # \- - Exactly one dash
            # [0-9]{4} - Exactly 4 numbers in the range of 0-9
            ( r'[0-9]{3}\-[0-9]{2}\-[0-9]{4}', "[SSN]" ),

            # Credit/Bank Card Number
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            # [\s] - macthes one space
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            # [\s] - macthes one space
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            # [\s] - macthes one space
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            ( r'[0-9]{4}[\s][0-9]{4}[\s][0-9]{4}[\s][0-9]{4}', "[CREDIT/DEBIT CARD]" ),

            # Bank Account Number
            # [0-9]{9} - Exactly 9 numbers in range of 0-9
            ( r'[0-9]{9}', "[BANK ACCOUNT]" ),

            # Addresses 
            # [0-9]{1,5} - 1 to 5 numbers in the range of 0-9
            # [\sA-Za-z]+,\s - Matches one or more letters or whitespace, then a comma followed by a whitespace
            # [\sA-Za-z]+,\s - Matches one or more letters or whitespace, then a comma followed by a whitespace
            # [A-Z]{2}\s - Matches the state, two capital letters
            # [0-9]{5} - Matches the zip code, five numbers in range of 0-9
            ( r'[0-9]{1,5} [\sA-Za-z]+,\s[\sA-Za-z]+,\s[A-Z]{2}\s[0-9]{5}', "[ADDRESS]" ),

            # IPV4 Address
            ( r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', "[ipv4]" ),

            # IPV6 Address
            ( r'[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}', "[ipv6]" ),
        
            # MAC Address
            ( r'[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}', "[MAC]" ),

            # Vehicle Identifier Number
            ( r'[A-HJ-NPR-Z0-9]{17}', "[VIN]" ),

            # General License Plate
            ( r'[A-Z]{3}-*\d{4}', "[LICENSE PLATE #]" ),

            # Passport
            ( r'passport.*?[A-Z]{1}[0-9]{8}', "[PASSPORT #]", re.IGNORECASE ),
            
            # Generic Student ID
            ( r'[A-Z]{1}[0-9]{6,8}', "[STUDENT #]" ),

            # United States Driver License Numbers
            (
                [
                    r"\d{7}",                       # AL, AK, DE, ME, OR, DC, WV
                    r"[a-zA-Z]\d{8}",               # AZ, GA, NE, VA
                    r"\d{9}",                       # AZ, CT, HI, IA, LA, MT, NM, SC, UT
                    r"9\d{8}",                      # AR
                    r"[a-zA-Z]\d{7}",               # CA
                    r"\d{2}-\d{3}-\d{4}",           # CO
                    r"[a-zA-Z](\d{3}-*){2}\d{2}-*\d{3}-*\d", # FL
                    r"[a-zA-Z]{2}\d{6}[a-zA-Z]",    # ID
                    r"[a-zA-Z]\d{3}-*(\d{4}-*){2}", # IL
                    r"\d{4}-\d{2}-\d{4}",           # IN
                    r"\d{3}[a-zA-Z]{2}\d{4}",       # IA
                    r"[a-zA-Z](\d{2}-){2}\d{4}",    # KA
                    r"[a-zA-Z]\d{2}-\d{3}-\d{4}",   # KY
                    r"[a-zA-Z]-*(\d{3}-*){4}",      # MD
                    r"[a-zA-Z]\d{9}",               # MA, MO, OK
                    r"[a-zA-Z](\s\d{3}){4}",        # MI
                    r"[a-zA-Z]\d{12}",              # MI, MN
                    r"\d{3}-\d{2}-\d{4}",           # MS
                    r"([0][1-9]|[1][0-2])\d{3}([1-9]\d{3})", # MT
                    r"\d{10}",                      # NV
                    r"([0][1-9]|[1][0-2])([a-zA-Z]\{3})(0[1-9]|[1-2][0-9]|3[0-1])\d", # NH
                    r"[a-zA-Z]\d{4}-*(\d{5}-*){2}", # NJ
                    r"(\d{3}){2}\s\d{3}",           # NY
                    r"\d{12}",                      # NC
                    r"[a-zA-Z]{3}-\d{2}-\d{4}",     # ND
                    r"\d{8}",                       # OH, SD, TX, VT
                    r"[a-zA-Z]{1}\d{4,8}",          # OH
                    r"[a-zA-Z]{2}\d{3,7}",          # OH
                    r"\d{2}( \d{3}){2}",            # PA
                    r"[1-9]{2}\d{5}",               # RI
                    r"\d{7,9}",                     # TN
                    r"\d{7}[a-zA-Z]",               # VT
                    r"[a-zA-Z](\d{2}-){2}\d{4}",    # VA
                    r"[a-zA-Z]{3}\*\*[a-zA-Z]{2}\d{3}[a-zA-Z]\d", # WA
                    r"[a-zA-Z]\d{6}",               # WV
                    r"[a-zA-Z]\d{3}-(\d{4}-){2}\d{2}", # WI
                    r"\d{6}-\d{3}",                 # WY
                ],
                "[DRIVER LICENSE #]" )
        ]

    def redact(self, input_path, output_path):
        content = ""

        with open(input_path, "r") as file:
            content = file.read()
            doc = self.__nlp(content)
            names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
            dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
            gpes = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
            locs = [ent.text for ent in doc.ents if ent.label_ == "LOC"]


            # Redact names
            for name in names:
                content = content.replace(name, "[NAME]")

            # Redact dates
            for date in dates:
                content = content.replace(date, "[DATE]")

            # Redact GPEs
            for gpe in gpes:
                content = content.replace(gpe, "[CITY, STATE, OR COUNTRY]")

            # Redact locations
            for loc in locs:
                content = content.replace(loc, "[LOCATION]")

            # Match all recorded patterns with respective replacements
            for pattern, replace, *additional_flags in self.__patterns:
                flags = re.M

                for flag in additional_flags:
                    flags |= flag

                if not isinstance(pattern, list):
                    content = re.sub(pattern, replace, content, flags=flags)
                    continue

                for p in pattern:
                    content = re.sub(p, replace, content, flags=flags)

        with open(output_path, "w") as file:
            file.write(content)
