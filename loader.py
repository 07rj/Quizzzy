import os
import importlib

BASE = "questions"


# =====================================================
# LEVELS
# =====================================================
def get_levels():

    if not os.path.exists(BASE):
        return []

    return sorted([
        item for item in os.listdir(BASE)
        if os.path.isdir(os.path.join(BASE, item))
        and not item.startswith("__")
        and item != "__pycache__"
    ])


# =====================================================
# SUBJECTS
# =====================================================
def get_subjects(level):

    if not isinstance(level, str):
        return []

    path = os.path.join(BASE, level)

    if not os.path.exists(path):
        return []

    return sorted([
        item for item in os.listdir(path)
        if os.path.isdir(os.path.join(path, item))
        and not item.startswith("__")
        and item != "__pycache__"
    ])


# =====================================================
# MOCKS
# =====================================================
def get_mocks(level, subject):

    if not isinstance(level, str):
        return []

    if not isinstance(subject, str):
        return []

    path = os.path.join(BASE, level, subject)

    if not os.path.exists(path):
        return []

    return sorted([
        file.replace(".py", "")
        for file in os.listdir(path)
        if file.startswith("mock_")
        and file.endswith(".py")
    ])


# =====================================================
# LOAD QUESTIONS
# =====================================================
def load_questions(level, subject, mock):

    if not all([level, subject, mock]):
        return []

    module_path = f"{BASE}.{level}.{subject}.{mock}"

    try:
        module = importlib.import_module(module_path)

        questions = getattr(module, "questions", [])

        if not isinstance(questions, list):
            return []

        return questions

    except ModuleNotFoundError:
        return []

    except Exception:
        return []