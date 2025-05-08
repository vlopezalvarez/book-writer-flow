#!/usr/bin/env python
import os
import time
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
import ollama

load_dotenv()

# -------------------- Models --------------------

class Chapter(BaseModel):
    title: str = ""
    content: str = ""

class BookState(BaseModel):
    topic: str = "Astronomy in 2025"
    total_chapters: int = 0
    titles: list[str] = []
    chapters: list[Chapter] = []

# -------------------- Flow Logic --------------------

class BookFlow:
    def __init__(self, llm_name: str):
        self.state = BookState()
        self.llm_name = llm_name

    def generate_outline(self):
        print(f"📘 Generating outline using {self.llm_name}...")
        prompt = f"Generate 5 chapter titles for a book about '{self.state.topic}'"
        response = ollama.chat(
            model=self.llm_name,
            messages=[{"role": "user", "content": prompt}]
        )
        lines = response['message']['content'].splitlines()
        self.state.titles = [line.strip("-•0123456789. ") for line in lines if line.strip()]
        self.state.total_chapters = len(self.state.titles)
        print("✅ Outline created")

    async def generate_chapters(self):
        print(f"✍️ Generating chapters using {self.llm_name}...")

        async def write_chapter(title):
            prompt = f"Write a chapter titled '{title}' for a book on '{self.state.topic}'."
            response = ollama.chat(
                model=self.llm_name,
                messages=[{"role": "user", "content": prompt}]
            )
            return Chapter(title=title, content=response['message']['content'])

        tasks = [asyncio.create_task(write_chapter(title)) for title in self.state.titles]
        chapters = await asyncio.gather(*tasks)
        self.state.chapters = chapters
        print("✅ All chapters generated")

    def save_book(self):
        filename = f"book_{self.llm_name.replace('/', '_').replace(':', '_')}.md"
        print(f"💾 Saving book to '{filename}'...")
        with open(filename, "w", encoding="utf-8") as f:
            for chapter in self.state.chapters:
                f.write(f"# {chapter.title}\n\n{chapter.content}\n\n")
        print(f"📚 Book saved to {filename}!")

        return filename

# -------------------- Entry Point --------------------

async def kickoff(llm_name: str, topic: str) -> tuple[str, float, int]:
    print(f"\n=== Generating book with {llm_name} ===")
    start_time = time.time()

    flow = BookFlow(llm_name)

    # Generate Outline
    flow.generate_outline()
    end_time = time.time()
    outline_duration = end_time - start_time
    print(f"\n=== generate_outline done (took {outline_duration:.2f}s) ===")

    # Generate Chapters
    await flow.generate_chapters()
    end_time = time.time()
    chapters_duration = end_time - start_time
    print(f"\n=== generate_chapters done (took {chapters_duration:.2f}s) ===")

    # Save the Book and calculate file size
    filename = flow.save_book()
    file_size_kb = Path(filename).stat().st_size / 1024

    total_duration = outline_duration + chapters_duration
    print(f"{llm_name} took {total_duration:.2f}s and produced {file_size_kb:.1f} KB")
    return filename, total_duration, file_size_kb

async def main():
    topic = "Astronomy in 2025"
    llms = ["gemma:latest", "mistral:latest", "llama3.1:latest", "deepseek-r1:latest"]
    results = []

    for llm in llms:
        result = await kickoff(llm, topic)
        results.append(result)

    print("\n=== Summary ===")
    for name, duration, size in results:
        print(f"{name}: {duration:.2f}s, {size:.1f} KB")

if __name__ == "__main__":
    asyncio.run(main())


