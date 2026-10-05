import math

from investment_prompting.strategies.usd_prompting_strategy import (
    UsdPromptingStrategy,
)

class UsdSelfConsistencyStrategy(UsdPromptingStrategy):
    """
    Calculates the investment using two independent methods
    and compares the results for consistency.
    """

    def self_consistency_chain_of_thought(prompt):
      strategy = UsdSelfConsistencyStrategy()
      return strategy.execute(prompt)

    def execute(self, prompt: dict) -> dict:

        method_one_result, method_one_logs = (
            self._reasoning_method_one(prompt)
        )

        method_two_result, method_two_logs = (
            self._reasoning_method_two(prompt)
        )

        consistency = math.isclose(
            method_one_result,
            method_two_result,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

        return {
            "strategy": "self_consistency",
            "reasoning_method_one": round(
                method_one_result,
                2,
            ),
            "reasoning_method_two": round(
                method_two_result,
                2,
            ),
            "existent_consistency": consistency,
            "difference": round(
                abs(
                    method_one_result
                    - method_two_result
                ),
                10,
            ),
            "method_one_logs": method_one_logs,
            "method_two_logs": method_two_logs,
        }

    def _reasoning_method_one(
        self,
        prompt: dict,
    ) -> tuple[float, list]:

        balance = prompt["initial_amount"]
        annual_return = prompt["annual_return"]
        annual_fee = prompt["annual_fee"]
        tax_rate = prompt["tax_rate"]
        years = prompt["years"]

        logs = []

        for year in range(1, years + 1):

            beginning_balance = balance

            return_earned = (
                annual_return
                * beginning_balance
            )

            tax_deducted = (
                tax_rate
                * return_earned
            )

            balance_after_taxes = (
                beginning_balance
                + return_earned
                - tax_deducted
            )

            deducted_fee = (
                annual_fee
                * balance_after_taxes
            )

            balance = (
                balance_after_taxes
                - deducted_fee
            )

            logs.append(
                {
                    "year": year,
                    "beginning_balance": round(
                        beginning_balance,
                        2,
                    ),
                    "return_earned": round(
                        return_earned,
                        2,
                    ),
                    "tax_deducted": round(
                        tax_deducted,
                        2,
                    ),
                    "deducted_fee": round(
                        deducted_fee,
                        2,
                    ),
                    "ending_balance": round(
                        balance,
                        2,
                    ),
                }
            )

        return balance, logs

    def _reasoning_method_two(
        self,
        prompt: dict,
    ) -> tuple[float, dict]:

        initial_amount = prompt["initial_amount"]
        annual_return = prompt["annual_return"]
        annual_fee = prompt["annual_fee"]
        tax_rate = prompt["tax_rate"]
        years = prompt["years"]

        reasoning_growth_factor = (
            1
            + annual_return
            * (1 - tax_rate)
        ) * (1 - annual_fee)

        result = (
            initial_amount
            * reasoning_growth_factor ** years
        )

        logs = {
            "initial_amount": initial_amount,
            "annual_return": annual_return,
            "tax_rate": tax_rate,
            "annual_fee": annual_fee,
            "years": years,
            "growth_factor": round(
                reasoning_growth_factor,
                6,
            ),
            "final_value": round(
                result,
                2,
            ),
        }

        return result, logs
