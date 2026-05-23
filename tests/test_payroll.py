from src.engine.payroll import PayrollCalculator


def test_basic_gross():
    gross, _, _ = PayrollCalculator.calculate_salary(40, 25.0)
    assert gross == 1000.0


def test_zero_tax_when_not_set():
    _, tax, _ = PayrollCalculator.calculate_salary(40, 25.0)
    assert tax == 0.0


def test_net_equals_gross_with_no_deductions():
    gross, _, net = PayrollCalculator.calculate_salary(40, 25.0)
    assert net == gross


def test_tax_calculation():
    gross, tax, _ = PayrollCalculator.calculate_salary(40, 25.0, tax_rate=10.0)
    assert gross == 1000.0
    assert tax == 100.0


def test_deductions_reduce_net():
    _, _, net = PayrollCalculator.calculate_salary(40, 25.0, deductions=200.0)
    assert net == 800.0


def test_bonus_increases_net():
    _, _, net = PayrollCalculator.calculate_salary(40, 25.0, bonus=100.0)
    assert net == 1100.0


def test_full_calculation():
    gross, tax, net = PayrollCalculator.calculate_salary(
        hours=40,
        rate=25.0,
        deductions=50.0,
        tax_rate=10.0,
        bonus=200.0,
    )
    assert gross == 1000.0
    assert tax == 100.0
    assert net == 1050.0


def test_zero_hours():
    gross, tax, net = PayrollCalculator.calculate_salary(0, 25.0)
    assert gross == 0.0
    assert tax == 0.0
    assert net == 0.0


def test_fractional_hours():
    gross, _, _ = PayrollCalculator.calculate_salary(7.5, 20.0)
    assert gross == 150.0
