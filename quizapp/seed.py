from quizapp.models import User, Specialization, Book,

def seed_data():
    User(username="zain", email="zain@test.com", password="123", role="student").save()
    User(username="admin", email="admin@test.com", password="admin", role="admin").save()

    Specialization(name="software", description="Software fundamentals").save()

    b = Book(
        title="Intro to CS",
        author="Unknown",
        specialization="software",
        file_path="books/intro.pdf",
        uploaded_by="admin",
        created_at="2024-01-01"
    ).save()

    Question(
        book_id=str(b.id),
        text="What is a computer?",
        options=[
            {"text": "A machine that processes data", "isCorrect": True},
            {"text": "A fruit", "isCorrect": False},
            {"text": "A car engine", "isCorrect": False}
        ],
        explanation="A computer processes information.",
        source_page="12",
        created_at="2024-01-01"
    ).save()

    print("Seed data inserted successfully!")
