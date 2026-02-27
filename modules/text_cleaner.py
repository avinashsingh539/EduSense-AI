def clean_text(text: str) -> str:
    import re

    # Normalize spacing
    text = re.sub(r'\s+', ' ', text)

    # Remove fillers safely
    fillers = [
        r'\buh\b', r'\bum\b', r'\byou know\b',
        r'\bokay\b', r'\bright\b', r'\bso\b'
    ]
    for f in fillers:
        text = re.sub(f, '', text, flags=re.IGNORECASE)

    # Fix broken sentences
    text = re.sub(r'\s([?.!,])', r'\1', text)

    return text.strip()