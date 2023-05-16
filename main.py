import openai
import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv
from openai.embeddings_utils import cosine_similarity


def get_secret_key() -> str:
    load_dotenv()
    return os.environ.get("OPENAI_KEY")


def main():
    openai.api_key = get_secret_key()

    df = pd.read_csv("lean_startup_embedded.csv")
    df["embedding"] = df["embedding"].apply(eval).apply(np.array)

    # Ask for input for a question
    user_question: str = input("What would you like to ask?\n")

    # Create the search embedding
    search_embedding = openai.Embedding.create(
        model="text-embedding-ada-002", input=user_question
    )["data"][0]["embedding"]

    # Compare them with cosine similarity
    df["similarities"] = df["embedding"].apply(
        lambda x: cosine_similarity(x, search_embedding)
    )

    # Sort the similarity and then get the top 3 results and send them to the prompt as context
    top_3_results = df.sort_values("similarities", ascending=False).head(3)
    print(top_3_results["text"])

    context: list[str] = []
    for i, row in top_3_results.iterrows():
        context.append(row["text"])

    # Create the final context to append to the message
    context: str = "\n".join(context)

    # Create final prompt
    final_prompt: str = f'Use the following passages to answer the query: "{user_question}"\n\nContext:\n{context}'

    print(final_prompt)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant answering questions about an entrepreneurial book known as The Lean Startup. Use the context provided to answer questions. Try to be concise as possible. If you do not know the answer, then state you do not know the answer.",
            },
            {
                "role": "user",
                "content": final_prompt,
            },
        ],
    )["choices"][0]["message"]["content"]

    # Print the response
    print(f"\n\n{response}")


if __name__ == "__main__":
    main()
