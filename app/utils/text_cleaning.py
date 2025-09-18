import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    
    #remove empty lines
    text = re.sub(r'\n{2,}', '\n', text)
    #remove citation brackets
    text = re.sub(r'\[\d+\]', '', text)
    #remove bullet points
    text = re.sub(r'•\s+', '', text)
    #remove numbered list items
    text = re.sub(r'^\s*[\d]+\.\s+', '', text, flags=re.MULTILINE)
    #normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    
    return text.strip()

def extract_specific_content(text: str, identifier: str, content_type: str = "section") -> str:
    if not text or not identifier:
        return text[:500] if text else "No content available"

    lines = text.split('\n')
    identifier_lower = identifier.lower().strip()

    if content_type == "figure":
        for i, line in enumerate(lines):
            if identifier_lower in line.lower() and ('figure' in line.lower() or 'fig' in line.lower()):
                start = max(0, i - 2)
                end = min(len(lines), i + 5)
                return '\n'.join(lines[start:end])

    elif content_type == "section":
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if identifier_lower in line_lower and len(line.strip()) < 150:
                return '\n'.join(lines[i:i + 15])
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if any(word in line_lower for word in identifier_lower.split()) and len(line.strip()) < 150:
                return '\n'.join(lines[i:i + 15])
    
    # Default fallback if no specific content found
    return text[:500] if text else "No content available"
