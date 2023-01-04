import re


def clear_text(text: str) -> str:
    clean_pattern = re.compile('<.*?>')
    cleaned_text = re.sub(clean_pattern, '', text)
    return ' '.join(cleaned_text.split())
