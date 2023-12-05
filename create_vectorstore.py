from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders.csv_loader import CSVLoader

# Load data
loader = CSVLoader(
    file_path='data/scopus.csv',
    source_column='EID',
        csv_args={
        "delimiter": ",",
    },
)
data = loader.load()

# Create vectorstore
embeddings_model_name = "sentence-transformers/all-mpnet-base-v2"
embeddings = HuggingFaceEmbeddings(
    model_name=embeddings_model_name
) 
vectorstore = FAISS.from_documents(
    data, 
    embeddings,
)
vectorstore.save_local("data/faiss_db")
print("Created vectorstore!")