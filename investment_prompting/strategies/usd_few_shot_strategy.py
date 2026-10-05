from .usd_prompting_strategy import UsdPromptingStrategy

from investment_prompting.models.simple_model import (
    SimpleModel,
)


class UsdFewShotStrategy(UsdPromptingStrategy):
    """
    Uses example prompt-response pairs to guide
    SimpleModel when a new prompt is processed.
    """

    def __init__(
        self,
        model: SimpleModel,
        examples: list,
    ):
        self.model = model
        self.examples = examples

    def execute(self, prompt: str) -> str:
        """
        Train the SimpleModel with the supplied examples
        and generate a prediction for the target prompt.
        """

        # Add supplied examples to the model
        for example in self.examples:

            if example not in self.model.examples:
                self.model.append_example(example)

        # Generate prediction
        prediction = self.model.few_shot_prompting(
            prompt
        )

        return prediction