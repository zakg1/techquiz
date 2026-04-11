import ollama

def test_llama():
    print("🔍 Testing Llama 3...")

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": "Hello Llama, are you working?"}]
    )

    print("🧠 Llama Response:")
    print(response["message"]["content"])


if __name__ == "__main__":
    test_llama()
