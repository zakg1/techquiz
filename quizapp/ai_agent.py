import ollama
import json

def call_ai_generate_questions(text, num_questions):
    prompt = f"""
    اقرأ النص التالي واستخرج منه {num_questions} أسئلة اختيار من متعدد (MCQ).
    كل سؤال يجب أن يكون بصيغة JSON كالتالي:

    {{
        "question": "...",
        "options": [
            {{"text": "...", "isCorrect": false}},
            {{"text": "...", "isCorrect": false}},
            {{"text": "...", "isCorrect": false}},
            {{"text": "...", "isCorrect": true}}
        ]
    }}

    النص:
    {text}

    أعد الإجابة بصيغة JSON فقط.
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response["message"]["content"])


def call_ai_grade_answers(questions, answers):
    prompt = f"""
    هذه أسئلة الامتحان مع إجابات الطالب.
    أريد منك حساب عدد الإجابات الصحيحة فقط.

    الأسئلة:
    {json.dumps(questions, ensure_ascii=False)}

    إجابات الطالب:
    {json.dumps(answers, ensure_ascii=False)}

    أعد النتيجة بصيغة JSON:
    {{
        "score": 0
    }}
    """

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response["message"]["content"])