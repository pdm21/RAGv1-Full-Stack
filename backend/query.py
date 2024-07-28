import argparse
from langchain_community.vectorstores import Chroma  # Updated import
from langchain.prompts import ChatPromptTemplate
from openai import OpenAI
import os

from get_embeddings import get_embedding_function

# Load the API key from the environment variable
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

def main():
    # Create CLI
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

def query_rag(query_text: str):
    # Prepare the DB
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the db
    results = db.similarity_search_with_score(query_text, k = 5)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    # model = Ollama(model="mistral")
    # Update the Ollama instance to point to the correct URL
    # model = Ollama(base_url="http://ollama-container:11434/api/generate", model="mistral")

    # response_text = model.invoke(prompt)

    # Call the OpenAI model
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Only use context from the prompt to generate your response."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    response_text = response.choices[0].message.content.strip()

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"{response_text}\n\nSources: {sources}"
    print(formatted_response)
    return response_text


if __name__ == "__main__":
    main()
