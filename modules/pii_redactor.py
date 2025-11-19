import os
import regex as re
import pymupdf as fitz
from modules.spacy import SpacyRedactor
from modules.regex import RegexRedactor

class PiiRedactor:
    def __init__(self):
        self.spacy = SpacyRedactor()
        self.regex = RegexRedactor()


    def redact_wrapper(self, input_path: str, output_path: str):
        """
        Wrapper function to execute specific redaction methods
        for files of specific file extensions/types.

        Paramters:
            input_path:     Path to input file to read and redact
            output_path:    Path to output file to store redacted file
        """

        file_ext = input_path.split(".")[-1]
        match(file_ext):
            case "pdf":
                self.redact_pdf(input_path, output_path)
                
            case _:
                self.redact_text(input_path, output_path)
    

    def redact_text(self, input_path: str, output_path: str, *, save: bool = True, text: str = "") -> None | str:
        """
        Redacts the given text file then store the redacted contents into a new file if `save` is True, else this method will redact the provided text string then returns the redacted text.

        Parameters:
            input_path:     Path to input file to read and redact
            output_path:    Path to output file to store redacted contents in
            save:           Whether to save redacted content or not
            text:           The text to redact if `save` is False

        Returns:
            content:        The redacted text content if `save` is False
        """
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

        # Apply Spacy redactions first
        honorifics_pattern = self.regex.get_honorifics_pattern()
        content = self.spacy.get_texts_to_redact(honorifics_pattern, content, redact_now=True)

        # Datatype checking
        if isinstance(content, list):
            raise Exception("`content` in `PiiRedactor.redact_text()` is somehow a list!")

        # Then apply regex redaction afterwards
        content = self.regex.redact_text(content)

        # Return the redacted text if not saving redacted output
        if not save:
            return content

        with open(output_path, "w") as file:
            file.write(content)


    def redact_pdf(self, input_file: str, output_file: str):
        if not input_file.endswith(".pdf"):
            raise Exception("Input file for PDF redaction is NOT a PDF file!")

        doc = fitz.open(input_file)

        for page in doc:
            words = page.get_text("words")
            words_text = " ".join( [w[4] for w in words] )

            nlp_doc = self.spacy.create_nlp_doc(words_text)

            # Apply regex redaction first
            self.regex.apply_pdf_redaction(page, words_text)

            # Then apply Spacy redaction
            self.spacy.apply_pdf_redaction(page, nlp_doc)

        doc.save(output_file, garbage=3, clean=True, deflate=True)
