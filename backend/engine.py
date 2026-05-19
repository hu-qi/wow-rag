import os
from typing import Any, Generator, List

import qdrant_client
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.llms import CompletionResponse, CustomLLM, LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.response_synthesizers import get_response_synthesizer
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.qdrant import QdrantVectorStore
from openai import OpenAI
from pydantic import Field


load_dotenv()


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Please copy backend/.env.example to backend/.env and fill in your own value."
        )
    return value


api_key = get_required_env("WOWRAG_API_KEY")
base_url = os.getenv("WOWRAG_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
chat_model = os.getenv("WOWRAG_CHAT_MODEL", "glm-4-flash")
emb_model = os.getenv("WOWRAG_EMBED_MODEL", "embedding-3")
docs_path = os.getenv("WOWRAG_DOCS_PATH", "../docs/问答手册.txt")
qdrant_path = os.getenv("WOWRAG_QDRANT_PATH", "qdrant")
qdrant_collection = os.getenv("WOWRAG_QDRANT_COLLECTION", "wenda")


class OurLLM(CustomLLM):
    api_key: str = Field(default=api_key)
    base_url: str = Field(default=base_url)
    model_name: str = Field(default=chat_model)
    client: OpenAI = Field(default=None, exclude=True)

    def __init__(self, api_key: str, base_url: str, model_name: str = chat_model, **data: Any):
        super().__init__(**data)
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(model_name=self.model_name)

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )
        if hasattr(response, "choices") and len(response.choices) > 0:
            response_text = response.choices[0].message.content
            return CompletionResponse(text=response_text)
        raise Exception(f"Unexpected response format: {response}")

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> Generator[CompletionResponse, None, None]:
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        try:
            for chunk in response:
                chunk_message = chunk.choices[0].delta
                if not chunk_message.content:
                    continue
                content = chunk_message.content
                yield CompletionResponse(text=content, delta=content)
        except Exception as exc:
            raise Exception(f"Unexpected response format: {exc}") from exc


class OurEmbeddings(BaseEmbedding):
    api_key: str = Field(default=api_key)
    base_url: str = Field(default=base_url)
    model_name: str = Field(default=emb_model)
    client: OpenAI = Field(default=None, exclude=True)

    def __init__(
        self,
        api_key: str = api_key,
        base_url: str = base_url,
        model_name: str = emb_model,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def invoke_embedding(self, query: str) -> List[float]:
        response = self.client.embeddings.create(model=self.model_name, input=[query])
        if response.data and len(response.data) > 0:
            return response.data[0].embedding
        raise ValueError("Failed to get embedding from API")

    def _get_query_embedding(self, query: str) -> List[float]:
        return self.invoke_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        return self.invoke_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return [self._get_text_embedding(text) for text in texts]

    async def _aget_query_embedding(self, query: str) -> List[float]:
        return self._get_query_embedding(query)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        return self._get_text_embedding(text)

    async def _aget_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        return self._get_text_embeddings(texts)


def create_query_engine() -> RetrieverQueryEngine:
    llm = OurLLM(api_key=api_key, base_url=base_url, model_name=chat_model)
    embedding = OurEmbeddings(api_key=api_key, base_url=base_url, model_name=emb_model)

    documents = SimpleDirectoryReader(input_files=[docs_path]).load_data()

    qclient = qdrant_client.QdrantClient(path=qdrant_path)
    vector_store = QdrantVectorStore(client=qclient, collection_name=qdrant_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embedding,
    )

    emb = embedding.get_text_embedding("你好呀呀")
    dimensions = len(emb)
    retriever = VectorIndexRetriever(
        similarity_top_k=5,
        index=index,
        dimensions=dimensions,
    )

    response_synthesizer = get_response_synthesizer(llm=llm, streaming=True)
    return RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
    )
