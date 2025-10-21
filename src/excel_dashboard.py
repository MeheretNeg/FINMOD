"""
Enhanced Excel Export with Professional Formatting and Interactive Charts
"""

import pandas as pd
import xlsxwriter
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import assumptions as asmp
from src import utils
from src.analysis import FinancialAnalysis


class ExcelDashboard:
    """Create professional Excel dashboard with charts and formatting"""

    def __init__(self, scenario: str = 'Base_Case'):
        self.scenario = scenario
        self.analysis = FinancialAnalysis(scenario)
        self.workbook = None
        self.formats = {}

    def create_formats(self):
        """Create reusable formats for the workbook"""

        # Header formats
        self.formats['header'] = self.workbook.add_format({
            'bold': True,
            'font_size': 14,
            'font_color': 'white',
            'bg_color': '#1F4E78',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        self.formats['subheader'] = self.workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        # Data formats
        self.formats['currency'] = self.workbook.add_format({
            'num_format': '#,##0',
            'border': 1,
            'align': 'right'
        })

        self.formats['currency_bold'] = self.workbook.add_format({
            'num_format': '#,##0',
            'border': 1,
            'bold': True,
            'bg_color': '#E7E6E6',
            'align': 'right'
        })

        self.formats['percent'] = self.workbook.add_format({
            'num_format': '0.0%',
            'border': 1,
            'align': 'right'
        })

        self.formats['number'] = self.workbook.add_format({
            'num_format': '#,##0',
            'border': 1,
            'align': 'right'
        })

        self.formats['text'] = self.workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter'
        })

        self.formats['text_bold'] = self.workbook.add_format({
            'border': 1,
            'bold': True,
            'bg_color': '#E7E6E6',
            'align': 'left'
        })

        # KPI formats
        self.formats['kpi_title'] = self.workbook.add_format({
            'bold': True,
            'font_size': 11,
            'bg_color': '#D9E1F2',
            'border': 1,
            'align': 'left',
            'valign': 'vcenter'
        })

        self.formats['kpi_value'] = self.workbook.add_format({
            'bold': True,
            'font_size': 16,
            'font_color': '#1F4E78',
            'border': 1,
            'align': 'right',
            'valign': 'vcenter'
        })

        self.formats['kpi_value_green'] = self.workbook.add_format({
            'bold': True,
            'font_size': 16,
            'font_color': '#00B050',
            'border': 1,
            'align': 'right',
            'valign': 'vcenter'
        })

        self.formats['kpi_value_red'] = self.workbook.add_format({
            'bold': True,
            'font_size': 16,
            'font_color': '#C00000',
            'border': 1,
            'align': 'right',
            'valign': 'vcenter'
        })

        # Title format
        self.formats['title'] = self.workbook.add_format({
            'bold': True,
            'font_size': 18,
            'font_color': '#1F4E78',
            'align': 'left',
            'valign': 'vcenter'
        })

        self.formats['subtitle'] = self.workbook.add_format({
            'font_size': 11,
            'font_color': '#44546A',
            'italic': True,
            'align': 'left'
        })

        # Positive/Negative formatting
        self.formats['positive'] = self.workbook.add_format({
            'num_format': '#,##0',
            'border': 1,
            'font_color': '#00B050',
            'align': 'right'
        })

        self.formats['negative'] = self.workbook.add_format({
            'num_format': '#,##0',
            'border': 1,
            'font_color': '#C00000',
            'align': 'right'
        })

    def create_dashboard(self, worksheet):
        """Create executive dashboard with KPIs and charts"""

        # Set column widths
        worksheet.set_column('A:A', 3)
        worksheet.set_column('B:B', 35)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 3)
        worksheet.set_column('E:E', 35)
        worksheet.set_column('F:F', 20)

        # Title
        worksheet.merge_range('B2:F2', 'ETHIOPIAN INTERNATIONAL CHRISTIAN SCHOOL', self.formats['title'])
        worksheet.merge_range('B3:F3', 'Financial Feasibility Study - Executive Dashboard', self.formats['subtitle'])
        worksheet.write('B4', f'Generated: {datetime.now().strftime("%B %d, %Y")}', self.formats['subtitle'])

        # Get metrics
        metrics = self.analysis.get_key_metrics_summary()

        # Investment Summary (Row 6-10)
        row = 6
        worksheet.merge_range(f'B{row}:C{row}', '💰 INVESTMENT REQUIRED', self.formats['subheader'])
        worksheet.merge_range(f'E{row}:F{row}', '📊 RETURNS', self.formats['subheader'])

        row += 1
        worksheet.write(f'B{row}', 'Total CAPEX', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Investment_Required'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'NPV (15% discount)', self.formats['kpi_title'])
        npv_format = self.formats['kpi_value_green'] if metrics['NPV'] > 0 else self.formats['kpi_value_red']
        worksheet.write(f'F{row}', metrics['NPV'], npv_format)

        row += 1
        worksheet.write(f'B{row}', 'Equity (40%)', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Equity_Required'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'IRR', self.formats['kpi_title'])
        irr_format = self.formats['kpi_value_green'] if metrics['IRR_%'] > 15 else self.formats['kpi_value_red']
        worksheet.write(f'F{row}', metrics['IRR_%']/100, irr_format)
        worksheet.write_formula(f'F{row}', f'={metrics["IRR_%"]}/100', irr_format)

        row += 1
        worksheet.write(f'B{row}', 'Debt (60%)', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Debt_Financing'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'Payback Period', self.formats['kpi_title'])
        worksheet.write(f'F{row}', f"{metrics['Payback_Period_Years']:.1f} years", self.formats['kpi_value'])

        # Revenue & Profitability (Row 12-16)
        row = 12
        worksheet.merge_range(f'B{row}:C{row}', '📈 REVENUE PROJECTIONS', self.formats['subheader'])
        worksheet.merge_range(f'E{row}:F{row}', '💵 PROFITABILITY', self.formats['subheader'])

        row += 1
        worksheet.write(f'B{row}', 'Year 1 Revenue', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Year_1_Revenue'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'Avg Operating Margin', self.formats['kpi_title'])
        worksheet.write(f'F{row}', metrics['Avg_Operating_Margin_%']/100, self.formats['kpi_value'])

        row += 1
        worksheet.write(f'B{row}', 'Year 10 Revenue', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Year_10_Revenue'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'Avg Net Margin', self.formats['kpi_title'])
        worksheet.write(f'F{row}', metrics['Avg_Net_Margin_%']/100, self.formats['kpi_value'])

        row += 1
        worksheet.write(f'B{row}', '10-Year Total Revenue', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Total_Revenue_10Y'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'Total Net Income (10Y)', self.formats['kpi_title'])
        worksheet.write(f'F{row}', metrics['Total_Net_Income_10Y'], self.formats['kpi_value'])

        # Enrollment & Break-even (Row 18-22)
        row = 18
        worksheet.merge_range(f'B{row}:C{row}', '👨‍🎓 ENROLLMENT', self.formats['subheader'])
        worksheet.merge_range(f'E{row}:F{row}', '⚖️ BREAK-EVEN', self.formats['subheader'])

        row += 1
        worksheet.write(f'B{row}', 'Year 1 Enrollment', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Year_1_Enrollment'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'Break-Even Year', self.formats['kpi_title'])
        worksheet.write(f'F{row}', str(metrics['Break_Even_Year']), self.formats['kpi_value'])

        row += 1
        worksheet.write(f'B{row}', 'Full Capacity', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Full_Capacity'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'Break-Even Enrollment', self.formats['kpi_title'])
        worksheet.write(f'F{row}', metrics['Break_Even_Enrollment'], self.formats['kpi_value'])

        row += 1
        worksheet.write(f'B{row}', 'Year 10 Enrollment', self.formats['kpi_title'])
        worksheet.write(f'C{row}', metrics['Year_10_Enrollment'], self.formats['kpi_value'])
        worksheet.write(f'E{row}', 'Operating Break-Even', self.formats['kpi_title'])
        worksheet.write(f'F{row}', str(metrics['Operational_Break_Even_Year']), self.formats['kpi_value'])

        # Investment Decision (Row 24)
        row = 24
        decision_text = '✅ FINANCIALLY VIABLE - Strong Investment Case'
        decision_color = '#00B050'

        if metrics['NPV'] > 0 and metrics['IRR_%'] > 15:
            decision_text = '✅ FINANCIALLY VIABLE - Strong Investment Case'
            decision_color = '#00B050'
        elif metrics['NPV'] > 0:
            decision_text = '⚠️ MARGINAL - Positive NPV but IRR below target'
            decision_color = '#FFC000'
        else:
            decision_text = '❌ NOT VIABLE - Negative NPV'
            decision_color = '#C00000'

        decision_format = self.workbook.add_format({
            'bold': True,
            'font_size': 14,
            'font_color': 'white',
            'bg_color': decision_color,
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        worksheet.merge_range(f'B{row}:F{row}', decision_text, decision_format)
        worksheet.set_row(row-1, 30)

        # Add charts starting at row 26
        self.add_dashboard_charts(worksheet, start_row=26)

    def add_dashboard_charts(self, worksheet, start_row=26):
        """Add charts to dashboard"""

        # Get data for charts
        pl = self.analysis.fs.generate_profit_loss()
        cf = self.analysis.fs.generate_cash_flow()
        revenue_df = self.analysis.fs.revenue_model.get_revenue_dataframe()

        # Chart 1: Revenue & Net Income Trend
        chart1 = self.workbook.add_chart({'type': 'column'})

        # We'll add data to the worksheet first
        chart_data_row = start_row + 15
        worksheet.write(chart_data_row, 1, 'Year')
        worksheet.write(chart_data_row, 2, 'Revenue')
        worksheet.write(chart_data_row, 3, 'Net Income')

        for i, (year, revenue, net_income) in enumerate(zip(pl['Year'], pl['Total_Revenue'], pl['Net_Income'])):
            worksheet.write(chart_data_row + 1 + i, 1, year)
            worksheet.write(chart_data_row + 1 + i, 2, revenue)
            worksheet.write(chart_data_row + 1 + i, 3, net_income)

        chart1.add_series({
            'name': 'Revenue',
            'categories': f'=Dashboard!$B${chart_data_row+2}:$B${chart_data_row+11}',
            'values': f'=Dashboard!$C${chart_data_row+2}:$C${chart_data_row+11}',
            'fill': {'color': '#4472C4'},
        })

        chart1.add_series({
            'name': 'Net Income',
            'categories': f'=Dashboard!$B${chart_data_row+2}:$B${chart_data_row+11}',
            'values': f'=Dashboard!$D${chart_data_row+2}:$D${chart_data_row+11}',
            'fill': {'color': '#70AD47'},
        })

        chart1.set_title({'name': '10-Year Revenue & Net Income Projection'})
        chart1.set_x_axis({'name': 'Year'})
        chart1.set_y_axis({'name': 'Amount (ETB)', 'num_format': '#,##0'})
        chart1.set_size({'width': 600, 'height': 300})
        chart1.set_legend({'position': 'bottom'})

        worksheet.insert_chart(f'B{start_row}', chart1)

        # Chart 2: Cash Flow Trend
        chart2 = self.workbook.add_chart({'type': 'line'})

        chart_data_row2 = start_row + 35
        worksheet.write(chart_data_row2, 1, 'Year')
        worksheet.write(chart_data_row2, 2, 'Cash Balance')
        worksheet.write(chart_data_row2, 3, 'Net Cash Flow')

        for i, (year, balance, net_cf) in enumerate(zip(cf['Year'], cf['Cash_Balance'], cf['Net_Cash_Flow'])):
            worksheet.write(chart_data_row2 + 1 + i, 1, year)
            worksheet.write(chart_data_row2 + 1 + i, 2, balance)
            worksheet.write(chart_data_row2 + 1 + i, 3, net_cf)

        chart2.add_series({
            'name': 'Cash Balance',
            'categories': f'=Dashboard!$B${chart_data_row2+2}:$B${chart_data_row2+11}',
            'values': f'=Dashboard!$C${chart_data_row2+2}:$C${chart_data_row2+11}',
            'line': {'color': '#FFC000', 'width': 2.5},
        })

        chart2.set_title({'name': 'Cash Flow Trend'})
        chart2.set_x_axis({'name': 'Year'})
        chart2.set_y_axis({'name': 'Amount (ETB)', 'num_format': '#,##0'})
        chart2.set_size({'width': 600, 'height': 300})
        chart2.set_legend({'position': 'bottom'})

        worksheet.insert_chart(f'E{start_row+20}', chart2)

        # Chart 3: Enrollment Growth
        chart3 = self.workbook.add_chart({'type': 'area'})

        chart_data_row3 = start_row + 55
        worksheet.write(chart_data_row3, 1, 'Year')
        worksheet.write(chart_data_row3, 2, 'Enrollment')

        for i, (year, enrollment) in enumerate(zip(revenue_df['Year'], revenue_df['Enrollment'])):
            worksheet.write(chart_data_row3 + 1 + i, 1, year)
            worksheet.write(chart_data_row3 + 1 + i, 2, enrollment)

        chart3.add_series({
            'name': 'Student Enrollment',
            'categories': f'=Dashboard!$B${chart_data_row3+2}:$B${chart_data_row3+11}',
            'values': f'=Dashboard!$C${chart_data_row3+2}:$C${chart_data_row3+11}',
            'fill': {'color': '#5B9BD5'},
        })

        chart3.set_title({'name': 'Student Enrollment Growth'})
        chart3.set_x_axis({'name': 'Year'})
        chart3.set_y_axis({'name': 'Students'})
        chart3.set_size({'width': 600, 'height': 300})
        chart3.set_legend({'position': 'bottom'})

        worksheet.insert_chart(f'B{start_row+20}', chart3)

    def format_table(self, worksheet, df, start_row, start_col):
        """Format a DataFrame as a professional table"""

        # Write headers
        for col_num, col_name in enumerate(df.columns):
            worksheet.write(start_row, start_col + col_num, col_name, self.formats['header'])

        # Write data
        for row_num, row_data in enumerate(df.values):
            for col_num, cell_value in enumerate(row_data):
                cell_row = start_row + row_num + 1
                cell_col = start_col + col_num

                # Handle NaN and None values
                import math
                if pd.isna(cell_value) or (isinstance(cell_value, float) and (math.isnan(cell_value) or math.isinf(cell_value))):
                    cell_value = 0  # or 'N/A'

                # Determine format based on column name and value
                col_name = df.columns[col_num]

                if col_num == 0:  # First column (usually Year or label)
                    fmt = self.formats['text_bold']
                elif isinstance(cell_value, str):
                    fmt = self.formats['text']
                elif '%' in col_name or 'Margin' in col_name or 'IRR' in col_name:
                    fmt = self.formats['percent']
                    if isinstance(cell_value, (int, float)):
                        cell_value = cell_value / 100 if cell_value > 1 else cell_value
                elif 'Total' in col_name or col_num == len(df.columns) - 1:
                    fmt = self.formats['currency_bold']
                elif isinstance(cell_value, (int, float)):
                    if cell_value < 0:
                        fmt = self.formats['negative']
                    else:
                        fmt = self.formats['currency']
                else:
                    fmt = self.formats['text']

                worksheet.write(cell_row, cell_col, cell_value, fmt)

        return start_row + len(df) + 1

    def export(self, filename):
        """Export complete dashboard to Excel"""

        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        # Create workbook with NaN handling
        self.workbook = xlsxwriter.Workbook(filepath, {'nan_inf_to_errors': True})
        self.create_formats()

        # Sheet 1: Dashboard
        print("Creating Executive Dashboard...")
        dashboard = self.workbook.add_worksheet('Dashboard')
        self.create_dashboard(dashboard)

        # Sheet 2: Profit & Loss
        print("Formatting Profit & Loss...")
        pl_sheet = self.workbook.add_worksheet('Profit_Loss')
        pl_df = self.analysis.fs.generate_profit_loss()
        self.format_table(pl_sheet, pl_df, 1, 1)
        pl_sheet.set_column('B:B', 12)
        pl_sheet.set_column('C:M', 15)

        # Sheet 3: Cash Flow
        print("Formatting Cash Flow...")
        cf_sheet = self.workbook.add_worksheet('Cash_Flow')
        cf_df = self.analysis.fs.generate_cash_flow()
        self.format_table(cf_sheet, cf_df, 1, 1)
        cf_sheet.set_column('B:B', 12)
        cf_sheet.set_column('C:G', 18)

        # Sheet 4: Revenue Detail
        print("Formatting Revenue Projections...")
        rev_sheet = self.workbook.add_worksheet('Revenue_Detail')
        rev_df = self.analysis.fs.revenue_model.get_revenue_dataframe()
        self.format_table(rev_sheet, rev_df, 1, 1)
        rev_sheet.set_column('B:B', 12)
        rev_sheet.set_column('C:K', 16)

        # Sheet 5: OPEX Detail
        print("Formatting Operating Expenses...")
        opex_sheet = self.workbook.add_worksheet('OPEX_Detail')
        opex_df = self.analysis.fs.opex_model.get_opex_dataframe()
        self.format_table(opex_sheet, opex_df, 1, 1)
        opex_sheet.set_column('B:B', 12)
        opex_sheet.set_column('C:L', 16)

        # Sheet 6: CAPEX
        print("Formatting CAPEX...")
        capex_sheet = self.workbook.add_worksheet('CAPEX_Summary')
        capex_df = self.analysis.fs.capex_model.get_capex_breakdown()
        self.format_table(capex_sheet, capex_df, 1, 1)
        capex_sheet.set_column('B:B', 30)
        capex_sheet.set_column('C:D', 18)

        # Sheet 7: Scenarios
        print("Formatting Scenario Comparison...")
        scenario_sheet = self.workbook.add_worksheet('Scenario_Comparison')
        scenario_df = self.analysis.compare_scenarios()
        self.format_table(scenario_sheet, scenario_df, 1, 1)
        scenario_sheet.set_column('B:C', 25)
        scenario_sheet.set_column('D:K', 16)

        # Close workbook
        self.workbook.close()
        print(f"\n✅ Enhanced Excel dashboard created: {filepath}")
        return filepath


if __name__ == '__main__':
    # Create enhanced dashboard
    dashboard = ExcelDashboard(scenario='Base_Case')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filepath = dashboard.export(f'School_Financial_Dashboard_{timestamp}.xlsx')
    print(f"\n📊 Open this file to view your interactive dashboard!")
