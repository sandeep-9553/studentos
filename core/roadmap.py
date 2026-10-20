import json

def load_roles():
    with open("data/roles.json", encoding="utf-8") as f:
        return json.load(f)

def build_roadmap(role, current_skills, roles):
    """Return the stages the student still needs, and the ones already known."""
    have = {s.strip().lower() for s in current_skills}
    missing = [s for s in roles[role] if s["skill"].lower() not in have]
    known = [s for s in roles[role] if s["skill"].lower() in have]
    return missing, known