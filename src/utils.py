"""
Utility functions for the financial model
"""

import pandas as pd
import numpy as np
import numpy_financial as npf
from typing import Dict, List, Tuple
import sys
import os

# Add config to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import assumptions as asmp


def get_year_range() -> List[int]:
    """
    Get list of years for projection

    Returns:
        List of years from launch to end of projection period
    """
    start_year = asmp.SCHOOL_LAUNCH_DATE.year
    return list(range(start_year, start_year + asmp.PROJECTION_YEARS))


def apply_inflation(base_value: float, year: int, inflation_rate: float = None) -> float:
    """
    Apply inflation to a base value

    Args:
        base_value: Base value in first year
        year: Target year
        inflation_rate: Annual inflation rate (default from assumptions)

    Returns:
        Inflated value
    """
    if inflation_rate is None:
        inflation_rate = asmp.ANNUAL_INFLATION_RATE

    start_year = asmp.SCHOOL_LAUNCH_DATE.year
    years_elapsed = year - start_year

    return base_value * ((1 + inflation_rate) ** years_elapsed)


def get_enrollment_by_year(year: int, scenario: str = 'Base_Case') -> int:
    """
    Calculate total student enrollment for a given year

    Args:
        year: The year to calculate enrollment for
        scenario: Scenario name (default: Base_Case)

    Returns:
        Total number of students enrolled
    """
    # Get base enrollment ramp
    ramp_rate = asmp.ENROLLMENT_RAMP.get(year, 1.0)

    # Get grades available in that year
    if year in asmp.GRADES_BY_YEAR:
        available_grades = asmp.GRADES_BY_YEAR[year]
    elif year >= 2029:
        # All grades available from 2029 onwards
        available_grades = [grade for grades in asmp.GRADE_LEVELS.values() for grade in grades]
    else:
        available_grades = asmp.GRADES_BY_YEAR[2026]

    # Calculate capacity for available grades
    capacity = sum(asmp.SECTIONS_PER_GRADE[grade] for grade in available_grades) * asmp.STUDENTS_PER_CLASS

    # Apply ramp rate
    enrollment = int(capacity * ramp_rate)

    # Apply scenario factor
    scenario_factor = asmp.SCENARIOS[scenario]['enrollment_factor']
    enrollment = int(enrollment * scenario_factor)

    return enrollment


def get_enrollment_by_grade(year: int, scenario: str = 'Base_Case') -> Dict[str, int]:
    """
    Calculate enrollment by grade for a given year

    Args:
        year: The year to calculate enrollment for
        scenario: Scenario name

    Returns:
        Dictionary with grade as key and student count as value
    """
    # Get grades available in that year
    if year in asmp.GRADES_BY_YEAR:
        available_grades = asmp.GRADES_BY_YEAR[year]
    elif year >= 2029:
        available_grades = [grade for grades in asmp.GRADE_LEVELS.values() for grade in grades]
    else:
        available_grades = asmp.GRADES_BY_YEAR[2026]

    # Get total enrollment
    total_enrollment = get_enrollment_by_year(year, scenario)

    # Distribute proportionally by capacity
    total_capacity = sum(asmp.SECTIONS_PER_GRADE[grade] for grade in available_grades)

    enrollment_by_grade = {}
    for grade in available_grades:
        grade_capacity = asmp.SECTIONS_PER_GRADE[grade]
        proportion = grade_capacity / total_capacity
        enrollment_by_grade[grade] = int(total_enrollment * proportion)

    return enrollment_by_grade


def calculate_tuition_by_year(year: int) -> Dict[str, float]:
    """
    Calculate tuition fees by grade for a given year (with inflation)

    Args:
        year: The year to calculate tuition for

    Returns:
        Dictionary with grade as key and tuition amount as value
    """
    tuition_by_grade = {}

    for grade, base_tuition in asmp.ANNUAL_TUITION.items():
        tuition_by_grade[grade] = apply_inflation(
            base_tuition,
            year,
            asmp.TUITION_INCREASE_RATE
        )

    return tuition_by_grade


