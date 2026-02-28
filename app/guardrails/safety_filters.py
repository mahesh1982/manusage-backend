class SafetyFilters:
    @staticmethod
    def sanitize(text: str) -> str:
        banned = ["hate", "violence", "self-harm"]
        for word in banned:
            text = text.replace(word, "[filtered]")
        return text
