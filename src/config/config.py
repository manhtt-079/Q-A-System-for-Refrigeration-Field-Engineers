import os
import logging
import logging.config
from dataclasses import dataclass, field
from configparser import ConfigParser

config = ConfigParser()
config.read("./config/config.ini")

os.makedirs(name=config["chat"]["log_dir"], mode=0o777, exist_ok=True)
logging.config.fileConfig("./config/logger.ini")
logger = logging.getLogger()


def get_logger():
    return logger

@dataclass
class EmbeddingConfig:
    pdf_dir: str = config["embedding"]["pdf_dir"]
    chunk_size: int = int(config["embedding"]["chunk_size"])
    chunk_overlap: int = int(config["embedding"]["chunk_overlap"])
    faiss_index: str = config["embedding"]["faiss_index"]
    split_mode: str = config["embedding"]["split_mode"]
    hf_embedding_model: str = config["embedding"]["hf_embedding_model"]

@dataclass
class OpenAIConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", config["openai"]["api_key"])
    embedding_model: str = config["openai"]["embedding_model"]
    chat_model: str = config["openai"]["chat_model"]
    max_retries: int = int(config["openai"]["max_retries"])
    temperature: float = float(config["openai"]["temperature"])


@dataclass
class AppConfig:
    host: str = config["app"]["host"]
    port: str = config["app"]["port"]
    debug: bool = True if config["app"]["debug"].lower() == "true" else False
    threaded: bool = True if config["app"]["threaded"].lower() == "true" else False
    qa_url: str = config["app"]["qa_url"]

@dataclass
class ChatConfig:
    log_dir: str = config["chat"]["log_dir"]
    max_history: int = int(config["chat"]["max_history"])

if __name__ == "__main__":
    pass
