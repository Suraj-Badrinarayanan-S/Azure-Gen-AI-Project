## Code: Dataset Import
import csv
from azure.data.tables import TableServiceClient, TableEntity, UpdateMode

# Azure Table Storage connection
connection_string = "DefaultEndpointsProtocol=https;AccountName=genaiproject;AccountKey=.secret-key;EndpointSuffix=core.windows.net"
table_name = "AzureProjTable"

# Create TableServiceClient
table_service = TableServiceClient.from_connection_string(conn_str=connection_string)
table_client = table_service.get_table_client(table_name)

# Create table if it doesn't exist
try:
    table_service.create_table(table_name)
except Exception as e:
    print(f"Table may already exist: {e}")

csv_file_path = "/Users/../Desktop/AzurelibQAProject 4/azurelib2.csv"

with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        entity = {
            'PartitionKey': "AZURELIB",
            'RowKey': row['id'],
            'Question': row['question'],
            'Answer': row['answer']
        }

        try:
            table_client.upsert_entity(entity=entity, mode=UpdateMode.MERGE)
            print(f"Upserted: {entity['RowKey']} - {entity['Question']}")
        except Exception as e:
            print(f"Error upserting {entity['RowKey']}: {e}")

print("Data sync (upsert) complete.")

## Code: Chat Bot Azure

import streamlit as st
#from openai import OpenAI
import os
st.title("Suraj's Chatbot")

# Step 2: Set the environment variables for Azure AI Search
# These variables configure the search service and index for retrieving documents

# Set the Azure AI Search service name
os.environ["AZURE_AI_SEARCH_SERVICE_NAME"] = "azureaisearchsuraj"

# Set the Azure AI Search index name to query
os.environ["AZURE_AI_SEARCH_INDEX_NAME"] = "azuretable-indexer"

# Set the Azure AI Search API key for authentication
os.environ["AZURE_AI_SEARCH_API_KEY"] = "secret key"


# Import necessary libraries and modules from Langchain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import AzureChatOpenAI
from langchain_community.retrievers import AzureAISearchRetriever

# Step 1: Initialize the AzureAI Search Retriever
# This retrieves relevant documents based on the user query from the Azure Search index
retriever = AzureAISearchRetriever(
    content_key="Answer",  # The key for the content field in the search results change it accordingly as per your data
    top_k=3,              # Number of top results to retrieve
    index_name="azuretable-index"  # Name of the Azure Search index to query
)

# Step 2: Define the prompt template for the language model
# This sets up how the context and question will be formatted for the model
prompt = ChatPromptTemplate.from_template(
    """Answer the question based only on the context provided.

Context: {context}  # Placeholder for the context from the retriever

Question: {question}  # Placeholder for the user question"""
)


# Step 3: Initialize the Azure Chat OpenAI model
# This sets up the model to be used for generating responses

llm = AzureChatOpenAI(
         api_version="2025-01-01-preview",  
      azure_endpoint="https://suraj-m9be1ytj-swedencentral.openai.azure.com/" ,
    api_key="ALppP4Gz32QTWWjGPlU0hPat11pDg0VpNNXF8i2fiUoFQEb2VN6tJQQJ99BDACfhMk5XJ3w3AAAAACOGcT4T",          # Fetch the API key for Azure OpenAI from environment variables
                     # Specify the API version to use
    model="gpt-4o-deployment"                              # Specify the model to use
)





# Step 4: Create a processing chain
# This chain will process the retrieved context and the user question
chain = (
    {"context": retriever , "question": RunnablePassthrough()}  # Set context using the retriever and format it
    | prompt                                                               # Pass the formatted context and question to the prompt
    | llm                                                                  # Generate a response using the language model
    | StrOutputParser()                                                   # Parse the output to a string format
)


# Set OpenAI API key from Streamlit secrets
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_question := st.chat_input("How Can I help you?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_question)
# Display assistant response in chat message container
    with st.chat_message("assistant"):
   
        
        response = chain.invoke(user_question)
      
        st.write(response)


        st.session_state.messages.append({"role": "assistant", "content": response})
