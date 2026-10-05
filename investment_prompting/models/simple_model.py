class SimpleModel:
  '''
  Simulates training with examples
  '''
  def __init__(self):
    self.examples = []

  def append_example(self, example):
    self.examples.append(example)

  def few_shot_prompting(self, prompt: str) -> str:

    if not self.examples:
      return (
        "There were no examples provided."
      )

    return (
      f"{len(self.examples)} provided."
      f"Few shot examples to process: "
      f"{prompt}"
    )