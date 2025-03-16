import glob
import os
from typing import Dict

import pandas as pd


def parse_integration_metadata(content: str) -> Dict[str, str]:
    """
    Parse metadata (title, author, date) and content from blogpost text.
    :param content: str, the content of the blogpost.
    :return: dict, a dictionary containing the metadata and content of the blogpost.
    """
    metadata = {}
    lines = content.splitlines()
    content_start_idx = 0

    for idx, line in enumerate(lines):
        if line.startswith('>>>>PROVIDER>>>>'):
            metadata['provider'] = line.replace('>>>>PROVIDER>>>>', '').strip()
        elif line.startswith('>>>>INTEGRATION_NAME>>>>'):
            metadata['Name'] = line.replace('>>>>INTEGRATION_NAME>>>>', '').strip()
        elif line.startswith('>>>>LICENSE>>>>'):
            metadata['license'] = line.replace('>>>>LICENSE>>>>', '').strip()
            content_start_idx = idx + 1
            break

    metadata['content'] = '\n'.join(lines[content_start_idx:]).strip()

    return metadata


def load_integrations(integration_folder: str) -> pd.DataFrame:
    """
    Given the integration folder, load all integration files into a DataFrame.
    :param integration_folder: str, the folder where the blogpost files are located.
    :return: pd.DataFrame, a DataFrame containing the integration files.
    """
    pattern = os.path.join(integration_folder, '*.md')
    integration_files = glob.glob(pattern)

    data = []
    for integration_file in integration_files:
        with open(integration_file, 'r', encoding='utf-8') as file:
            content = file.read()
            metadata = parse_integration_metadata(content)
            metadata['filename'] = os.path.basename(integration_file)
            data.append(metadata)

    return pd.DataFrame(data)
