import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
# Import our custom financial calculation module
from financial_ratios_calculator import FinancialRatios

def get_decimal_input(prompt: str) -> Decimal:
    """
    Safely gets a non-negative Decimal input from the user.
    Handles non-numeric input and negative values gracefully.
    """
    while True:
        try:
            value_str = input(prompt).strip() # .strip() removes leading/trailing whitespace
            if not value_str: # Check for empty input
                raise ValueError("Input cannot be empty.")
            
            value = Decimal(value_str)
            if value.compare(Decimal('0')) < 0:
                print("Input cannot be negative. Please enter a non-negative number.")
            else:
                return value
        except InvalidOperation:
            print("Invalid input. Please enter a valid numerical value (e.g., 123.45).")
        except ValueError as e:
            print(f"Input Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during input: {e}")

def main():
    """
    Main function to run the Profit Analysis application.
    Gathers input, performs calculations, and displays results.
    """
    print("--- Profit Analysis Application ---")
    
    # Define a fixed tax rate for net profit calculation
    TAX_RATE = Decimal('0.25') # 25%

    # --- Input Gathering ---
    try:
        prof_bm = get_decimal_input("Input Total Industry Benchmark (e.g., 15 for 15%): ")
        revenue = get_decimal_input("Input Total Revenue: P")
        annual_interest = get_decimal_input("Input Interest annual payment: P")
        ebit = get_decimal_input("Input EBIT (Earnings Before Interest and Taxes): P")
        total_liabilities = get_decimal_input("Input Total Liabilities: P")
        shareholders_equity = get_decimal_input("Input Total Shareholder Equity: P")
        average_total_assets = get_decimal_input("Input Total Average Total Assets: P")

    except Exception as e:
        print(f"\nExiting: Error during input gathering - {e}", file=sys.stderr)
        return

    # --- Intermediate Calculations ---
    # These are specific to the app's workflow, not generic ratios
    ebt = ebit - annual_interest
    net_profit = ebt * (Decimal('1') - TAX_RATE)
    tax_val = TAX_RATE * ebt

    # --- Ratio Calculations and Error Handling ---
    # Call functions from our financial_ratios_calculator module
    
    dte_ratio = Decimal('NaN') # Initialize with NaN to indicate not calculated
    return_on_assets = Decimal('NaN')
    return_on_equity = Decimal('NaN')
    icr = Decimal('NaN')
    profit_margin = Decimal('NaN')
    company_performance = "Not Assessed" # Default performance status

    print("\n--- Performing Calculations ---")
    try:
        dte_ratio = FinancialRatios.calculate_debt_to_equity_ratio(total_liabilities, shareholders_equity)
    except ValueError as e:
        print(f"Error calculating Debt-to-Equity Ratio: {e}", file=sys.stderr)

    try:
        return_on_assets = FinancialRatios.calculate_return_on_assets(net_profit, average_total_assets)
    except ValueError as e:
        print(f"Error calculating Return on Assets: {e}", file=sys.stderr)
        
    try:
        return_on_equity = FinancialRatios.calculate_return_on_equity(net_profit, shareholders_equity)
    except ValueError as e:
        print(f"Error calculating Return on Equity: {e}", file=sys.stderr)

    try:
        icr = FinancialRatios.calculate_interest_coverage_ratio(ebit, annual_interest)
    except ValueError as e:
        print(f"Error calculating Interest Coverage Ratio: {e}", file=sys.stderr)

    try:
        profit_margin = FinancialRatios.calculate_profit_margin(net_profit, revenue)
    except ValueError as e:
        print(f"Error calculating Profit Margin: {e}", file=sys.stderr)
    
    # Assess company performance only if profit_margin was successfully calculated
    if not profit_margin.is_nan():
        company_performance = FinancialRatios.get_company_performance(profit_margin, prof_bm)
    else:
        company_performance = "Cannot Assess (Profit Margin Undefined)"

    # --- Display Results ---
    print("\n--- Profit Analysis Results ---")

    # Use f-strings with format specifiers for clean output.
    # :.2f for 2 decimal places, :,.2f for thousands separator and 2 decimal places
    
    print(f"Revenue         = P{revenue:,.2f}")
    print(f"EBIT            = P{ebit:,.2f}")
    print(f"EBT             = P{ebt:,.2f}")
    print(f"Tax Value       = P{tax_val:,.2f}")
    print(f"Net Profit      = P{net_profit:,.2f}")
    print(f"------------------------------------")
    
    # Display ratios, handling cases where they might be NaN
    print(f"Debt-to-Equity  = {dte_ratio:,.2f}" if not dte_ratio.is_nan() else "Debt-to-Equity  = N/A")
    print(f"Return on Assets= {return_on_assets * 100:,.2f}%" if not return_on_assets.is_nan() else "Return on Assets= N/A")
    print(f"Return on Equity= {return_on_equity * 100:,.2f}%" if not return_on_equity.is_nan() else "Return on Equity= N/A")
    print(f"Interest Cover  = {icr:,.2f}" if not icr.is_nan() else "Interest Cover  = N/A")
    print(f"Profit Margin   = {profit_margin:,.2f} Percent" if not profit_margin.is_nan() else "Profit Margin   = N/A")
    
    print(f"Company Performance: {company_performance}")

    print("\n--- Analysis Complete ---")

if __name__ == "__main__":
    main()