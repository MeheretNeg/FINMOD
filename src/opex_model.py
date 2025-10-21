"""
OPEX Model - Operating Expenditure calculations
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import assumptions as asmp
from src import utils


class OPEXModel:
    """Calculate all operating expenditures"""

    def __init__(self, scenario: str = 'Base_Case'):
        """
        Initialize OPEX model

        Args:
            scenario: Scenario name from assumptions
        """
        self.scenario = scenario
        self.years = utils.get_year_range()
        self.scenario_opex_factor = asmp.SCENARIOS[scenario].get('opex_factor', 1.0)

    def calculate_staff_salaries(self, year: int) -> Dict[str, float]:
        """
        Calculate total staff salaries and benefits for a year

        Args:
            year: The year to calculate for

        Returns:
            Dictionary with salary breakdown
        """
        # Get staff count for the year
        staff_counts = utils.calculate_staff_count_by_year(year, self.scenario)

        total_annual_salary = 0
        salary_by_category = {}

        for role, count in staff_counts.items():
            # Get base monthly salary
            monthly_salary = asmp.STAFF_STRUCTURE[role]['monthly_salary']

            # Apply inflation
            inflated_salary = utils.apply_inflation(monthly_salary, year, asmp.SALARY_INCREASE_RATE)

            # Calculate annual salary for this role
            annual_salary = inflated_salary * 12 * count

            total_annual_salary += annual_salary
            salary_by_category[role] = annual_salary

        # Calculate benefits and taxes
        benefits = total_annual_salary * asmp.EMPLOYEE_BENEFITS_RATE
        payroll_tax = total_annual_salary * asmp.PAYROLL_TAX_RATE

        # Apply scenario factor
        total_compensation = (total_annual_salary + benefits + payroll_tax) * self.scenario_opex_factor

        return {
            'Base_Salaries': total_annual_salary * self.scenario_opex_factor,
            'Benefits': benefits * self.scenario_opex_factor,
            'Payroll_Tax': payroll_tax * self.scenario_opex_factor,
            'Total_Compensation': total_compensation,
            'Details': salary_by_category
        }

    def calculate_utilities(self, year: int) -> float:
        """
        Calculate annual utilities costs

        Args:
            year: The year to calculate for

        Returns:
            Total annual utilities cost
        """
        # Calculate monthly utilities at full capacity
        monthly_base = sum(asmp.UTILITIES_MONTHLY.values())

        # Scale by enrollment (utilities scale with usage)
        enrollment = utils.get_enrollment_by_year(year, self.scenario)
        scale_factor = min(enrollment / asmp.TOTAL_CAPACITY, 1.0)  # Cap at 100%

        # Apply scaling (minimum 60% even when empty for base utilities)
        scaled_monthly = monthly_base * max(scale_factor, 0.60)

        # Apply inflation
        inflated_monthly = utils.apply_inflation(scaled_monthly, year, asmp.ANNUAL_INFLATION_RATE)

        # Annual cost
        annual_utilities = inflated_monthly * 12 * self.scenario_opex_factor

        return annual_utilities

    def calculate_maintenance(self, year: int) -> float:
        """
        Calculate annual maintenance costs

        Args:
            year: The year to calculate for

        Returns:
            Total annual maintenance cost
        """
        total_maintenance = sum(asmp.MAINTENANCE_ANNUAL.values())

        # Apply inflation
        inflated_maintenance = utils.apply_inflation(total_maintenance, year, asmp.ANNUAL_INFLATION_RATE)

        return inflated_maintenance * self.scenario_opex_factor

    def calculate_learning_materials(self, year: int) -> float:
        """
        Calculate learning materials and supplies costs

        Args:
            year: The year to calculate for

        Returns:
            Total learning materials cost
        """
        enrollment = utils.get_enrollment_by_year(year, self.scenario)

        # Per-student materials
        per_student_cost = asmp.LEARNING_MATERIALS_ANNUAL['Textbooks_per_student']
        per_student_total = per_student_cost * enrollment

        # Fixed costs
        fixed_costs = sum([
            asmp.LEARNING_MATERIALS_ANNUAL['Classroom_Supplies'],
            asmp.LEARNING_MATERIALS_ANNUAL['Lab_Supplies'],
            asmp.LEARNING_MATERIALS_ANNUAL['Library_Books'],
            asmp.LEARNING_MATERIALS_ANNUAL['Sports_Equipment'],
            asmp.LEARNING_MATERIALS_ANNUAL['Art_Supplies'],
        ])

        total_materials = per_student_total + fixed_costs

        # Apply inflation
        inflated_materials = utils.apply_inflation(total_materials, year, asmp.ANNUAL_INFLATION_RATE)

        return inflated_materials * self.scenario_opex_factor

    def calculate_administrative_expenses(self, year: int) -> float:
        """
        Calculate administrative expenses

        Args:
            year: The year to calculate for

        Returns:
            Total administrative expenses
        """
        total_admin = sum(asmp.ADMINISTRATIVE_ANNUAL.values())

        # Apply inflation
        inflated_admin = utils.apply_inflation(total_admin, year, asmp.ANNUAL_INFLATION_RATE)

        return inflated_admin * self.scenario_opex_factor

    def calculate_marketing_expenses(self, year: int) -> float:
        """
        Calculate marketing and recruitment expenses

        Args:
            year: The year to calculate for

        Returns:
            Total marketing expenses
        """
        total_marketing = sum(asmp.MARKETING_ANNUAL.values())

        # Higher marketing in early years
        year_index = self.years.index(year)
        if year_index < 3:
            # Years 1-3: 150% of base marketing
            marketing_factor = 1.5
        elif year_index < 5:
            # Years 4-5: 120% of base marketing
            marketing_factor = 1.2
        else:
            # Year 6+: Normal marketing
            marketing_factor = 1.0

        total_marketing *= marketing_factor

        # Apply inflation
        inflated_marketing = utils.apply_inflation(total_marketing, year, asmp.ANNUAL_INFLATION_RATE)

        return inflated_marketing * self.scenario_opex_factor

    def calculate_professional_development(self, year: int) -> float:
        """
        Calculate professional development expenses

        Args:
            year: The year to calculate for

        Returns:
            Total professional development expenses
        """
        total_pd = sum(asmp.PROFESSIONAL_DEVELOPMENT.values())

        # Apply inflation
        inflated_pd = utils.apply_inflation(total_pd, year, asmp.ANNUAL_INFLATION_RATE)

        return inflated_pd * self.scenario_opex_factor

    def calculate_other_expenses(self, year: int) -> float:
        """
        Calculate other operating expenses

        Args:
            year: The year to calculate for

        Returns:
            Total other expenses
        """
        total_other = sum(asmp.OTHER_OPEX_ANNUAL.values())

        # Apply inflation
        inflated_other = utils.apply_inflation(total_other, year, asmp.ANNUAL_INFLATION_RATE)

        return inflated_other * self.scenario_opex_factor

    def calculate_cost_of_goods_sold(self, year: int) -> float:
        """
        Calculate COGS (transportation, meals, uniforms)

        Args:
            year: The year to calculate for

        Returns:
            Total COGS
        """
        enrollment = utils.get_enrollment_by_year(year, self.scenario)

        # Transportation costs (60% of revenue as cost)
        transport_students = int(enrollment * asmp.TRANSPORT_PARTICIPATION_RATE)
        transport_cost_per_student = asmp.TRANSPORT_FEE_ANNUAL * 0.60  # 60% cost ratio
        transport_cost = transport_students * transport_cost_per_student

        # Meal program costs (65% of revenue as cost)
        meal_students = int(enrollment * asmp.MEAL_PARTICIPATION_RATE)
        meal_cost_per_student = asmp.MEAL_PROGRAM_FEE_ANNUAL * 0.65  # 65% cost ratio
        meal_cost = meal_students * meal_cost_per_student

        # Uniform costs (50% of revenue as cost)
        uniform_cost = enrollment * asmp.UNIFORM_REVENUE_PER_STUDENT * 0.50  # 50% cost ratio

        total_cogs = transport_cost + meal_cost + uniform_cost

        # Apply inflation
        inflated_cogs = utils.apply_inflation(total_cogs, year, asmp.ANNUAL_INFLATION_RATE)

        return inflated_cogs * self.scenario_opex_factor

    def calculate_total_opex(self) -> Dict[int, Dict[str, float]]:
        """
        Calculate all operating expenses by year

        Returns:
            Dictionary with year as key and expense breakdown as value
        """
        opex_by_year = {}

        for year in self.years:
            # Calculate all expense categories
            salaries = self.calculate_staff_salaries(year)
            utilities = self.calculate_utilities(year)
            maintenance = self.calculate_maintenance(year)
            materials = self.calculate_learning_materials(year)
            admin = self.calculate_administrative_expenses(year)
            marketing = self.calculate_marketing_expenses(year)
            prof_dev = self.calculate_professional_development(year)
            other = self.calculate_other_expenses(year)
            cogs = self.calculate_cost_of_goods_sold(year)

            total = (salaries['Total_Compensation'] + utilities + maintenance +
                    materials + admin + marketing + prof_dev + other + cogs)

            opex_by_year[year] = {
                'Staff_Compensation': salaries['Total_Compensation'],
                'Utilities': utilities,
                'Maintenance': maintenance,
                'Learning_Materials': materials,
                'Administrative': admin,
                'Marketing': marketing,
                'Professional_Development': prof_dev,
                'COGS': cogs,
                'Other': other,
                'Total': total
            }

        return opex_by_year

    def get_opex_dataframe(self) -> pd.DataFrame:
        """
        Get OPEX data as DataFrame

        Returns:
            DataFrame with all expenses by year
        """
        opex_data = self.calculate_total_opex()

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(opex_data, orient='index')
        df.index.name = 'Year'
        df.reset_index(inplace=True)

        # Add enrollment for reference
        df['Enrollment'] = df['Year'].apply(lambda y: utils.get_enrollment_by_year(y, self.scenario))

        # Reorder columns
        columns = ['Year', 'Enrollment', 'Staff_Compensation', 'Utilities', 'Maintenance',
                  'Learning_Materials', 'Administrative', 'Marketing', 'Professional_Development',
                  'COGS', 'Other', 'Total']
        df = df[columns]

        return df


if __name__ == '__main__':
    # Test the OPEX model
    print("=" * 80)
    print("OPEX MODEL TEST - BASE CASE")
    print("=" * 80)

    model = OPEXModel(scenario='Base_Case')
    df = model.get_opex_dataframe()

    print("\nOperating Expense Projections (ETB):")
    print(df.to_string(index=False))

    print(f"\n10-Year Total OPEX: {utils.format_currency(df['Total'].sum())}")
    print(f"Average Annual OPEX: {utils.format_currency(df['Total'].mean())}")
    print(f"Year 1 OPEX: {utils.format_currency(df['Total'].iloc[0])}")
    print(f"Year 10 OPEX: {utils.format_currency(df['Total'].iloc[-1])}")

    # Staff breakdown for Year 1
    print("\n" + "=" * 80)
    print("Year 1 Staff Breakdown:")
    print("=" * 80)
    year1 = model.years[0]
    staff_details = model.calculate_staff_salaries(year1)
    staff_counts = utils.calculate_staff_count_by_year(year1, model.scenario)

    for role, count in staff_counts.items():
        salary = staff_details['Details'][role]
        print(f"{role}: {count} x {utils.format_currency(salary/count/12)}/month = {utils.format_currency(salary)}/year")

    print(f"\nTotal Compensation: {utils.format_currency(staff_details['Total_Compensation'])}")
