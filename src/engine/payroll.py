class PayrollCalculator:
    @staticmethod
    def calculate_salary(hours, rate, deductions, tax_rate, bonus):
        gross = hours * rate
        tax = gross * (tax_rate / 100)
        net = gross - deductions - tax + bonus
        return gross, tax, net
