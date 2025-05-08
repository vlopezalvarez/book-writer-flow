# 📝 Book Writer Flow (Ollama Edition)

This project is a modified version of [book-writer-flow](https://github.com/patchy631/ai-engineering-hub/tree/main/book-writer-flow), adapted to work **locally using Ollama** and extended to **benchmark multiple local LLMs** for book generation.

## 🔄 Changes from Original

- ✅ Replaced OpenAI with **local LLMs via [Ollama](https://ollama.com)**.
- ✅ Bright Data removed. No web scraping or external data retrieval: Bright Data is used for web scraping and proxy-based data gathering. None of that functionality is included in this version.
- ✅ Works fully offline (once models are downloaded).
- ✅ Benchmarks multiple local models (e.g., LLaMA, Mistral, DeepSeek, Gemma) by comparing:
  - Time taken to generate a full book
  - Output file size in KB
- ✅ Outputs books in Markdown format and optionally as PDF.


## 🚀 How It Works

1. Prompts an LLM to generate a book outline (chapter titles).
2. Asynchronously generates each chapter using the selected model.
3. Saves the final book in `.md` format.
4. Repeats the process for each installed LLM and records timing and output size.

## Run the project

Finally, head over to this folder:
```
cd book_flow/book_writing_flow/src
```

and run the project by running the following command:

```bash
python book_writing_flow/main.py
```

## Sample Output

The book produced by the workflow on "Astronomy in 2025" is shown here: [Sample book](Final_book.pdf)

## 📊 Benchmark Output

Example benchmark summary (Apple M1):

```
=== Summary ===
book_gemma_latest.md: 1324.19s, 13.5 KB
book_mistral_latest.md: 1209.29s, 24.0 KB
book_llama3.1_latest.md: 1270.37s, 26.8 KB
book_deepseek-r1_latest.md: 28872.98s, 205.5 KB
```

You can compare the Markdown files to analyze the content quality across models.

## 🧠 Requirements

- Python 3.10+
- [Ollama](https://ollama.com) installed with the models you want to benchmark:
  ```bash
  ollama pull llama3.1
  ollama pull mistral
  ollama pull gemma
  ollama pull deepseek-r1
  ```
- Python libraries

  ```
  pip install ollama pydantic python-dotenv
  ```

Script uses standard libraries like os, time, asyncio, and pathlib.

## ▶️ Run the Benchmark
```python book_writing_flow/main.py```
Books will be saved as book_<model>.md files in the current directory.

## 📄 License
This project follows the same license as the original book-writer-flow, with modifications for local execution and benchmarking.

Let me know if you'd like a section for screenshots, PDF conversion instructions, or a chart comparing generation speed and size per model.


