"""
Main execution script for Ethiopian International Christian School Financial Model

This script generates a complete financial feasibility study including:
- Revenue projections
- Capital expenditure (CAPEX) breakdown
- Operating expenditure (OPEX) projections
- Financial statements (P&L, Cash Flow, Balance Sheet)
- Financial analysis (NPV, IRR, Break-even)
- Sensitivity analysis
- Scenario comparison

Output: Excel workbook with all analyses in the output/ directory
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from config import assumptions as asmp
from src import utils
from src.revenue_model import RevenueModel
from src.capex_model import CAPEXModel
from src.opex_model import OPEXModel
from src.financial_statements import FinancialStatements
from src.analysis import FinancialAnalysis
from src.excel_dashboard import ExcelDashboard


def print_header(title: str):
    """Print formatted header"""
    print("\n" + "=" * 100)
    print(f"  {title}")
    print("=" * 100)


def generate_financial_model(scenario: str = 'Base_Case'):
    """
    Generate complete financial model for a scenario

    Args:
        scenario: Scenario name from assumptions
    """
    print_header(f"GENERATING FINANCIAL MODEL - {scenario.upper()}")

    # Initialize models
    print("\nInitializing models...")
    revenue_model = RevenueModel(scenario)
    capex_model = CAPEXModel(scenario)
    opex_model = OPEXModel(scenario)
    fs = FinancialStatements(scenario)
    analysis = FinancialAnalysis(scenario)

    # Generate all components
    print("Calculating revenue projections...")
    revenue_df = revenue_model.get_revenue_dataframe()

    print("Calculating capital expenditure...")
    capex_summary = capex_model.get_capex_breakdown()
    capex_details = capex_model.get_detailed_breakdown()

    print("Calculating operating expenses...")
    opex_df = opex_model.get_opex_dataframe()

    print("Generating financial statements...")
    pl_df = fs.generate_profit_loss()
    cf_df = fs.generate_cash_flow()
    bs_df = fs.generate_balance_sheet()

    print("Performing financial analysis...")
    metrics = analysis.get_key_metrics_summary()
    break_even = analysis.calculate_break_even()

    return {
        'revenue': revenue_df,
        'capex_summary': capex_summary,
        'capex_details': capex_details,
        'opex': opex_df,
        'profit_loss': pl_df,
        'cash_flow': cf_df,
        'balance_sheet': bs_df,
        'metrics': metrics,
        'break_even': break_even,
    }


def export_full_model():
    """
    Generate and export complete financial model with all scenarios
    """
    print_header("ETHIOPIAN INTERNATIONAL CHRISTIAN SCHOOL - FINANCIAL FEASIBILITY STUDY")
    print(f"\nSchool: {asmp.SCHOOL_NAME}")
    print(f"Location: {asmp.LOCATION}")
    print(f"Curriculum: {asmp.CURRICULUM_TYPE}")
    print(f"Launch Date: {asmp.SCHOOL_LAUNCH_DATE.strftime('%B %Y')}")
    print(f"Projection Period: {asmp.PROJECTION_YEARS} years")
    print(f"\nReport Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Generate base case
    base_case = generate_financial_model('Base_Case')

    # Generate all scenarios
    print_header("GENERATING SCENARIO COMPARISONS")
    analysis = FinancialAnalysis('Base_Case')
    scenario_comparison = analysis.compare_scenarios()
    sensitivity_results = analysis.perform_sensitivity_analysis()

    # Prepare export data
    export_data = {
        'Executive_Summary': create_executive_summary(base_case),
        'Revenue_Projections': base_case['revenue'],
        'CAPEX_Summary': base_case['capex_summary'],
        'OPEX_Projections': base_case['opex'],
        'Profit_Loss': base_case['profit_loss'],
        'Cash_Flow': base_case['cash_flow'],
        'Balance_Sheet': base_case['balance_sheet'],
        'Scenario_Comparison': scenario_comparison,
    }

    # Add CAPEX details
    for name, df in base_case['capex_details'].items():
        export_data[f'CAPEX_{name}'] = df

    # Add sensitivity analysis
    for variable, df in sensitivity_results.items():
        export_data[f'Sensitivity_{variable}'] = df

    # Export to Enhanced Excel Dashboard
    print_header("CREATING INTERACTIVE EXCEL DASHBOARD")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'School_Financial_Dashboard_{timestamp}.xlsx'

    # Use enhanced dashboard
    dashboard = ExcelDashboard(scenario='Base_Case')
    filepath = dashboard.export(filename)

    # Print summary to console
    print_summary(base_case, scenario_comparison)

    return filepath


def create_executive_summary(base_case: dict) -> 'pd.DataFrame':
    """Create executive summary table"""
    import pandas as pd

    metrics = base_case['metrics']

    summary_data = {
        'Metric': [
            'INVESTMENT REQUIREMENTS',
            'Total CAPEX Required',
            'Equity Investment (40%)',
            'Debt Financing (60%)',
            '',
            'REVENUE PROJECTIONS',
            'Year 1 Revenue',
            'Year 10 Revenue',
            'Total 10-Year Revenue',
            'Revenue CAGR',
            '',
            'PROFITABILITY',
            'Year 1 Net Income',
            'Year 10 Net Income',
            'Total 10-Year Net Income',
            'Average Operating Margin',
            'Average Net Margin',
            '',
            'FINANCIAL METRICS',
            'Net Present Value (NPV)',
            'Internal Rate of Return (IRR)',
            'Payback Period',
            'Break-Even Year (Cumulative)',
            'Operational Break-Even Year',
            '',
            'ENROLLMENT',
            'Year 1 Enrollment',
            'Year 10 Enrollment',
            'Full Capacity',
            'Break-Even Enrollment',
            '',
            'CASH POSITION',
            'Final Cash Balance (Year 10)',
            'Minimum Cash Balance',
        ],
        'Value': [
            '',
            utils.format_currency(metrics['Investment_Required']),
            utils.format_currency(metrics['Equity_Required']),
            utils.format_currency(metrics['Debt_Financing']),
            '',
            '',
            utils.format_currency(metrics['Year_1_Revenue']),
            utils.format_currency(metrics['Year_10_Revenue']),
            utils.format_currency(metrics['Total_Revenue_10Y']),
            f"{metrics['Revenue_CAGR_%']:.1f}%",
            '',
            '',
            utils.format_currency(metrics['Year_1_Net_Income']),
            utils.format_currency(metrics['Year_10_Net_Income']),
            utils.format_currency(metrics['Total_Net_Income_10Y']),
            f"{metrics['Avg_Operating_Margin_%']:.1f}%",
            f"{metrics['Avg_Net_Margin_%']:.1f}%",
            '',
            '',
            utils.format_currency(metrics['NPV']),
            f"{metrics['IRR_%']:.1f}%",
            f"{metrics['Payback_Period_Years']:.1f} years",
            str(metrics['Break_Even_Year']) if metrics['Break_Even_Year'] else 'N/A',
            str(metrics['Operational_Break_Even_Year']) if metrics['Operational_Break_Even_Year'] else 'N/A',
            '',
            '',
            f"{metrics['Year_1_Enrollment']} students",
            f"{metrics['Year_10_Enrollment']} students",
            f"{metrics['Full_Capacity']} students",
            f"{metrics['Break_Even_Enrollment']} students",
            '',
            '',
            utils.format_currency(metrics['Final_Cash_Balance']),
            utils.format_currency(metrics['Min_Cash_Balance']),
        ]
    }

    return pd.DataFrame(summary_data)


def print_summary(base_case: dict, scenario_comparison: 'pd.DataFrame'):
    """Print summary to console"""
    metrics = base_case['metrics']

    print_header("EXECUTIVE SUMMARY")

    print("\n💰 INVESTMENT REQUIREMENTS:")
    print(f"   Total CAPEX Required:    {utils.format_currency(metrics['Investment_Required'])}")
    print(f"   Equity Investment (40%): {utils.format_currency(metrics['Equity_Required'])}")
    print(f"   Debt Financing (60%):    {utils.format_currency(metrics['Debt_Financing'])}")

    print("\n📈 REVENUE PROJECTIONS:")
    print(f"   Year 1 Revenue:          {utils.format_currency(metrics['Year_1_Revenue'])}")
    print(f"   Year 10 Revenue:         {utils.format_currency(metrics['Year_10_Revenue'])}")
    print(f"   10-Year Total:           {utils.format_currency(metrics['Total_Revenue_10Y'])}")
    print(f"   Revenue CAGR:            {metrics['Revenue_CAGR_%']:.1f}%")

    print("\n💵 PROFITABILITY:")
    print(f"   Year 1 Net Income:       {utils.format_currency(metrics['Year_1_Net_Income'])}")
    print(f"   Year 10 Net Income:      {utils.format_currency(metrics['Year_10_Net_Income'])}")
    print(f"   Avg Operating Margin:    {metrics['Avg_Operating_Margin_%']:.1f}%")
    print(f"   Avg Net Margin:          {metrics['Avg_Net_Margin_%']:.1f}%")

    print("\n📊 FINANCIAL METRICS:")
    print(f"   NPV (15% discount):      {utils.format_currency(metrics['NPV'])}")
    print(f"   IRR:                     {metrics['IRR_%']:.1f}%")
    print(f"   Payback Period:          {metrics['Payback_Period_Years']:.1f} years")
    print(f"   Break-Even Year:         {metrics['Break_Even_Year'] if metrics['Break_Even_Year'] else 'N/A'}")

    print("\n👨‍🎓 ENROLLMENT:")
    print(f"   Year 1 Enrollment:       {metrics['Year_1_Enrollment']} students")
    print(f"   Year 10 Enrollment:      {metrics['Year_10_Enrollment']} students")
    print(f"   Full Capacity:           {metrics['Full_Capacity']} students")
    print(f"   Break-Even Enrollment:   {metrics['Break_Even_Enrollment']} students")

    print("\n💎 INVESTMENT DECISION:")
    if metrics['NPV'] > 0 and metrics['IRR_%'] > 15:
        print("   ✅ FINANCIALLY VIABLE - Strong investment case")
        print(f"   • Positive NPV of {utils.format_currency(metrics['NPV'])}")
        print(f"   • IRR of {metrics['IRR_%']:.1f}% exceeds target of 15%")
    elif metrics['NPV'] > 0:
        print("   ⚠️  MARGINAL - Positive NPV but IRR below target")
    else:
        print("   ❌ NOT VIABLE - Negative NPV and/or insufficient returns")

    print("\n" + "=" * 100)
    print("\n✅ Complete financial model exported to Excel!")
    print("   Review the Excel file for detailed projections, scenarios, and sensitivity analysis.")
    print("\n" + "=" * 100)


if __name__ == '__main__':
    try:
        # Generate and export full model
        filepath = export_full_model()

        print(f"\n📁 Output file: {filepath}")
        print("\nNext steps:")
        print("1. Review the Excel workbook for detailed analysis")
        print("2. Adjust assumptions in config/assumptions.py as needed")
        print("3. Re-run this script to generate updated projections")
        print("4. Share with stakeholders for review and decision-making")

    except Exception as e:
        print(f"\n❌ Error generating financial model: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
