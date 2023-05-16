# PDFClass.py - holds the PDF class

# Imports
from PyPDF2 import PdfReader, PageObject


class PDF:
    def __init__(self, file_path: str, start_page_num: int, end_page_num: int) -> None:
        self.file_path: str = file_path
        self.pdf_obj: PdfReader = PdfReader(self.file_path)  # Init PDF reader
        self.pages: list[PageObject] = self.pdf_obj.pages[start_page_num:end_page_num]

    def print_approximations(self):
        # Split the pages into "word" arrays for each page (maybe be slightly inaccurate due to PDF)
        pages_split_by_words: list[list[str]] = list(
            map(lambda p: p.extract_text().split(), self.pages)
        )

        # Count the total words in the pages
        total_word_count: int = 0

        for arr_of_words in pages_split_by_words:
            total_word_count += len(arr_of_words)

        # 100 tokens ~= 75 words
        approximated_tokens: int = int(total_word_count * (100 / 75))

        # ada embedding model = $0.0004/1000 tokens -> round to 2 decimal places
        total_approximated_cost: float = round((approximated_tokens / 1000) * 0.0004, 2)

        # Print one time cost estimate
        print(f"Total Amount of Words: {total_word_count}")
        print(f"Total Amount of Tokens: {approximated_tokens}")
        print(f"Total Estimated Cost: ${total_approximated_cost}")
