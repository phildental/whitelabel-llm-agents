import streamlit as st
import pickle
import dotenv

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.agents import create_csv_agent
import os
import tempfile

dotenv.load_dotenv()

def process_and_store_pickle(file, embeddings_folder):
    file_type = file.type.split('/')[1]

    if file_type == 'pdf':
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        embeddings = OpenAIEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # Generate a unique file name for the pickle file
        pickle_file_name = f"{file.name}_{file_type}.pkl"
        pickle_file_path = os.path.join(embeddings_folder, pickle_file_name)

        with open(pickle_file_path, 'wb') as f:
            pickle.dump(knowledge_base, f)

        st.success(f"File processed and stored as pickle: {pickle_file_name}")

    elif file_type == 'csv':
        # Process the CSV file and create the knowledge base
        # Store it as a pickle file using a similar approach as above
        pass

def main():
    st.set_page_config(page_title="Ask me something 🧞‍♂️")
    st.header("Ask me anything about the uploaded file 🧞‍♂️")

    file = st.file_uploader("Upload a file", type=("pdf", "csv", "pkl"))
    embeddings_folder = "/Users/felipemarques/Documents/GitHub/whitelabel-llm-agents/pickles"

    llm = OpenAI(temperature=0)  # Define llm outside the file upload condition

    # Process and store pickle button
    if file is not None:
        file_type = file.type.split('/')[1]

        # Check if file is pickle
        if file_type == 'pkl':
            # load and use your pickle file
            knowledge_base = pickle.load(file)

    if file is not None or st.button("Process and Store as Pickle"):
        file_type = file.type.split('/')[1]

        st.write("---")
        pickle_files = [file for file in os.listdir(embeddings_folder) if file.endswith(".pkl")]
        selected_pickle_file = st.selectbox("Choose a pickle file as the prompt", pickle_files)

        if selected_pickle_file:
            selected_pickle_file_path = os.path.join(embeddings_folder, selected_pickle_file)
            with open(selected_pickle_file_path, 'rb') as f:
                knowledge_base = pickle.load(f)

        if file_type == 'pdf':
            pdf_reader = PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()

            text_splitter = CharacterTextSplitter(
                separator="\n", 
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text)
            embeddings = OpenAIEmbeddings()

            if not selected_pickle_file:
                knowledge_base = FAISS.from_texts(chunks, embeddings)

            user_question = st.text_input("Ask me a question about the pdf")
            if user_question and knowledge_base:
                docs = knowledge_base.similarity_search(user_question)

                chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
                with get_openai_callback() as cb:
                    response = chain.run(input_documents=docs, question=user_question)
                    print(cb)
                
                # Clear the output before displaying the response
                st.empty()
                st.write(response)
        
        elif file_type == 'csv':
            user_question = st.text_input("Ask me a question about the csv")

            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False)

            # Write the contents of the uploaded file into the temporary file
            temp_file.write(file.read())

            # Close the temporary file to ensure data is saved
            temp_file.close()

            agent = create_csv_agent(llm=llm, path=temp_file.name, verbose=True)

            if user_question is not None and user_question != "":
                with get_openai_callback() as cb:
                    output = agent.run(input=user_question)
                    print(cb)
                
                # Clear the output before displaying the response
                st.empty()
                st.write(output)

            # Delete the temporary file after usage
            os.remove(temp_file.name)

    else:
        st.write("---")
        pickle_files = [file for file in os.listdir(embeddings_folder) if file.endswith(".pkl")]
        if pickle_files:
            selected_pickle_file = st.selectbox("Choose a pickle file as the prompt", pickle_files)
            if selected_pickle_file:
                selected_pickle_file_path = os.path.join(embeddings_folder, selected_pickle_file)
                with open(selected_pickle_file_path, 'rb') as f:
                    knowledge_base = pickle.load(f)

                user_question = st.text_input("Ask me a question")
                if user_question and knowledge_base:
                    docs = knowledge_base.similarity_search(user_question)

                    chain = load_qa_chain(llm, chain_type="stuff", verbose=True)
                    with get_openai_callback() as cb:
                        response = chain.run(input_documents=docs, question=user_question)
                        print(cb)
                    
                    # Clear the output before displaying the response
                    st.empty()
                    st.write(response)
        else:
            st.write("No pickle files available.")

if __name__ == '__main__':
    main()
