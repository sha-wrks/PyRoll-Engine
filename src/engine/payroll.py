"""Payroll calculation engine."""


class PayrollCalculator:
    """Computes gross pay, tax amount, and net pay."""

    @staticmethod
    def calculate_salary(
        hours: float,
        rate: float,
        deductions: float = 0.0,
        tax_rate: float = 0.0,
        bonus: float = 0.0,
    ) -> tuple[float, float, float]:
        """Return ``(gross, tax_amount, net_pay)``."""
        gross = hours * rate
        tax = gross * (tax_rate / 100)
        net = gross - deductions - tax + bonus
        return gross, tax, net
