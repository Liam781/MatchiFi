import sys
from decimal import Decimal, InvalidOperation, getcontext
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTextEdit
)

# Set Decimal precision high enough for financial calcs
getcontext().prec = 28

# Your FinancialRatios class from the previous code snippet
class FinancialRatios:
    @staticmethod
    def calculate_debt_to_equity_ratio(total_liabilities: Decimal, shareholders_equity: Decimal) -> Decimal:
        if shareholders_equity == 0:
            raise ValueError("Shareholders' Equity cannot be zero for Debt-to-Equity Ratio.")
        return total_liabilities / shareholders_equity

    @staticmethod
    def calculate_return_on_assets(net_income: Decimal, average_total_assets: Decimal) -> Decimal:
        if average_total_assets == 0:
            raise ValueError("Average Total Assets cannot be zero for Return on Assets.")
        return net_income / average_total_assets

    @staticmethod
    def calculate_return_on_equity(net_income: Decimal, average_shareholders_equity: Decimal) -> Decimal:
        if average_shareholders_equity == 0:
            raise ValueError("Average Shareholders' Equity cannot be zero for Return on Equity.")
        return net_income / average_shareholders_equity

    @staticmethod
    def calculate_interest_coverage_ratio(ebit: Decimal, interest_expense: Decimal) -> Decimal:
        if interest_expense == 0:
            raise ValueError("Interest Expense cannot be zero for Interest Coverage Ratio.")
        return ebit / interest_expense

    @staticmethod
    def calculate_profit_margin(net_profit: Decimal, revenue: Decimal) -> Decimal:
        if revenue == 0:
            raise ValueError("Revenue cannot be zero for Profit Margin.")
        return (net_profit / revenue) * Decimal('100')

    @staticmethod
    def get_company_performance(profit_margin: Decimal, industry_benchmark: Decimal) -> str:
        if profit_margin.is_nan() or profit_margin.is_infinite():
            return "Cannot assess performance due to undefined or infinite profit margin."
        elif profit_margin < industry_benchmark:
            return "Poor"
        else:
            return "Exceptional"


class MatchiFiApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MatchiFi - Funding Recommendation")
        self.setGeometry(100, 100, 500, 500)

        self.layout = QVBoxLayout()

        # Input fields with labels
        self.layout.addWidget(QLabel("Enter Total Revenue (P):"))
        self.revenue_input = QLineEdit()
        self.layout.addWidget(self.revenue_input)

        self.layout.addWidget(QLabel("Enter EBIT (P):"))
        self.ebit_input = QLineEdit()
        self.layout.addWidget(self.ebit_input)

        self.layout.addWidget(QLabel("Enter Interest Payment (P):"))
        self.interest_input = QLineEdit()
        self.layout.addWidget(self.interest_input)

        self.layout.addWidget(QLabel("Enter Total Liabilities (P):"))
        self.liabilities_input = QLineEdit()
        self.layout.addWidget(self.liabilities_input)

        self.layout.addWidget(QLabel("Enter Shareholders Equity (P):"))
        self.equity_input = QLineEdit()
        self.layout.addWidget(self.equity_input)

        self.layout.addWidget(QLabel("Enter Average Total Assets (P):"))
        self.assets_input = QLineEdit()
        self.layout.addWidget(self.assets_input)

        self.layout.addWidget(QLabel("Enter Industry Profit Margin Benchmark (%):"))
        self.benchmark_input = QLineEdit()
        self.layout.addWidget(self.benchmark_input)

        # Button
        self.predict_button = QPushButton("Get Funding Recommendation & Analysis")
        self.predict_button.clicked.connect(self.make_prediction)
        self.layout.addWidget(self.predict_button)

        # Result display (multiline & scrollable)
        self.result_display = QTextEdit()
        self.result_display.setReadOnly(True)
        self.layout.addWidget(self.result_display)

        self.setLayout(self.layout)

    def make_prediction(self):
        try:
            # Parse inputs safely as Decimals
            revenue = Decimal(self.revenue_input.text())
            ebit = Decimal(self.ebit_input.text())
            interest = Decimal(self.interest_input.text())
            liabilities = Decimal(self.liabilities_input.text())
            equity = Decimal(self.equity_input.text())
            assets = Decimal(self.assets_input.text())
            benchmark = Decimal(self.benchmark_input.text())

            # Constants & intermediate calculations
            TAX_RATE = Decimal('0.25')
            ebt = ebit - interest
            net_profit = ebt * (Decimal('1') - TAX_RATE)

            results = {}

            # Calculate financial ratios with error handling
            try:
                dte = FinancialRatios.calculate_debt_to_equity_ratio(liabilities, equity)
                results["Debt-to-Equity Ratio"] = f"{dte:.4f}"
            except Exception as e:
                results["Debt-to-Equity Ratio"] = f"Error: {e}"

            try:
                roa = FinancialRatios.calculate_return_on_assets(net_profit, assets)
                results["Return on Assets (ROA)"] = f"{roa * 100:.2f}%"
            except Exception as e:
                results["Return on Assets (ROA)"] = f"Error: {e}"

            try:
                roe = FinancialRatios.calculate_return_on_equity(net_profit, equity)
                results["Return on Equity (ROE)"] = f"{roe * 100:.2f}%"
            except Exception as e:
                results["Return on Equity (ROE)"] = f"Error: {e}"

            try:
                icr = FinancialRatios.calculate_interest_coverage_ratio(ebit, interest)
                results["Interest Coverage Ratio (ICR)"] = f"{icr:.2f}"
            except Exception as e:
                results["Interest Coverage Ratio (ICR)"] = f"Error: {e}"

            try:
                profit_margin = FinancialRatios.calculate_profit_margin(net_profit, revenue)
                results["Profit Margin"] = f"{profit_margin:.2f}%"
            except Exception as e:
                results["Profit Margin"] = f"Error: {e}"

            # Company performance based on profit margin & benchmark
            try:
                if "Profit Margin" in results and not results["Profit Margin"].startswith("Error"):
                    performance = FinancialRatios.get_company_performance(profit_margin, benchmark)
                else:
                    performance = "Cannot assess performance due to error in Profit Margin"
            except Exception as e:
                performance = f"Error assessing performance: {e}"

            # Determine recommendation based on company performance or profit margin
            recommendation = "Eligible" if performance == "Exceptional" else "Not Eligible"

            # Compose output text
            output_text = (
                f"--- Profit Analysis Results ---\n"
                f"Revenue: P{revenue:,.2f}\n"
                f"EBIT: P{ebit:,.2f}\n"
                f"EBT (Earnings Before Tax): P{ebt:,.2f}\n"
                f"Net Profit (after tax): P{net_profit:,.2f}\n\n"
            )
            for key, val in results.items():
                output_text += f"{key}: {val}\n"
            output_text += f"\nCompany Performance: {performance}\n"
            output_text += f"Funding Recommendation: {recommendation}"

            self.result_display.setPlainText(output_text)

        except (InvalidOperation, ValueError):
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values for all fields.")
        except Exception as e:
            QMessageBox.critical(self, "Unexpected Error", f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatchiFiApp()
    window.show()
    sys.exit(app.exec_())
