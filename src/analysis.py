"""
Financial Analysis - NPV, IRR, Break-even, Sensitivity Analysis
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import assumptions as asmp
from src import utils
from src.financial_statements import FinancialStatements


class FinancialAnalysis:
    """Perform financial analysis and metrics calculation"""

    def __init__(self, scenario: str = 'Base_Case'):
        """
        Initialize financial analysis

        Args:
            scenario: Scenario name from assumptions
        """
        self.scenario = scenario
        self.fs = FinancialStatements(scenario)

    def calculate_npv_irr(self) -> Dict[str, float]:
        """
        Calculate NPV and IRR

        Returns:
            Dictionary with NPV and IRR values
        """
        # Get cash flows
        cf = self.fs.generate_cash_flow()
        cash_flows = cf['Net_Cash_Flow'].tolist()

        # Calculate NPV
        npv = utils.calculate_npv(cash_flows, asmp.DISCOUNT_RATE)

        # Calculate IRR
        irr = utils.calculate_irr(cash_flows)

        # Calculate payback period
        payback = utils.calculate_payback_period(cash_flows)

        return {
            'NPV': npv,
            'IRR': irr if irr else 0,
            'Payback_Period': payback if payback else 999,
        }

    def calculate_break_even(self) -> Dict[str, any]:
        """
        Calculate break-even analysis

        Returns:
            Dictionary with break-even metrics
        """
        pl = self.fs.generate_profit_loss()

        # Find break-even year (when cumulative net income turns positive)
        pl['Cumulative_Net_Income'] = pl['Net_Income'].cumsum()

        break_even_year = None
        for idx, row in pl.iterrows():
            if row['Cumulative_Net_Income'] > 0:
                break_even_year = row['Year']
                break

        # Find operational break-even (when EBITDA turns positive)
        operational_break_even_year = None
        for idx, row in pl.iterrows():
            if row['EBITDA'] > 0:
                operational_break_even_year = row['Year']
                break

        # Calculate break-even enrollment (at full capacity pricing)
        # Simplified: Fixed costs / (Revenue per student - Variable cost per student)
        year_1_opex = self.fs.opex_by_year[self.fs.years[0]]
        fixed_costs = year_1_opex['Total'] * 0.70  # Assume 70% are fixed costs

        year_1_revenue = self.fs.revenue_by_year[self.fs.years[0]]
        year_1_enrollment = utils.get_enrollment_by_year(self.fs.years[0], self.scenario)

        revenue_per_student = year_1_revenue['Total'] / year_1_enrollment
        variable_cost_per_student = (year_1_opex['Total'] * 0.30) / year_1_enrollment  # 30% variable

        contribution_margin = revenue_per_student - variable_cost_per_student

        break_even_enrollment = int(fixed_costs / contribution_margin) if contribution_margin > 0 else 0

        return {
            'Break_Even_Year': break_even_year,
            'Operational_Break_Even_Year': operational_break_even_year,
            'Break_Even_Enrollment': break_even_enrollment,
            'Full_Capacity': asmp.TOTAL_CAPACITY,
            'Break_Even_Percentage': (break_even_enrollment / asmp.TOTAL_CAPACITY * 100) if asmp.TOTAL_CAPACITY > 0 else 0,
        }

    def perform_sensitivity_analysis(self) -> Dict[str, pd.DataFrame]:
        """
        Perform sensitivity analysis on key variables

        Returns:
            Dictionary with sensitivity analysis results
        """
        sensitivity_results = {}

        # Base case NPV
        base_npv = self.calculate_npv_irr()['NPV']
        base_irr = self.calculate_npv_irr()['IRR']

        # Enrollment sensitivity
        enrollment_data = []
        for change in asmp.SENSITIVITY_VARIABLES['enrollment']:
            # Modify scenario
            temp_scenario = f"Enrollment_{change}"
            # This is simplified - in practice, we'd create new scenarios
            # For now, we'll approximate

            factor = 1 + (change / 100)
            npv_change = base_npv * factor  # Simplified linear approximation

            enrollment_data.append({
                'Change_%': change,
                'NPV': npv_change,
                'NPV_Change_%': ((npv_change - base_npv) / base_npv * 100) if base_npv != 0 else 0,
            })

        sensitivity_results['Enrollment'] = pd.DataFrame(enrollment_data)

        # Tuition sensitivity
        tuition_data = []
        for change in asmp.SENSITIVITY_VARIABLES['tuition']:
            factor = 1 + (change / 100)
            # Revenue increase directly impacts NPV
            npv_change = base_npv + (base_npv * factor * 0.5)  # Approximate

            tuition_data.append({
                'Change_%': change,
                'NPV': npv_change,
                'NPV_Change_%': ((npv_change - base_npv) / base_npv * 100) if base_npv != 0 else 0,
            })

        sensitivity_results['Tuition'] = pd.DataFrame(tuition_data)

        # OPEX sensitivity
        opex_data = []
        for change in asmp.SENSITIVITY_VARIABLES['opex']:
            factor = 1 + (change / 100)
            # Cost increase reduces NPV
            npv_change = base_npv - (base_npv * factor * 0.3)  # Approximate

            opex_data.append({
                'Change_%': change,
                'NPV': npv_change,
                'NPV_Change_%': ((npv_change - base_npv) / base_npv * 100) if base_npv != 0 else 0,
            })

        sensitivity_results['OPEX'] = pd.DataFrame(opex_data)

        # CAPEX sensitivity
        capex_data = []
        for change in asmp.SENSITIVITY_VARIABLES['capex']:
            factor = 1 + (change / 100)
            # CAPEX increase reduces NPV (one-time impact)
            capex_impact = self.fs.total_capex * (change / 100)
            npv_change = base_npv - capex_impact

            capex_data.append({
                'Change_%': change,
                'NPV': npv_change,
                'NPV_Change_%': ((npv_change - base_npv) / base_npv * 100) if base_npv != 0 else 0,
            })

        sensitivity_results['CAPEX'] = pd.DataFrame(capex_data)

        return sensitivity_results

    def compare_scenarios(self) -> pd.DataFrame:
        """
        Compare different scenarios

        Returns:
            DataFrame comparing key metrics across scenarios
        """
        scenarios_data = []

        for scenario_name in asmp.SCENARIOS.keys():
            # Create financial statements for this scenario
            fs = FinancialStatements(scenario=scenario_name)
            analysis = FinancialAnalysis(scenario=scenario_name)

            # Get metrics
            metrics = analysis.calculate_npv_irr()
            break_even = analysis.calculate_break_even()

            pl = fs.generate_profit_loss()
            cf = fs.generate_cash_flow()

            scenarios_data.append({
                'Scenario': scenario_name,
                'Description': asmp.SCENARIOS[scenario_name]['description'],
                'Total_Revenue_10Y': pl['Total_Revenue'].sum(),
                'Total_Net_Income_10Y': pl['Net_Income'].sum(),
                'Avg_Operating_Margin_%': pl['Operating_Margin_%'].mean(),
                'NPV': metrics['NPV'],
                'IRR_%': metrics['IRR'] * 100 if metrics['IRR'] else 0,
                'Payback_Period_Years': metrics['Payback_Period'],
                'Break_Even_Year': break_even['Break_Even_Year'],
                'Final_Cash_Balance': cf['Cash_Balance'].iloc[-1],
            })

        return pd.DataFrame(scenarios_data)

    def get_key_metrics_summary(self) -> Dict[str, any]:
        """
        Get summary of key metrics

        Returns:
            Dictionary with key metrics
        """
        pl = self.fs.generate_profit_loss()
        cf = self.fs.generate_cash_flow()
        npv_irr = self.calculate_npv_irr()
        break_even = self.calculate_break_even()

        return {
            'Investment_Required': self.fs.total_capex,
            'Equity_Required': self.fs.total_capex * asmp.EQUITY_CONTRIBUTION,
            'Debt_Financing': self.fs.total_capex * asmp.DEBT_CONTRIBUTION,

            'Year_1_Revenue': pl['Total_Revenue'].iloc[0],
            'Year_10_Revenue': pl['Total_Revenue'].iloc[-1],
            'Total_Revenue_10Y': pl['Total_Revenue'].sum(),
            'Revenue_CAGR_%': ((pl['Total_Revenue'].iloc[-1] / pl['Total_Revenue'].iloc[0]) ** (1/9) - 1) * 100,

            'Year_1_Net_Income': pl['Net_Income'].iloc[0],
            'Year_10_Net_Income': pl['Net_Income'].iloc[-1],
            'Total_Net_Income_10Y': pl['Net_Income'].sum(),

            'Avg_Operating_Margin_%': pl['Operating_Margin_%'].mean(),
            'Avg_Net_Margin_%': pl['Net_Margin_%'].mean(),

            'NPV': npv_irr['NPV'],
            'IRR_%': npv_irr['IRR'] * 100 if npv_irr['IRR'] else 0,
            'Payback_Period_Years': npv_irr['Payback_Period'],

            'Break_Even_Year': break_even['Break_Even_Year'],
            'Operational_Break_Even_Year': break_even['Operational_Break_Even_Year'],
            'Break_Even_Enrollment': break_even['Break_Even_Enrollment'],

            'Final_Cash_Balance': cf['Cash_Balance'].iloc[-1],
            'Min_Cash_Balance': cf['Cash_Balance'].min(),

            'Year_1_Enrollment': utils.get_enrollment_by_year(self.fs.years[0], self.scenario),
            'Year_10_Enrollment': utils.get_enrollment_by_year(self.fs.years[-1], self.scenario),
            'Full_Capacity': asmp.TOTAL_CAPACITY,
        }


if __name__ == '__main__':
    # Test analysis
    print("=" * 80)
    print("FINANCIAL ANALYSIS - BASE CASE")
    print("=" * 80)

    analysis = FinancialAnalysis(scenario='Base_Case')

    # Key metrics
    print("\nKEY METRICS SUMMARY:")
    print("=" * 80)
    metrics = analysis.get_key_metrics_summary()
    for key, value in metrics.items():
        if isinstance(value, float):
            if 'Margin' in key or 'IRR' in key or 'CAGR' in key:
                print(f"{key}: {value:.2f}%")
            else:
                print(f"{key}: {utils.format_currency(value)}")
        else:
            print(f"{key}: {value}")

    # Break-even analysis
    print("\n" + "=" * 80)
    print("BREAK-EVEN ANALYSIS:")
    print("=" * 80)
    break_even = analysis.calculate_break_even()
    for key, value in break_even.items():
        if isinstance(value, float):
            print(f"{key}: {value:.1f}")
        else:
            print(f"{key}: {value}")

    # Scenario comparison
    print("\n" + "=" * 80)
    print("SCENARIO COMPARISON:")
    print("=" * 80)
    scenarios = analysis.compare_scenarios()
    print(scenarios.to_string(index=False))

    # Sensitivity analysis
    print("\n" + "=" * 80)
    print("SENSITIVITY ANALYSIS:")
    print("=" * 80)
    sensitivity = analysis.perform_sensitivity_analysis()
    for variable, df in sensitivity.items():
        print(f"\n{variable} Sensitivity:")
        print(df.to_string(index=False))
