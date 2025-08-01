import requests
from typing import List, Any

class EmbedderClient:
    def __init__(self, endpoint: str = "http://localhost:8000/embed", timeout: int = 30):
        """
        :param endpoint: URL of the embedding service
        :param timeout: request timeout in seconds
        """
        self.endpoint = endpoint
        self.timeout = timeout

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Send a list of text chunks to the embedding service and return their vectors.
        :param texts: list of cleaned text strings to embed
        :return: list of embedding vectors (each a list of floats)
        """
        payload = {"texts": texts}
        try:
            resp = requests.post(self.endpoint, json=payload, timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(f"Embedding request failed: {e}") from e

        data = resp.json()
        if "vectors" not in data:
            raise RuntimeError(f"Unexpected response format: {data}")
        return data["vectors"]

if __name__ == "__main__":
    # Example usage
    client = EmbedderClient()
    chunks = [
        "hello world",
        "otedy qokeedy qokedy"
    ]
    embeddings = client.embed_texts(chunks)
    for i, emb in enumerate(embeddings):
        print(f"Chunk {i} → {len(emb)}‑dim vector")
