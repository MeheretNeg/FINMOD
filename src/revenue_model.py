"""
Revenue Model - All revenue streams for the school
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import assumptions as asmp
from src import utils


class RevenueModel:
    """Calculate all revenue streams"""

    def __init__(self, scenario: str = 'Base_Case'):
        """
        Initialize revenue model

        Args:
            scenario: Scenario name from assumptions
        """
        self.scenario = scenario
        self.years = utils.get_year_range()
        self.scenario_tuition_factor = asmp.SCENARIOS[scenario]['tuition_factor']

    def calculate_tuition_revenue(self) -> Dict[int, float]:
        """
        Calculate tuition revenue by year

        Returns:
            Dictionary with year as key and tuition revenue as value
        """
        tuition_revenue = {}

        for year in self.years:
            total_revenue = 0

            # Get enrollment by grade
            enrollment_by_grade = utils.get_enrollment_by_grade(year, self.scenario)

            # Get tuition by grade (with inflation)
            tuition_by_grade = utils.calculate_tuition_by_year(year)

            # Calculate revenue
            for grade, students in enrollment_by_grade.items():
                grade_tuition = tuition_by_grade[grade] * self.scenario_tuition_factor
                total_revenue += students * grade_tuition

            tuition_revenue[year] = total_revenue

        return tuition_revenue

    def calculate_registration_fees(self) -> Dict[int, float]:
        """
        Calculate registration fee revenue (new students only)

        Assumes 25% new students each year after year 1
        """
        registration_revenue = {}

        for i, year in enumerate(self.years):
            enrollment = utils.get_enrollment_by_year(year, self.scenario)

            if i == 0:
                # Year 1: All students are new
                new_students = enrollment
            else:
                # Subsequent years: Estimate new students
                # New KG + natural attrition + growth
                new_students = int(enrollment * 0.25)  # ~25% new each year

            # Apply inflation to registration fee
            fee = utils.apply_inflation(asmp.REGISTRATION_FEE, year, asmp.TUITION_INCREASE_RATE)
            fee *= self.scenario_tuition_factor

            registration_revenue[year] = new_students * fee

        return registration_revenue

    def calculate_materials_fees(self) -> Dict[int, float]:
        """Calculate annual materials and activity fees"""
        materials_revenue = {}

        for year in self.years:
            enrollment = utils.get_enrollment_by_year(year, self.scenario)

            # Apply inflation
            materials_fee = utils.apply_inflation(asmp.ANNUAL_MATERIALS_FEE, year, asmp.TUITION_INCREASE_RATE)
            tech_fee = utils.apply_inflation(asmp.TECHNOLOGY_FEE, year, asmp.TUITION_INCREASE_RATE)
            activity_fee = utils.apply_inflation(asmp.ACTIVITY_FEE, year, asmp.TUITION_INCREASE_RATE)

            # Apply scenario factor
            total_fees = (materials_fee + tech_fee + activity_fee) * self.scenario_tuition_factor

            materials_revenue[year] = enrollment * total_fees

        return materials_revenue

    def calculate_transportation_revenue(self) -> Dict[int, float]:
        """Calculate transportation service revenue"""
        transport_revenue = {}

        for year in self.years:
            enrollment = utils.get_enrollment_by_year(year, self.scenario)
            participating_students = int(enrollment * asmp.TRANSPORT_PARTICIPATION_RATE)

            # Apply inflation
            transport_fee = utils.apply_inflation(asmp.TRANSPORT_FEE_ANNUAL, year, asmp.TUITION_INCREASE_RATE)
            transport_fee *= self.scenario_tuition_factor

            transport_revenue[year] = participating_students * transport_fee

        return transport_revenue

    def calculate_meal_program_revenue(self) -> Dict[int, float]:
        """Calculate meal program revenue"""
        meal_revenue = {}

        for year in self.years:
            enrollment = utils.get_enrollment_by_year(year, self.scenario)
            participating_students = int(enrollment * asmp.MEAL_PARTICIPATION_RATE)

            # Apply inflation
            meal_fee = utils.apply_inflation(asmp.MEAL_PROGRAM_FEE_ANNUAL, year, asmp.TUITION_INCREASE_RATE)
            meal_fee *= self.scenario_tuition_factor

            meal_revenue[year] = participating_students * meal_fee

        return meal_revenue

    def calculate_uniform_sales(self) -> Dict[int, float]:
        """Calculate uniform sales revenue"""
        uniform_revenue = {}

        for year in self.years:
            enrollment = utils.get_enrollment_by_year(year, self.scenario)

            # Apply inflation
            uniform_revenue_per_student = utils.apply_inflation(
                asmp.UNIFORM_REVENUE_PER_STUDENT, year, asmp.ANNUAL_INFLATION_RATE
            )

            uniform_revenue[year] = enrollment * uniform_revenue_per_student

        return uniform_revenue

    def calculate_after_school_revenue(self) -> Dict[int, float]:
        """Calculate after-school program revenue"""
        after_school_revenue = {}

        for year in self.years:
            enrollment = utils.get_enrollment_by_year(year, self.scenario)
            participating_students = int(enrollment * asmp.AFTER_SCHOOL_PARTICIPATION_RATE)

            # Apply inflation
            fee = utils.apply_inflation(asmp.AFTER_SCHOOL_FEE_ANNUAL, year, asmp.TUITION_INCREASE_RATE)
            fee *= self.scenario_tuition_factor

            after_school_revenue[year] = participating_students * fee

        return after_school_revenue

    def calculate_total_revenue(self) -> Dict[int, Dict[str, float]]:
        """
        Calculate all revenue streams

        Returns:
            Dictionary with year as key and dict of revenue streams as value
        """
        # Calculate all revenue streams
        tuition = self.calculate_tuition_revenue()
        registration = self.calculate_registration_fees()
        materials = self.calculate_materials_fees()
        transport = self.calculate_transportation_revenue()
        meals = self.calculate_meal_program_revenue()
        uniforms = self.calculate_uniform_sales()
        after_school = self.calculate_after_school_revenue()

        # Combine all streams
        total_revenue = {}

        for year in self.years:
            total_revenue[year] = {
                'Tuition': tuition[year],
                'Registration_Fees': registration[year],
                'Materials_Fees': materials[year],
                'Transportation': transport[year],
                'Meal_Program': meals[year],
                'Uniform_Sales': uniforms[year],
                'After_School': after_school[year],
                'Total': (tuition[year] + registration[year] + materials[year] +
                         transport[year] + meals[year] + uniforms[year] + after_school[year])
            }

        return total_revenue

    def get_revenue_dataframe(self) -> pd.DataFrame:
        """
        Get revenue data as DataFrame

        Returns:
            DataFrame with all revenue streams by year
        """
        revenue_data = self.calculate_total_revenue()

        # Convert to DataFrame
        df = pd.DataFrame.from_dict(revenue_data, orient='index')
        df.index.name = 'Year'
        df.reset_index(inplace=True)

        # Add enrollment for reference
        df['Enrollment'] = df['Year'].apply(lambda y: utils.get_enrollment_by_year(y, self.scenario))

        # Reorder columns
        columns = ['Year', 'Enrollment', 'Tuition', 'Registration_Fees', 'Materials_Fees',
                  'Transportation', 'Meal_Program', 'Uniform_Sales', 'After_School', 'Total']
        df = df[columns]

        return df


if __name__ == '__main__':
    # Test the revenue model
    print("=" * 80)
    print("REVENUE MODEL TEST - BASE CASE")
    print("=" * 80)

    model = RevenueModel(scenario='Base_Case')
    df = model.get_revenue_dataframe()

    print("\nRevenue Projections (ETB):")
    print(df.to_string(index=False))

    print(f"\n10-Year Total Revenue: {utils.format_currency(df['Total'].sum())}")
    print(f"Average Annual Revenue: {utils.format_currency(df['Total'].mean())}")
    print(f"Year 1 Revenue: {utils.format_currency(df['Total'].iloc[0])}")
    print(f"Year 10 Revenue: {utils.format_currency(df['Total'].iloc[-1])}")
