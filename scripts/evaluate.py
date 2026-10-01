from app.rag import CricketRAG


test_cases = [

    {
        "question": "Who won the 2011 Cricket World Cup?",
        "expected": "India"
    },
    {
        "question": "Who was defeated by India in the 2011 World Cup final?",
        "expected": "Sri Lanka"
    },
    {
        "question": "Where was the 2011 World Cup final played?",
        "expected": "Wankhede Stadium"
    },
    {
        "question": "Which city hosted the 2011 World Cup final?",
        "expected": "Mumbai"
    },
    {
        "question": "Who scored 91 runs in the 2011 World Cup final?",
        "expected": "MS Dhoni"
    },
    {
        "question": "Who scored 97 runs in the 2011 World Cup final?",
        "expected": "Gautam Gambhir"
    },
    {
        "question": "Who was Player of the Tournament in the 2011 World Cup?",
        "expected": "Yuvraj Singh"
    },
    {
        "question": "How many runs did India score in the 2011 World Cup final?",
        "expected": "277"
    },

    {
        "question": "Who won the 2023 Cricket World Cup?",
        "expected": "Australia"
    },
    {
        "question": "Who did Australia defeat in the 2023 World Cup final?",
        "expected": "India"
    },
    {
        "question": "Where was the 2023 World Cup final played?",
        "expected": "Narendra Modi Stadium"
    },
    {
        "question": "Which city hosted the 2023 World Cup final?",
        "expected": "Ahmedabad"
    },
    {
        "question": "Who was Player of the Tournament in the 2023 World Cup?",
        "expected": "Virat Kohli"
    },
    {
        "question": "How many runs did Virat Kohli score in the 2023 World Cup?",
        "expected": "765"
    },
    {
        "question": "Who was India's captain in the 2023 World Cup?",
        "expected": "Rohit Sharma"
    },
    {
        "question": "Which country hosted the 2023 World Cup?",
        "expected": "India"
    },

    {
        "question": "Who won the 1983 Cricket World Cup?",
        "expected": "India"
    },
    {
        "question": "Who was India's captain in the 1983 World Cup?",
        "expected": "Kapil Dev"
    },
    {
        "question": "Where was the 1983 World Cup held?",
        "expected": "England"
    },
    {
        "question": "Which team did India defeat in the 1983 World Cup final?",
        "expected": "West Indies"
    },

    {
        "question": "When did India play its first Test match?",
        "expected": "1932"
    },
    {
        "question": "Which country did India play against in its first Test match?",
        "expected": "England"
    },
    {
        "question": "Who is an Indian wicketkeeper-batsman who scored 91 in the 2011 final?",
        "expected": "MS Dhoni"
    },
    {
        "question": "Who was the captain of India in limited-overs cricket according to the knowledge base?",
        "expected": "MS Dhoni"
    },
    {
        "question": "Who scored 97 runs in the 2011 final?",
        "expected": "Gautam Gambhir"
    },
    {
        "question": "Who was named Player of the Tournament in 2011?",
        "expected": "Yuvraj Singh"
    },

    {
        "question": "Who was named Player of the Tournament in 2023?",
        "expected": "Virat Kohli"
    },
    {
        "question": "Who was India's captain during the 2023 Cricket World Cup?",
        "expected": "Rohit Sharma"
    },
    {
        "question": "Which stadium hosted the 2023 World Cup final?",
        "expected": "Narendra Modi Stadium"
    },
    {
        "question": "Which stadium hosted the 2011 World Cup final?",
        "expected": "Wankhede Stadium"
    }
]


rag = CricketRAG()

correct = 0


print("\n" + "=" * 70)
print("CRICKET RAG EVALUATION")
print("=" * 70)


for i, test in enumerate(test_cases, start=1):

    question = test["question"]
    expected = test["expected"]

    result = rag.ask(question)

    answer = result["answer"]

    if expected.lower() in answer.lower():
        correct += 1
        status = "CORRECT"
    else:
        status = "INCORRECT"

    print(f"\nTest {i}")
    print(f"Question : {question}")
    print(f"Expected : {expected}")
    print(f"Answer   : {answer}")
    print(f"Status   : {status}")


accuracy = (correct / len(test_cases)) * 100


print("\n" + "=" * 70)
print(f"Correct answers : {correct}/{len(test_cases)}")
print(f"Accuracy        : {accuracy:.2f}%")
print("=" * 70)