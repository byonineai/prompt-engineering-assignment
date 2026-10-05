from .usd_prompting_strategy import UsdPromptingStrategy


class UsdChainOfThoughtStrategy(UsdPromptingStrategy):
    """
    Calculates yearly investment value.

    The calculation records each financial calculation step, so
    the final result can be inspected
    """

    # Wrapper method
    def chain_of_thought(prompt):
      strategy = UsdChainOfThoughtStrategy()
      return strategy.execule(prompt)

    def execute(self, prompt: dict) -> dict:

        initial_amount = prompt["initial_amount"]
        annual_return = prompt["annual_return"]
        annual_fee = prompt["annual_fee"]
        tax_rate = prompt["tax_rate"]
        years = prompt["years"]

        balance = initial_amount

        result_logs = []

        for year in range(1, years + 1):

            beginning_balance = balance

            # Return on investment
            earned_return = beginning_balance * annual_return

            # Tax applied to the return on investment
            tax_deducted = earned_return * tax_rate

            # Balance after taxes and return
            balance_after_taxes = beginning_balance + earned_return - tax_deducted

            # Annual fee
            deducted_fee = balance_after_taxes * annual_fee

            # Final year balance
            ending_balance = balance_after_taxes - deducted_fee

            result_logs.append(
                {
                    "year": year,
                    "beginning_balance": round(beginning_balance, 2),
                    "earned_return": round(earned_return, 2),
                    "tax_deducted": round(tax_deducted, 2),
                    "deducted_fee": round(deducted_fee, 2),
                    "ending_balance": round(ending_balance, 2),
                }
            )

            balance = ending_balance

        return {"strategy":"Chain of Thought","final_value": round(balance, 2), "result_logs": result_logs}
