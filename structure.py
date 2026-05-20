# structure.py

LEVELS = {
    "foundation": {
        "name": "⚙️ Foundation",
        "subjects": {
            "ct": "Computational Thinking",
            "english_1": "English 1",
            "english_2": "English 2",
            "maths_1": "Maths 1",
            "maths_2": "Maths 2",
            "prog_python": "Programming In Python",
            "statistics_1": "Statistics 1",
            "statistics_2": "Statistics 2"
        }
    },

    "diploma_prog": {
        "name": "🧑🏼‍💻 Diploma In Programming",
        "subjects": {
            "app_dev_1": "Modern Application Development 1",
            "app_dev_2": "Modern Application Development 2",
            "dbms": "Database Management System",
            "java": "Programming Concepts Using JAVA",
            "pdsa": "PDSA Using Python",
            "sys_com": "System Commands"
        }
    },

    "diploma_ds": {
        "name": " 🐼 Diploma In Data Science",
        "subjects": {
            "ba": "Business Analytics",
            "bdm": "Business Data Management",
            "dl_gen_ai": "Deep Learning And Generative AI",
            "ml_f": "Machine Learning Foundation",
            "ml_p": "Machine Learning Practice",
            "ml_t": "Machine Learning Techniques",
            "tools_ds": "Tools In Data Science"
        }
    },

    "bsc": {
        "name": "📃 BSc Level",
        "subjects": {
            "big_data": "Big Data",
            "llm": "Large Language Models",
            "os": "Operating System",
            "prog_c": "Programming In C"
        }
    },

    "bs": {
        "name": "🎓 BS Level",
        "subjects": {
            "ai": "AI: Search Method",
            "dl": "Deep Learning",
            "sof_engin": "Software Engineering",
            "sof_test": "Software Testing"
        }
    }
}


# =====================================================
# SAFE ACCESS FUNCTION (IMPORTANT FIX)
# =====================================================
def get_level_data(level_key):
    """
    Always returns a safe dictionary.
    Prevents NoneType crashes in Streamlit.
    """
    return LEVELS.get(level_key, {
        "name": "Invalid Level",
        "subjects": {}
    })


# =====================================================
# OPTIONAL HELPERS
# =====================================================
def get_subjects(level_key):
    level_data = get_level_data(level_key)
    return level_data.get("subjects", {})


def get_level_name(level_key):
    return get_level_data(level_key).get("name", "Unknown Level")


def get_all_levels():
    return list(LEVELS.keys())