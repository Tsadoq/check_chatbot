import os
import glob
import re
from typing import Dict, List, Tuple

import pandas as pd
from tqdm.auto import tqdm


def parse_blog_metadata(content: str) -> Dict[str, str]:
    """
    Parse metadata (title, author, date) and content from blogpost text.
    :param content: str, the content of the blogpost.
    :return: dict, a dictionary containing the metadata and content of the blogpost.
    """
    metadata = {}
    lines = content.splitlines()
    content_start_idx = 0

    for idx, line in enumerate(lines):
        if line.startswith('>>>>TITLE>>>>'):
            metadata['title'] = line.replace('>>>>TITLE>>>>', '').strip()
        elif line.startswith('>>>>AUTHOR>>>>'):
            metadata['author'] = line.replace('>>>>AUTHOR>>>>', '').strip()
        elif line.startswith('>>>>DATE>>>>'):
            metadata['date'] = line.replace('>>>>DATE>>>>', '').strip()
            content_start_idx = idx + 1
            break

    metadata['content'] = '\n'.join(lines[content_start_idx:]).strip()
    return metadata


def chunk_markdown_sections(text: str) -> List[Tuple[str, str]]:
    """
    Split markdown text into chunks based on section headers.
    Each header line starts with '#' (e.g. "# Section Title").
    If there is text before any header, label it as 'Introduction'.

    :param text: str, markdown content.
    :return: List of tuples where each tuple is (section, chunk_text).
    """
    lines = text.splitlines()
    chunks = []

    current_section = "Introduction" if lines and not re.match(r'^#\s+', lines[0]) else None
    current_chunk_lines = []

    for line in lines:
        if re.match(r'^#\s+', line):
            if current_chunk_lines or current_section is not None:
                chunk_text = "\n".join(current_chunk_lines).strip()
                if chunk_text:
                    chunks.append((current_section, chunk_text))
            current_section = line.lstrip('#').strip()
            current_chunk_lines = []
        else:
            current_chunk_lines.append(line)

    chunk_text = "\n".join(current_chunk_lines).strip()
    if chunk_text:
        chunks.append((current_section, chunk_text))

    return chunks


def load_blogposts_chunks(blog_folder: str) -> pd.DataFrame:
    """
    Load blogpost files from a folder and chunk them by markdown sections.
    Each row of the returned DataFrame corresponds to a chunk from the blogpost,
    including the full text (in 'complete_text'), metadata, the chunk text (in 'chunk'),
    and the section header (in 'section').

    :param blog_folder: str, the folder where the blogpost markdown files are located.
    :return: pd.DataFrame, a DataFrame containing one row per section chunk.
    """
    pattern = os.path.join(blog_folder, '*.md')
    blog_files = glob.glob(pattern)
    data = []

    for blog_file in tqdm(blog_files, desc="Loading blogposts"):
        with open(blog_file, 'r', encoding='utf-8') as file:
            content = file.read()
            metadata = parse_blog_metadata(content)
            metadata['filename'] = os.path.basename(blog_file)
            metadata['filepath'] = blog_file
            chunks = chunk_markdown_sections(metadata['content'])
            for section, chunk in chunks:
                row = metadata.copy()
                row['section'] = section
                row['chunk'] = chunk
                data.append(row)

    return pd.DataFrame(data)
