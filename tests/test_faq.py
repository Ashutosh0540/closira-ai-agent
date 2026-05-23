from agents.faq_agent import FAQAgent


faq_agent = FAQAgent("data/sop.json")

while True:

    question = input("\nCustomer: ")

    if question.lower() == "exit":
        break

    result = faq_agent.answer_question(question)

    print("\nAI RESPONSE:")
    print(result)