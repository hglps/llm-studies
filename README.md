# LLM Studies and RAG Scripts Repository

This repository contains code and resources for studying large language models (LLMs) and implementing Retrieval-Augmented Generation (RAG) scripts.
The goal of this repository is to provide a collection of tools, experiments, and analyses related to the study of LLMs and their applications in RAG systems.

## Installation

To install the required dependencies, run:

```bash
conda create --name llm python=3.11
pip install torch numpy pandas chromadb sentence-transformers langchain
```

If running local models, also run:
```bash
pip install ollama
```

Docker Container: To be defined.

## Usage

### Running Experiments

In this project, we used redis as the broker for celery in WSL2.

Run:

```bash
sudo apt update
sudo apt install redis-server

sudo redis-server --daemonize yes

redis-cli ping

celery -A book_rag worker --loglevel=info
```

To be defined.

### Querying RAG Systems

To be defined.

## References

- [llm-course: Course to get into Large Language Models (LLMs) with roadmaps and Colab notebooks.](https://github.com/mlabonne/llm-course)
- [LLM-engineer-handbook: A curated list of Large Language Model resources, covering model training, serving, fine-tuning, and building LLM applications.](https://github.com/SylphAI-Inc/LLM-engineer-handbook)
- [DeepLearning.ai: LangChain for LLM Application Development](https://www.deeplearning.ai/short-courses/langchain-for-llm-application-development/)
- [HuggingFace: The LLM Course](https://huggingface.co/huggingface-course)
- [Build a simple LLM application with chat models and prompt templates](https://python.langchain.com/docs/tutorials/llm_chain/)
