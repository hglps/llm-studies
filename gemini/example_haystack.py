from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack_integrations.components.generators.google_ai import GoogleAIGeminiGenerator
from haystack.components.builders import PromptBuilder
from haystack.dataclasses import ChatMessage


class SimpleRAG:
    def __init__(self):
        self.document_store = InMemoryDocumentStore()
        self.document_store.write_documents([
            Document(content="My name is Jean and I live in Paris."),
            Document(content="My name is Mark and I live in Berlin."),
            Document(content="My name is Giorgio and I live in Rome.")
        ])
        self.prompt_template = """
        You are a helpful assistant.
        Given these documents, answer the question.
        Documents:
        {% for doc in documents %}
        {{ doc.content }}
        {% endfor %}
        Question: {{question}}
        Answer:
        """
        self.prompt_builder = PromptBuilder(template=self.prompt_template, required_variables=["question", "documents"])
        self.retriever = InMemoryBM25Retriever(document_store=self.document_store)
        self.llm = GoogleAIGeminiGenerator(
            model="gemini-2.0-flash",
            api_key=Secret.from_env_var("GEMINI_API_KEY")
        )

        self.rag_pipeline = Pipeline()
        self.rag_pipeline.add_component("retriever", self.retriever)
        self.rag_pipeline.add_component("prompt_builder", self.prompt_builder)
        self.rag_pipeline.add_component("llm", self.llm)
        self.rag_pipeline.connect("retriever", "prompt_builder.documents")
        self.rag_pipeline.connect("prompt_builder", "llm")
        
    def __call__(self, retriever, prompt_builder):
        results = self.rag_pipeline.run(
            {"retriever": {"query": retriever["query"]},
            "prompt_builder": {"question": prompt_builder["question"]},
            }
        )
        return results["llm"]["replies"]

rag_system = SimpleRAG()
question = "Who lives in Paris?"
prompt = {
    "retriever": {"query": question},
    "prompt_builder": {"question": question}
}
response = rag_system(**prompt)
print(response)
