import spacy
from typing import Dict, Tuple

nlp = spacy.load("en_core_web_sm")

TARGET_ENTITIES = {"PERSON", "ORG", "GPE", "DATE", "MONEY"}

def sanitize_prompt(text: str) -> Tuple[str, Dict[str, str]]:
    doc = nlp(text)
    entity_counts: Dict[str, int] = {}
    mapping: Dict[str, str] = {}
    
    entities = sorted(doc.ents, key=lambda e: e.start_char, reverse=True)
    sanitized_text = text

    for ent in entities:
        if ent.label_ in TARGET_ENTITIES:
            label = ent.label_
            entity_counts[label] = entity_counts.get(label, 0) + 1
            placeholder = f"[{label}_{entity_counts[label]}]"
            mapping[placeholder] = ent.text
            sanitized_text = (
                sanitized_text[:ent.start_char] + 
                placeholder + 
                sanitized_text[ent.end_char:]
            )

    return sanitized_text, mapping

def rehydrate_response(response_text: str, session_vault: Dict[str, str]) -> str:
    rehydrated = response_text
    for placeholder, original_value in session_vault.items():
        rehydrated = rehydrated.replace(placeholder, original_value)
    return rehydrated
