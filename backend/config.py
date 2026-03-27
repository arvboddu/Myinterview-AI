import os


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
CHROMA_PATH = os.getenv("CHROMA_PATH", "vectorstore")
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-large-en")
TTS_HOST = os.getenv("TTS_HOST", "http://127.0.0.1:5002")
WHISPER_BIN = os.getenv("WHISPER_BIN", "whisper")
