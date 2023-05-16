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

    # Create dataframe where each row is a page
    df = pd.DataFrame(lean_startup.clean_pages, columns=["text"])

    # Set OpenAI key
    openai.api_key = secret_key_openai

    # Create embeddings for each page (row in df that holds text)
    df["embedding"] = df["text"].apply(
        lambda text: openai.Embedding.create(
            model="text-embedding-ada-002", input=text
        )["data"][0]["embedding"]
    )

    # Save it to a CSV
    df.to_csv("lean_startup_embedded.csv")

    print(df.head(10))


if __name__ == "__main__":
    main()
