import language_tool_python
import json

tool = language_tool_python.LanguageTool('fr')

def correct_french(text):
    matches = tool.check(text)
    corrected = language_tool_python.utils.correct(text, matches)
    explanations = []
    for match in matches:
        explanations.append({
            "error": text[match.offset:match.offset + match.errorLength],
            "message": match.message,
            "suggestions": match.replacements
        })
    return corrected, explanations

def load_mistakes(path="mistakes.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
