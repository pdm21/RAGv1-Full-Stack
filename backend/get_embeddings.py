from langchain_community.embeddings.bedrock import BedrockEmbeddings

def get_embedding_function():
    embeddings = BedrockEmbeddings(
        credentials_profile_name="default",  # Using the default profile
        region_name="us-east-1",  # Correct region
        model_id="amazon.titan-embed-g1-text-02"  # Correct model ID
    )
    return embeddings
