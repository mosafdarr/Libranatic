from enum import Enum


class TestProvider(Enum):
    TEST1 = "test1"
    TEST2 = "test2"
    TEST3 = "test3"


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GEMINI = "gemini"
    GROQ = "groq"
    HUGGINGFACE = "huggingface"
