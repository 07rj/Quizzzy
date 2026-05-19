import os
import importlib.util

BASE = "questions"


# =====================================================
# GET QUIZZES (quiz_1.a, quiz_1.b)
# =====================================================
def get_quiz(level, subject):

    path = os.path.join(BASE, level, subject)

    if not os.path.exists(path):
        return []

    quizzes = []

    for file in os.listdir(path):
        if file.startswith("quiz_") and file.endswith(".py"):
            quizzes.append(file.replace(".py", ""))

    return sorted(quizzes)


# =====================================================
# LOAD SINGLE QUIZ ONLY (NO MERGE)
# =====================================================
def load_questions(level, subject, quiz):

    file_path = os.path.join(BASE, level, subject, quiz + ".py")

    if not os.path.exists(file_path):
        return []

    spec = importlib.util.spec_from_file_location(quiz, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, "questions", [])