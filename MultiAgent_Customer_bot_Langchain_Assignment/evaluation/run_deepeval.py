# evaluation/run_deepeval.py

import os
from dotenv import load_dotenv

# ------------------------------------------------------------------
# 1. Load .env EXPLICITLY (required for python -m)
# ------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

ENV_PATH = os.path.join(PROJECT_ROOT, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

# Fail fast if not loaded
assert os.getenv("OPENAI_API_KEY"), "❌ AZURE_OPENAI_API_KEY not loaded"
assert os.getenv("OPENAI_API_TYPE"), "❌ Not using Azure OpenAI"

print("✅ Azure OpenAI environment loaded")

# ------------------------------------------------------------------
# 2. Imports AFTER env is loaded
# ------------------------------------------------------------------
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.models import GPTModel

from graph.workflow import build_graph

# ------------------------------------------------------------------
# 3. Build LangGraph
# ------------------------------------------------------------------
graph = build_graph()

# ------------------------------------------------------------------
# 4. DeepEval Judge (Azure-compatible)
# ------------------------------------------------------------------
azure_judge = GPTModel(model="gpt-4o")

relevancy_metric = AnswerRelevancyMetric(
    threshold=0.6,
    model=azure_judge
)

# ------------------------------------------------------------------
# 5. Evaluation Dataset
# ------------------------------------------------------------------
test_data = [
    {
        "question": "How can I reset my password?",
        "expected": "User should be guided to reset password using forgot password option."
    },
    {
        "question": "My account is locked. What should I do?",
        "expected": "User should be instructed to contact support or unlock account."
    }
]

# ------------------------------------------------------------------
# 6. Run Evaluation
# ------------------------------------------------------------------
for item in test_data:
    print("\n==============================")
    print("QUESTION:", item["question"])

    result = graph.invoke({
    "question": item["question"]
})

    final_answer = result["answer"]

    print("ANSWER:", final_answer)

    test_case = LLMTestCase(
        input=item["question"],
        actual_output=final_answer,
        expected_output=item["expected"]
    )

    relevancy_metric.measure(test_case)

    print("Relevancy Score:", relevancy_metric.score)
    print("Reason:", relevancy_metric.reason)

print("\n✅ DeepEval completed successfully")