def calculate_staff_count_by_year(year: int, scenario: str = 'Base_Case') -> Dict[str, int]:
    """
    Calculate staff count based on enrollment

    Args:
        year: The year to calculate staff for
        scenario: Scenario name

    Returns:
        Dictionary with staff role as key and count as value
    """
    enrollment = get_enrollment_by_year(year, scenario)
    full_capacity = asmp.TOTAL_CAPACITY

    # Scale factor based on enrollment
    scale_factor = enrollment / full_capacity

    staff_counts = {}

    for role, details in asmp.STAFF_STRUCTURE.items():
        base_count = details['count']

        # Core admin staff always present (minimum 1)
        if role in ['Principal', 'Finance_Manager', 'HR_Manager']:
            staff_counts[role] = base_count
        # Teachers scale with enrollment
        elif role in ['Teachers', 'Teaching_Assistants']:
            # Calculate needed teachers based on student-teacher ratio
            if role == 'Teachers':
                needed = max(int(enrollment / asmp.STUDENT_TEACHER_RATIO), 5)  # Min 5 teachers
                staff_counts[role] = needed
            else:
                staff_counts[role] = max(int(base_count * scale_factor), 2)
        # Other staff scale proportionally (with minimum)
        else:
            scaled_count = int(base_count * scale_factor)
            staff_counts[role] = max(scaled_count, 1)  # Minimum 1

    return staff_counts


def calculate_npv(cash_flows: List[float], discount_rate: float = None) -> float:
    """
    Calculate Net Present Value

    Args:
        cash_flows: List of cash flows by year
        discount_rate: Discount rate (default from assumptions)

    Returns:
        NPV value
    """
    if discount_rate is None:
        discount_rate = asmp.DISCOUNT_RATE

    npv = 0
    for year, cash_flow in enumerate(cash_flows):
        npv += cash_flow / ((1 + discount_rate) ** year)

    return npv


def calculate_irr(cash_flows: List[float], guess: float = 0.1) -> float:
    """
    Calculate Internal Rate of Return using Newton's method

    Args:
        cash_flows: List of cash flows by year
        guess: Initial guess for IRR

    Returns:
        IRR as decimal (e.g., 0.15 for 15%)
    """
    # Use numpy-financial's IRR function
    try:
        return npf.irr(cash_flows)
    except:
        # Fallback to manual calculation
        tolerance = 0.0001
        max_iterations = 1000
        rate = guess

        for _ in range(max_iterations):
            npv = sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cash_flows))
            npv_derivative = sum(-i * cf / ((1 + rate) ** (i + 1)) for i, cf in enumerate(cash_flows))

            if abs(npv) < tolerance:
                return rate

            if npv_derivative == 0:
                return None

            rate = rate - npv / npv_derivative

        return rate


def calculate_payback_period(cash_flows: List[float]) -> float:
    """
    Calculate payback period in years

    Args:
        cash_flows: List of cash flows by year

    Returns:
        Payback period in years (fractional)
    """
    cumulative = 0

    for year, cash_flow in enumerate(cash_flows):
        cumulative += cash_flow

        if cumulative >= 0:
            # Interpolate to get fractional year
            if year == 0:
                return 0

            previous_cumulative = cumulative - cash_flow
            fraction = abs(previous_cumulative) / cash_flow
            return year + fraction

    return None  # Never pays back


def format_currency(amount: float, currency: str = None) -> str:
    """
    Format amount as currency string

    Args:
        amount: Amount to format
        currency: Currency code (default from assumptions)

    Returns:
        Formatted string
    """
    if currency is None:
        currency = asmp.CURRENCY

    return f"{currency} {amount:,.0f}"


def create_summary_dataframe(data_dict: Dict[int, float], name: str) -> pd.DataFrame:
    """
    Create a summary DataFrame from a dictionary

    Args:
        data_dict: Dictionary with year as key and value
        name: Name for the value column

    Returns:
        DataFrame with Year and value columns
    """
    df = pd.DataFrame(list(data_dict.items()), columns=['Year', name])
    return df


def export_to_excel(dataframes: Dict[str, pd.DataFrame], filename: str):
    """
    Export multiple DataFrames to Excel with multiple sheets

    Args:
        dataframes: Dictionary with sheet name as key and DataFrame as value
        filename: Output filename
    """
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)

    filepath = os.path.join(output_dir, filename)

    with pd.ExcelWriter(filepath, engine='xlsxwriter') as writer:
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Auto-adjust column widths
            worksheet = writer.sheets[sheet_name]
            for i, col in enumerate(df.columns):
                max_length = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                )
                worksheet.set_column(i, i, max_length + 2)

    print(f"Excel file exported: {filepath}")
    return filepath
