"""
Financial Statements - P&L, Cash Flow, and Balance Sheet
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import assumptions as asmp
from src import utils
from src.revenue_model import RevenueModel
from src.opex_model import OPEXModel
from src.capex_model import CAPEXModel


class FinancialStatements:
    """Generate all financial statements"""

    def __init__(self, scenario: str = 'Base_Case'):
        """
        Initialize financial statements

        Args:
            scenario: Scenario name from assumptions
        """
        self.scenario = scenario
        self.years = utils.get_year_range()

        # Initialize models
        self.revenue_model = RevenueModel(scenario)
        self.opex_model = OPEXModel(scenario)
        self.capex_model = CAPEXModel(scenario)

        # Get data
        self.revenue_by_year = self.revenue_model.calculate_total_revenue()
        self.opex_by_year = self.opex_model.calculate_total_opex()
        self.total_capex = self.capex_model.calculate_total_capex()['Total']

    def generate_profit_loss(self) -> pd.DataFrame:
        """
        Generate Profit & Loss Statement

        Returns:
            DataFrame with P&L for all years
        """
        pl_data = []

        for year in self.years:
            revenue = self.revenue_by_year[year]
            opex = self.opex_by_year[year]

            # Revenue
            total_revenue = revenue['Total']

            # Operating Expenses
            total_opex = opex['Total']

            # EBITDA
            ebitda = total_revenue - total_opex

            # Depreciation (straight-line over 20 years)
            depreciation = self.total_capex / 20

            # EBIT
            ebit = ebitda - depreciation

            # Interest (if using debt financing)
            # Assume 60% debt financing
            debt_amount = self.total_capex * asmp.DEBT_CONTRIBUTION
            interest_expense = debt_amount * asmp.LOAN_INTEREST_RATE

            # Reduce debt over loan term
            year_index = self.years.index(year)
            if year_index < asmp.LOAN_TERM_YEARS:
                principal_payment = debt_amount / asmp.LOAN_TERM_YEARS
                remaining_debt = debt_amount - (principal_payment * year_index)
                interest_expense = remaining_debt * asmp.LOAN_INTEREST_RATE
            else:
                interest_expense = 0

            # EBT (Earnings Before Tax)
            ebt = ebit - interest_expense

            # Tax (Ethiopia corporate tax rate ~30%)
            tax_rate = 0.30
            if ebt > 0:
                tax_expense = ebt * tax_rate
            else:
                tax_expense = 0

            # Net Income
            net_income = ebt - tax_expense

            # Operating metrics
            operating_margin = (ebit / total_revenue * 100) if total_revenue > 0 else 0
            net_margin = (net_income / total_revenue * 100) if total_revenue > 0 else 0

            pl_data.append({
                'Year': year,
                'Total_Revenue': total_revenue,
                'Operating_Expenses': total_opex,
                'EBITDA': ebitda,
                'Depreciation': depreciation,
                'EBIT': ebit,
                'Interest_Expense': interest_expense,
                'EBT': ebt,
                'Tax_Expense': tax_expense,
                'Net_Income': net_income,
                'Operating_Margin_%': operating_margin,
                'Net_Margin_%': net_margin,
            })

        return pd.DataFrame(pl_data)

    def generate_cash_flow(self) -> pd.DataFrame:
        """
        Generate Cash Flow Statement

        Returns:
            DataFrame with cash flow for all years
        """
        pl = self.generate_profit_loss()
        cf_data = []

        cash_balance = 0
        debt_amount = self.total_capex * asmp.DEBT_CONTRIBUTION
        equity_amount = self.total_capex * asmp.EQUITY_CONTRIBUTION

        for i, year in enumerate(self.years):
            pl_row = pl[pl['Year'] == year].iloc[0]

            # Operating activities
            net_income = pl_row['Net_Income']
            depreciation = pl_row['Depreciation']  # Non-cash expense, add back
            changes_in_working_capital = 0  # Simplified

            cash_from_operations = net_income + depreciation + changes_in_working_capital

            # Investing activities
            if i == 0:
                # Year 1: CAPEX investment
                capex_cash_out = -self.total_capex
            else:
                # Subsequent years: minor CAPEX for replacements/expansion
                capex_cash_out = -self.total_capex * 0.02  # 2% annual maintenance CAPEX

            cash_from_investing = capex_cash_out

            # Financing activities
            if i == 0:
                # Year 1: Raise equity and debt
                equity_raised = equity_amount
                debt_raised = debt_amount
                debt_repayment = 0
            else:
                equity_raised = 0
                debt_raised = 0
                # Debt repayment
                if i < asmp.LOAN_TERM_YEARS:
                    debt_repayment = -debt_amount / asmp.LOAN_TERM_YEARS
                else:
                    debt_repayment = 0

            cash_from_financing = equity_raised + debt_raised + debt_repayment

            # Net cash flow
            net_cash_flow = cash_from_operations + cash_from_investing + cash_from_financing

            # Cash balance
            cash_balance += net_cash_flow

            cf_data.append({
                'Year': year,
                'Cash_from_Operations': cash_from_operations,
                'Cash_from_Investing': cash_from_investing,
                'Cash_from_Financing': cash_from_financing,
                'Net_Cash_Flow': net_cash_flow,
                'Cash_Balance': cash_balance,
            })

        return pd.DataFrame(cf_data)

    def generate_balance_sheet(self) -> pd.DataFrame:
        """
        Generate Balance Sheet (simplified)

        Returns:
            DataFrame with balance sheet for all years
        """
        pl = self.generate_profit_loss()
        cf = self.generate_cash_flow()

        bs_data = []
        retained_earnings = 0
        debt_balance = self.total_capex * asmp.DEBT_CONTRIBUTION

        for i, year in enumerate(self.years):
            pl_row = pl[pl['Year'] == year].iloc[0]
            cf_row = cf[cf['Year'] == year].iloc[0]

            # Assets
            cash = cf_row['Cash_Balance']

            # Fixed assets (net of depreciation)
            if i == 0:
                gross_fixed_assets = self.total_capex
            else:
                # Add minor CAPEX each year
                gross_fixed_assets += self.total_capex * 0.02

            accumulated_depreciation = pl_row['Depreciation'] * (i + 1)
            net_fixed_assets = gross_fixed_assets - accumulated_depreciation

            # Working capital (simplified)
            accounts_receivable = pl_row['Total_Revenue'] * (asmp.ACCOUNTS_RECEIVABLE_DAYS / 365)
            inventory = 500000  # Simplified constant inventory
            working_capital = accounts_receivable + inventory

            total_assets = cash + net_fixed_assets + working_capital

            # Liabilities
            accounts_payable = pl_row['Operating_Expenses'] * (asmp.ACCOUNTS_PAYABLE_DAYS / 365)

            # Debt balance
            if i < asmp.LOAN_TERM_YEARS:
                debt_balance -= self.total_capex * asmp.DEBT_CONTRIBUTION / asmp.LOAN_TERM_YEARS
            else:
                debt_balance = 0

            total_liabilities = accounts_payable + debt_balance

            # Equity
            equity = self.total_capex * asmp.EQUITY_CONTRIBUTION
            retained_earnings += pl_row['Net_Income']

            total_equity = equity + retained_earnings

            # Total liabilities + equity
            total_liab_equity = total_liabilities + total_equity

            bs_data.append({
                'Year': year,
                'Cash': cash,
                'Accounts_Receivable': accounts_receivable,
                'Inventory': inventory,
                'Net_Fixed_Assets': net_fixed_assets,
                'Total_Assets': total_assets,
                'Accounts_Payable': accounts_payable,
                'Debt': debt_balance,
                'Total_Liabilities': total_liabilities,
                'Equity': equity,
                'Retained_Earnings': retained_earnings,
                'Total_Equity': total_equity,
                'Total_Liab_Equity': total_liab_equity,
            })

        return pd.DataFrame(bs_data)

    def get_all_statements(self) -> Dict[str, pd.DataFrame]:
        """
        Get all financial statements

        Returns:
            Dictionary with statement name as key and DataFrame as value
        """
        return {
            'Profit_Loss': self.generate_profit_loss(),
            'Cash_Flow': self.generate_cash_flow(),
            'Balance_Sheet': self.generate_balance_sheet(),
            'Revenue_Detail': self.revenue_model.get_revenue_dataframe(),
            'OPEX_Detail': self.opex_model.get_opex_dataframe(),
            'CAPEX_Detail': self.capex_model.get_capex_breakdown(),
        }


if __name__ == '__main__':
    # Test financial statements
    print("=" * 80)
    print("FINANCIAL STATEMENTS TEST - BASE CASE")
    print("=" * 80)

    fs = FinancialStatements(scenario='Base_Case')

    # P&L
    print("\n" + "=" * 80)
    print("PROFIT & LOSS STATEMENT")
    print("=" * 80)
    pl = fs.generate_profit_loss()
    print(pl.to_string(index=False))

    # Cash Flow
    print("\n" + "=" * 80)
    print("CASH FLOW STATEMENT")
    print("=" * 80)
    cf = fs.generate_cash_flow()
    print(cf.to_string(index=False))

    # Summary metrics
    print("\n" + "=" * 80)
    print("KEY METRICS")
    print("=" * 80)
    print(f"Total Revenue (10 years): {utils.format_currency(pl['Total_Revenue'].sum())}")
    print(f"Total Net Income (10 years): {utils.format_currency(pl['Net_Income'].sum())}")
    print(f"Average Operating Margin: {pl['Operating_Margin_%'].mean():.1f}%")
    print(f"Average Net Margin: {pl['Net_Margin_%'].mean():.1f}%")
    print(f"Final Cash Balance: {utils.format_currency(cf['Cash_Balance'].iloc[-1])}")
