import os
import glob
import re
from typing import Dict, List, Tuple

import pandas as pd
from tqdm.auto import tqdm


def clean_asciidoc_content(content: str) -> str:
    """
    Cleans non-human-readable AsciiDoc metadata and conditional directives from content.

    :param content: str, the content of the AsciiDoc file.
    :return: str, the cleaned content.
    """
    lines = content.splitlines()
    cleaned_lines = []
    skip_lines = False

    for line in lines:
        if (line.startswith('//') or line.startswith('include::') or line.startswith(':') or
                line.startswith('ifdef::') or line.startswith('endif::[]')):
            continue
        elif line.startswith('{') and line.endswith('}'):
            continue
        elif line.startswith('{related-start}'):
            skip_lines = True
        elif line.startswith('{related-end}'):
            skip_lines = False
        elif not skip_lines:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()


def chunk_asciidoc_sections(text: str) -> List[Tuple[str, str]]:
    """
    Split AsciiDoc text into chunks based on section markers.
    A section marker is a line matching the pattern [#something].
    If there is text before the first section marker, it is labeled as "Introduction."

    :param text: str, cleaned AsciiDoc content.
    :return: List of tuples (section, chunk_text)
    """
    lines = text.splitlines()
    chunks = []

    current_section = "Introduction" if lines and not re.match(r'^\[#.+?\]', lines[0]) else None
    current_chunk_lines = []

    for line in lines:
        if re.match(r'^\[#(.+?)\]', line):
            if current_chunk_lines or current_section is not None:
                chunk_text = "\n".join(current_chunk_lines).strip()
                if chunk_text:
                    chunks.append((current_section, chunk_text))
            match = re.match(r'^\[#(.+?)\]', line)
            current_section = match.group(1).strip()
            current_chunk_lines = []
        else:
            current_chunk_lines.append(line)

    # Flush the final chunk
    chunk_text = "\n".join(current_chunk_lines).strip()
    if chunk_text:
        chunks.append((current_section, chunk_text))

    return chunks


def load_asciidoc_files_chunks(root_folder: str) -> pd.DataFrame:
    """
    Load all AsciiDoc files from 'en' subfolders under the given root folder, clean their content,
    and split each file into chunks based on section markers.

    Each row in the returned DataFrame corresponds to a section chunk and includes:
      - 'complete_text': the entire cleaned file text,
      - 'chunk': the chunk corresponding to one section,
      - 'section': the section identifier (extracted from the [#...]-style marker),
      - Metadata such as 'filename' and 'folder'.

    :param root_folder: str, the root folder where the AsciiDoc files are located.
    :return: pd.DataFrame containing one row per section chunk.
    """
    pattern = os.path.join(root_folder, '**/en/*.asciidoc')
    asciidoc_files = glob.glob(pattern, recursive=True)
    data = []

    for doc_file in tqdm(asciidoc_files, desc='Loading Documentation AsciiDoc files'):
        with open(doc_file, 'r', encoding='utf-8') as file:
            content = file.read()
            cleaned_content = clean_asciidoc_content(content)
            metadata = {
                'filename': os.path.basename(doc_file).split('.')[0],
                'folder': os.path.dirname(doc_file),
                'complete_text': cleaned_content
            }

            chunks = chunk_asciidoc_sections(cleaned_content)
            for section, chunk in chunks:
                row = metadata.copy()
                row['section'] = section
                row['chunk'] = chunk
                data.append(row)

    return pd.DataFrame(data)
