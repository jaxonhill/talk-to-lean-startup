# create_embeddings.py - Creates the embeddings for the PDF
import openai
import pandas as pd
import numpy as np

# Classes
from PDFClass import PDF


def main():
    # Create the PDF object with only meaningful pages (Ch 1 : Acknowledgements)
    lean_startup: PDF = PDF(
        file_path="the_lean_startup.pdf", start_page_num=10, end_page_num=272
    )
    lean_startup.print_approximations()  # Print amt of words, tokens, cost


if __name__ == "__main__":
    main()
