from tqdm import tqdm
import pandas as pd
from langchain.evaluation import load_evaluator
from langchain_openai import ChatOpenAI

from config.config import OpenAIConfig

df = pd.read_csv('./Q&A-seedlist.csv')

accuracy_criteria = {
    "accuracy": """
    Score 1: The answer is completely unrelated to the reference.
    Score 3: The answer has minor relevance but does not align with the reference.
    Score 5: The answer has moderate relevance but contains inaccuracies.
    Score 7: The answer aligns with the reference but has minor errors or omissions.
    Score 10: The answer is completely accurate and aligns perfectly with the reference."""
}

evaluator = load_evaluator(
    "labeled_score_string",
    criteria=accuracy_criteria,
    llm=ChatOpenAI(model="gpt-4", api_key=OpenAIConfig.api_key),
    normalize_by=10
)

results = []
for i, row in tqdm(df.iterrows()):
    eval_result = evaluator.evaluate_strings(
        prediction=row["candidate's Answer"],
        reference=row['Answer (Ground Truth)'],
        input=row['Question']
    )
    print(eval_result)
    results.append(eval_result)

pd.DataFrame(results).to_csv("eval_results.csv", index=False)

scores = [1 if result['score'] > 0.5 else 0 for result in results]

print("Accuracy: ", (sum(scores) / len(scores))*100)