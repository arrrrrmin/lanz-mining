"""A keyword anaylsis of talkshow guests, supported by zero-shot classification.
The used model was published by: Sahaj Tomar, https://github.com/Sahajtomar
The model can be found at huggingface: https://huggingface.co/Sahajtomar/German_Zeroshot
"""

from typing import Union

from transformers import pipeline, Pipeline

TOPICS = [
    "Außenpolitik",
    "Innenpolitik",
    "Sicherheit",
    "Energie",
    "Gesundheit",
    "Digitales",
    "Russland",
    "Ukraine",
    "Nahost",
    "Migration",
    "Wirtschaft",
    # "Journalismus",
    "Klima",
    "Bildung",
    "Rechtliches",
    "Soziales",
]
MODEL_TAG = "Sahajtomar/German_Zeroshot"
MODEL_TASK = "zero-shot-classification"
HYPO_TEMPLATE = "Zu geladene Person äußert sich zu {}."


def get_classifier_pipeline() -> Pipeline:
    return pipeline(MODEL_TASK, model=MODEL_TAG)


def run_pipeline(sequences: Union[list[str], str], classifier: Pipeline) -> list[dict[str, float]]:
    if isinstance(sequences, str):
        sequences = [sequences]
    result_list = classifier(sequences, TOPICS, hypothesis_template=HYPO_TEMPLATE)
    # Maybe add a threshold to cut off probs?
    return [
        {label: result["scores"][i] for i, label in enumerate(result["labels"])}
        for result in result_list
    ]
