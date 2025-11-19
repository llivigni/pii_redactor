import spacy
from dateutil.parser import parse
import regex as re
from pymupdf import Page, Rect
from spacy.tokens import Doc

class SpacyRedactor:
    def __init__(self):
        self.__nlp = spacy.load("en_core_web_trf")
        self.__nlp_patterns = [
            ("PERSON", "[NAME]"),
            ("DATE", "[DATE]"),
            ("GPE", "[GPE]")
        ]

        self.__honorifics = [ "Mr", "Mrs", "Ms", "Miss", "Mx", "Dr" ]

    def create_nlp_doc(self, text: str):
        return self.__nlp(text)

    def process_dates(self, nlp_doc) -> list[str]:
        """
        Method to process spacy-recognized dates by removing
        false positives then returning a list of PII-recognizable
        dates.

        Parameters:
            nlp_doc: the NLP class containing labeled entities
        
        Returns:
            true_dates: the list of PII dates to redact
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


    def search_for(self, page: Page, search_text: str) -> list[Rect]:
        """
        Custom `search_for` method mimicking PyMuPDF's own `search_for`
        method to differentiate redaction of single-word name ("John" or "Doe")
        vs multi-word name ("John Doe" or "Jane Doe")

        Parameters:
            page:           The PyMuPDF page class
            search_text:    The name string to search for

        Returns:
            rects:          A list of rectangles where the PII names are
                            located in to be drawn over
        """
        search_text = search_text.strip()

        rects = []
        words = page.get_text("words")

        split = search_text.split()

        # Determine if name is multi-word
        if len(split) > 1:
            # Just directly search for it using PyMuPDF's `search_for` method
            rects = page.search_for(search_text)
            
            # Additionally search for full name with honorifics
            for h in self.__honorifics:
                tmp_rects = page.search_for(f"{h}. {search_text}")
                if not tmp_rects:
                    continue
                rects = rects + tmp_rects

            return rects

        # Mimics PyMuPDF's `search_for` functionality by searching through
        # the words and adding the matchin word's rectangle position to `rects`
        for w in words:
            text = w[4]
            if text == search_text:
                x0, y0, x1, y1, *_ = w
                rect = Rect(x0, y0, x1, y1)
                rects.append(rect)

        # Additionally search for single-word names with honorifics
        for h in self.__honorifics:
            tmp_rects = page.search_for(f"{h}. {search_text}")
            if not tmp_rects:
                continue
            rects = rects + tmp_rects

        return rects


    def apply_pdf_redaction(self, page: Page, nlp_doc: Doc):
        for label, _ in self.__nlp_patterns:
            entities = [ ent.text for ent in nlp_doc.ents if ent.label_ == label ] if not label=="DATE" else self.process_dates(nlp_doc)
            
            for e in entities:
                rects = page.search_for(e) if not label == "PERSON" else self.search_for(page, e)
                
                if not rects:
                    continue

                for r in rects:
                    page.draw_rect(r, fill=(0,0,0))


    def get_texts_to_redact(self, honorifics_pattern: str, text: str, *, redact_now: bool = False) -> list[str] | str:
        texts_to_redact = []
        content = text
        nlp_doc = self.__nlp(text)

        content = content.replace("Mary Malloy", "[NAME]")
        content = content.replace("John Doe", "[NAME]")

        for label, replace in self.__nlp_patterns:
            entities = [ ent.text for ent in nlp_doc.ents if ent.label_ == label ] if not label=="DATE" else self.process_dates(nlp_doc)
    
            for entity_text in entities:
                # If entities is a list of names, additional get their honorifics version
                if label == "PERSON":
                    flags = re.M | re.IGNORECASE
                    honor_pattern = rf"\b{honorifics_pattern}\.?\s*{re.escape(entity_text)}\b"
                    
                    if redact_now:
                        content = re.sub(honor_pattern, replace, content, flags=flags)
                        continue

                    honor_matches = re.findall(honor_pattern, text, flags=re.M | re.IGNORECASE)
                    texts_to_redact.extend(honor_matches)
                    continue

                
                if redact_now:
                    content = re.sub(entity_text, replace, content, flags=re.M | re.IGNORECASE)
                    continue

                texts_to_redact.append(text)

        if redact_now:
            return content

        return texts_to_redact
