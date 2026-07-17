from services.gemini_service import ask_gemini

print("=" * 60)
print("FoodExpress AI Test")
print("=" * 60)

while True:

    question = input("\nCustomer: ")

    if question.lower() in ["exit", "quit"]:
        print("\nGoodbye!")
        break

    reply = ask_gemini(question)

    print("\nFoodExpress AI:\n")
    print(reply)