import spacy
import re
import os
from dateutil.parser import parse
import pymupdf as fitz

class PiiRedactor():
    def __init__(self):
        self.__nlp = spacy.load("en_core_web_trf")
        self.__nlp_patterns = [
            # SpaCy label, redaction replacement
            ("PERSON", "[NAME]"),
            ("DATE", "[DATE]"),
            #("GPE", "[CITY, STATE, or COUNTRY]"),
            #("LOC", "[LOCATION]")
        ]
        self.__patterns = [
            # Pattern, Replacement, [Optional additional flags]

            # Medical Record Number
            ( r'(?i)medical\s*(?:record)?\s*(?:number|num|#)?[:\s]{0,10}(\d{6,12})\b', "[MEDICAL RECORD #]", re.IGNORECASE ),


            # Passport
            ( r'passport.*?[A-Z]{1}[0-9]{8}', "[PASSPORT #]", re.IGNORECASE ),

            # Vehicle Identifier Number
            ( r'[A-HJ-NPR-Z0-9]{17}', "[VIN]" ),

            # Age
            ( r'\b(?:aged?\s*\d{1,3}|(?:\d{1,3}\s*(?:years?|yrs?|yo|y/o)\s*old?)|\d{1,3}-year-old)\b', "[AGE]" ),

            # Email Addresses 
            # [a-zA-Z0-9_.+-]+ - Repeated one or more times: Any lowercase/capital letter, number, underscore, period, plus sign, and dash
            # @ - Symbol splitting local part and domain 
            # [a-zA-Z0-9-]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
            # \. - Matches one period
            # [a-zA-Z0-9-.]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
            ( r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', "[EMAIL]" ),

            # Fax
            ( r'fax.{0,15}(\(?[0-9]{3}\)?[-\s]?[0-9]{3}[-\s]?[0-9]{4})', "[FAX]", re.IGNORECASE ),

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
            ( r'[0-9]{6,17}', "[BANK ACCOUNT]" ),

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

            # General License Plate
            ( r'[A-Z]{3}-*\d{4}', "[LICENSE PLATE #]" ),
            
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

    ##################### Helper Functions #####################
    
    def __process_dates(self, nlp_doc) -> list:
        """
        Method to process spacy-recognized dates by removing
        false positives and return a list of true, human-recognizable
        dates.
        """
        true_dates = []
        RELATIVE_KEYWORDS = [
            "ago", "from now", "next", "last", "past", "future",
            "today", "yesterday", "tomorrow", "this", "coming", "previous",
            "day", "days", "month", "months", "year", "years",
            "week", "weeks"
        ]

        for ent in nlp_doc.ents:
            if not ent.label_ == "DATE":
                continue

            if re.match(r"\b(?:(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day),?\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t|tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:,\s*\d{2,4})?\b", ent.text, re.M):
                true_dates.append(ent.text)
                continue

            if any(keyword in ent.text.lower() for keyword in RELATIVE_KEYWORDS):
                continue

            try:
                date = parse(ent.text, fuzzy=True)
                true_dates.append(ent.text)
            except:
                pass
        
        return true_dates


    def __search_for(self, page, search_text):
        honorifics_pattern = r'(?:Mr|Mrs|Ms|Miss|Mx|Dr)\.?'
        honorifics = [ "Mr", "Mrs", "Ms", "Miss", "Mx", "Dr" ]
        
        search_text = search_text.strip()

        rects = []
        words = page.get_text("words")

        split = search_text.split()

        if len(split) > 1:
            rects = page.search_for(search_text)
            
            # Additionally search for full name with honorifics
            for h in honorifics:
                tmp_rects = page.search_for(f"{h}. {search_text}")
                if not tmp_rects:
                    continue
                rects = rects + tmp_rects

            return rects

        for w in words:
            text = w[4]
            if text == search_text:
                x0, y0, x1, y1, *_ = w
                rect = fitz.Rect(x0, y0, x1, y1)
                rects.append(rect)

        # Additionally search for single-word names with honorifics
        for h in honorifics:
            tmp_rects = page.search_for(f"{h}. {search_text}")
            if not tmp_rects:
                continue
            rects = rects + tmp_rects

        return rects


    def __draw_redact(self, page_buffer, rect):
        """
        Method to draw a rectangular box over given rectangle
        position, then add text on top to show redaction type.
        """
        page_buffer.draw_rect(rect, fill=(0,0,0))

    ################### Main Class Functions ###################

    def redact_wrapper(self, input_path, output_path):
        """
        Wrapper function to execute specific redaction methods
        for files of specific file extensions/types.
        """

        file_ext = input_path.split(".")[-1]
        match(file_ext):
            case "pdf":
                self.redact_pdf(input_path, output_path)
                
            case _:
                self.redact_text(input_path, output_path)


    def redact_text(self, input_path, output_path, *, save=True, text=""):
        content = ""

        if save:
            if not os.path.exists(input_path):
                raise Exception(f"The input path to `redact_text()` doesn't exist: {input_path}")

            with open(input_path, "r") as file:
                content = file.read()
        else:
            if not text:
                raise Exception("Text not provided to `redact_text()` with `save=False`")

            content = text
        
        doc = self.__nlp(content)
        
        for label, replace in self.__nlp_patterns:
            patterns = [ent.text for ent in doc.ents if ent.label_ == label] if not label=="DATE" else self.__process_dates(doc)

            for p in patterns:
                content = content.replace(p, replace)

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

        if not save:
            return

        with open(output_path, "w") as file:
            file.write(content)


    def redact_pdf(self, input_file, output_file):
        if not input_file.endswith(".pdf"):
            raise Exception("Must be PDF file.")
        
        doc = fitz.open(input_file)
        for page in doc:
            words = page.get_text("words")
            words_text = " ".join([w[4] for w in words])

            for pattern, replace, *opt_flags in self.__patterns:
                flags = re.M

                for flag in opt_flags:
                    flags |= flag

                # TODO: Do pattern for driver's license
                if isinstance(pattern, list):
                    continue

                for matched in re.finditer(pattern, words_text, flags):
                    matched_text = matched.group()

                    if "FAX" in replace or "MEDICAL" in replace:
                        matched_text = matched.group(1) if matched.lastindex else matched.group()

                    rects = page.search_for(matched_text)
                    if not rects:
                        continue

                    for rect in rects:
                        self.__draw_redact(page, rect)

                    words_text = re.sub(pattern, "", words_text)

            nlp_doc = self.__nlp(words_text)
            for label, replace in self.__nlp_patterns:
                patterns = [ent.text for ent in nlp_doc.ents if ent.label_ == label] if not label=="DATE" else self.__process_dates(nlp_doc)

                if label == "PERSON":
                    print(label, patterns)

                for p in patterns:
                    rects = page.search_for(p) if not label == "PERSON" else self.__search_for(page, p)
                    
                    if not rects:
                        continue
                    
                    for rect in rects:
                        self.__draw_redact(page, rect)

                    words_text = re.sub(p, "", words_text)

            doc.save(output_file, garbage=3, clean=True, deflate=True)
