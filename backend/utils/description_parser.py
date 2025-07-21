import re

def parse_biology_description(text: str):
    """
    Divide a descrição 'Biology' em características físicas, comportamento e habitat.
    """
    physical, behavior, habitat = [], [], []

    # Normalizar texto
    text = text.replace("\n", " ")

    # Heurísticas simples para separar
    sentences = re.split(r'(?<=[.!?]) +', text)
    for s in sentences:
        s_lower = s.lower()
        if any(word in s_lower for word in ["color", "feather", "wing", "tail", "body", "appearance", "claw", "size"]):
            physical.append(s)
        elif any(word in s_lower for word in ["fly", "hunt", "attack", "behavior", "known to", "aggressive", "gentle"]):
            behavior.append(s)
        elif any(word in s_lower for word in ["habitat", "climate", "found in", "lives", "regions", "fields", "ocean"]):
            habitat.append(s)
        else:
            behavior.append(s)  # default

    return " ".join(physical), " ".join(behavior), " ".join(habitat)
