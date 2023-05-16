# create_embeddings.py - Creates the embeddings for the PDF
import openai
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

# Classes
from PDFClass import PDF


def get_secret_key() -> str:
    load_dotenv()
    return os.environ.get("OPENAI_KEY")


def main():
    # Create the PDF object with only meaningful pages (Ch 1 : Acknowledgements)
    lean_startup: PDF = PDF(
        file_path="the_lean_startup.pdf", start_page_num=10, end_page_num=272
    )
    lean_startup.print_approximations()  # Print amt of words, tokens, cost

    # Get OpenAI key from environment variable (.env)
    secret_key_openai: str = get_secret_key()


if __name__ == "__main__":
    main()
