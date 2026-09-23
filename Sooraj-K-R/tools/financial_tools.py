def calculate_emi(principal: float, annual_rate: float, tenure_years: int) -> float:
    """Calculate Equated Monthly Installment for a loan."""
    if principal <= 0 or tenure_years <= 0:
        raise ValueError("Principal and tenure must be positive.")

    if annual_rate == 0:
        return principal / (tenure_years * 12)

    monthly_rate = annual_rate / (12 * 100)
    months = tenure_years * 12
    emi = principal * monthly_rate * (1 + monthly_rate) ** months / ((1 + monthly_rate) ** months - 1)
    return round(emi, 2)


def calculate_simple_interest(principal: float, rate: float, time: float) -> float:
    """Calculate simple interest."""
    if principal < 0 or rate < 0 or time < 0:
        raise ValueError("Principal, rate, and time must be non-negative.")

    interest = principal * rate * time / 100
    return round(interest, 2)


def calculate_compound_interest(
    principal: float, rate: float, time: float, compounds_per_year: int = 1
) -> float:
    """Calculate compound interest."""
    if principal < 0 or rate < 0 or time < 0:
        raise ValueError("Principal, rate, and time must be non-negative.")
    if compounds_per_year <= 0:
        raise ValueError("Compounding frequency must be positive.")

    if rate == 0:
        return 0.0

    amount = principal * (1 + rate / (100 * compounds_per_year)) ** (compounds_per_year * time)
    interest = amount - principal
    return round(interest, 2)


def calculate_sip_returns(monthly_investment: float, annual_rate: float, years: int) -> float:
    """Calculate the future value of a monthly SIP."""
    if monthly_investment <= 0 or years <= 0:
        raise ValueError("Monthly investment and years must be positive.")

    if annual_rate == 0:
        return round(monthly_investment * years * 12, 2)

    monthly_rate = annual_rate / (12 * 100)
    months = years * 12
    future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    return round(future_value, 2)


def calculate_returns(principal: float, annual_rate: float, years: int) -> float:
    """Calculate returns on a lump-sum investment using compound interest."""
    if principal <= 0 or years <= 0:
        raise ValueError("Principal and years must be positive.")

    if annual_rate == 0:
        return round(principal, 2)

    future_value = principal * (1 + annual_rate / 100) ** years
    return round(future_value, 2)
