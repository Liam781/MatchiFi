import sys
from decimal import Decimal, getcontext, InvalidOperation

# Set the global precision for Decimal operations.
# 28 digits is a common recommendation for financial applications.
getcontext().prec = 28

class FinancialRatios:
    """
    A class containing static methods for calculating various financial ratios.
    All calculations use decimal.Decimal for arbitrary-precision arithmetic.
    Methods raise ValueError for invalid or undefined calculations (e.g., division by zero).
    """

    @staticmethod
    def calculate_debt_to_equity_ratio(total_liabilities: Decimal, shareholders_equity: Decimal) -> Decimal:
        """
        Calculates the Debt-to-Equity Ratio.
        Measures a company's financial leverage.
        Raises ValueError if shareholders_equity is zero.
        """
        if shareholders_equity.compare(Decimal('0')) == 0:
            raise ValueError("Shareholders' Equity cannot be zero for Debt-to-Equity Ratio.")
        return total_liabilities / shareholders_equity

    @staticmethod
    def calculate_return_on_assets(net_income: Decimal, average_total_assets: Decimal) -> Decimal:
        """
        Calculates the Return on Assets (ROA).
        Indicates how efficiently assets generate profit.
        Raises ValueError if average_total_assets is zero.
        """
        if average_total_assets.compare(Decimal('0')) == 0:
            raise ValueError("Average Total Assets cannot be zero for Return on Assets.")
        return net_income / average_total_assets

    @staticmethod
    def calculate_return_on_equity(net_income: Decimal, average_shareholders_equity: Decimal) -> Decimal:
        """
        Calculates the Return on Equity (ROE).
        Measures profit generated per dollar of shareholders' equity.
        Raises ValueError if average_shareholders_equity is zero.
        """
        if average_shareholders_equity.compare(Decimal('0')) == 0:
            raise ValueError("Average Shareholders' Equity cannot be zero for Return on Equity.")
        return net_income / average_shareholders_equity

    @staticmethod
    def calculate_interest_coverage_ratio(ebit: Decimal, interest_expense: Decimal) -> Decimal:
        """
        Calculates the Interest Coverage Ratio (ICR).
        Assesses a company's ability to pay interest expenses from operating profit.
        Raises ValueError if interest_expense is zero.
        """
        if interest_expense.compare(Decimal('0')) == 0:
            # If EBIT is also zero, it's 0/0, which is NaN.
            # If EBIT is positive, it's effectively infinite.
            # Raising ValueError for clarity that it's an undefined/problematic scenario.
            raise ValueError("Interest Expense cannot be zero for Interest Coverage Ratio.")
        return ebit / interest_expense

    @staticmethod
    def calculate_profit_margin(net_profit: Decimal, revenue: Decimal) -> Decimal:
        """
        Calculates the Profit Margin as a percentage.
        Measures the percentage of revenue that ends up as net profit.
        Raises ValueError if revenue is zero.
        """
        if revenue.compare(Decimal('0')) == 0:
            raise ValueError("Revenue cannot be zero for Profit Margin.")
        # Multiply by 100 here to return a percentage value (e.g., 15.25 for 15.25%)
        return (net_profit / revenue) * Decimal('100')

    @staticmethod
    def get_company_performance(profit_margin: Decimal, industry_benchmark: Decimal) -> str:
        """
        Compares the company's profit margin to an industry benchmark.
        Assumes both are in percentage format (e.g., 15.0 for 15%).
        """
        # Check if profit_margin is a valid number before comparison
        if profit_margin.is_nan() or profit_margin.is_infinite():
            return "Cannot assess performance due to undefined or infinite profit margin."
        elif profit_margin < industry_benchmark:
            return "Poor"
        else:
            return "Exceptional"
