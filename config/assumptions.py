"""
Financial Model Assumptions for Ethiopian International Christian School
All monetary values in Ethiopian Birr (ETB) unless otherwise specified
"""

import numpy as np
from datetime import datetime

# ============================================================================
# PROJECT TIMELINE
# ============================================================================
PROJECT_START_DATE = datetime(2025, 1, 1)  # Planning starts
CONSTRUCTION_START = datetime(2025, 3, 1)
SCHOOL_LAUNCH_DATE = datetime(2026, 9, 1)  # Academic year starts
PROJECTION_YEARS = 10  # Total years to project

# ============================================================================
# ECONOMIC ASSUMPTIONS
# ============================================================================
CURRENCY = "ETB"
USD_TO_ETB_RATE = 55.0  # Ethiopian Birr per USD (2024 rate)
ANNUAL_INFLATION_RATE = 0.20  # 20% (Ethiopia's historical average)
TUITION_INCREASE_RATE = 0.15  # 15% annual increase (below inflation for competitiveness)
SALARY_INCREASE_RATE = 0.18  # 18% annual increase
DISCOUNT_RATE = 0.15  # 15% for NPV calculations

# ============================================================================
# SCHOOL PROFILE
# ============================================================================
SCHOOL_NAME = "Ethiopian International Christian School"
LOCATION = "Addis Ababa, Ethiopia"
CURRICULUM_TYPE = "International (IB/Cambridge) with Christian Foundation"

# ============================================================================
# ENROLLMENT ASSUMPTIONS
# ============================================================================

# Grade structure and capacity
GRADE_LEVELS = {
    'KG': ['KG1', 'KG2'],  # Kindergarten
    'Elementary': ['Grade1', 'Grade2', 'Grade3', 'Grade4', 'Grade5'],
    'Middle': ['Grade6', 'Grade7', 'Grade8', 'Grade9'],
    'High': ['Grade10', 'Grade11', 'Grade12']
}

# Students per class
STUDENTS_PER_CLASS = 20  # International standard: 15-22 students

# Number of sections (classes) per grade at full capacity
SECTIONS_PER_GRADE = {
    'KG1': 2, 'KG2': 2,
    'Grade1': 2, 'Grade2': 2, 'Grade3': 2, 'Grade4': 2, 'Grade5': 2,
    'Grade6': 2, 'Grade7': 2, 'Grade8': 2, 'Grade9': 2,
    'Grade10': 2, 'Grade11': 2, 'Grade12': 2
}

# Total capacity at maturity
TOTAL_CAPACITY = sum(SECTIONS_PER_GRADE.values()) * STUDENTS_PER_CLASS  # 520 students

# Enrollment ramp-up by year (% of capacity)
# Year 1: K-9 only, starting at 40% capacity
# Gradual growth as reputation builds and higher grades added
ENROLLMENT_RAMP = {
    2026: 0.40,  # Year 1: 40% of K-9 capacity (launch year)
    2027: 0.55,  # Year 2: 55% - add Grade 10
    2028: 0.68,  # Year 3: 68% - add Grade 11
    2029: 0.78,  # Year 4: 78% - add Grade 12 (full K-12)
    2030: 0.86,  # Year 5: 86%
    2031: 0.92,  # Year 6: 92%
    2032: 0.96,  # Year 7: 96%
    2033: 0.98,  # Year 8: 98%
    2034: 1.00,  # Year 9: 100% (full capacity)
    2035: 1.00,  # Year 10: 100%
}

# Grades available by year (progressive expansion)
GRADES_BY_YEAR = {
    2026: ['KG1', 'KG2', 'Grade1', 'Grade2', 'Grade3', 'Grade4', 'Grade5',
           'Grade6', 'Grade7', 'Grade8', 'Grade9'],
    2027: ['KG1', 'KG2', 'Grade1', 'Grade2', 'Grade3', 'Grade4', 'Grade5',
           'Grade6', 'Grade7', 'Grade8', 'Grade9', 'Grade10'],
    2028: ['KG1', 'KG2', 'Grade1', 'Grade2', 'Grade3', 'Grade4', 'Grade5',
           'Grade6', 'Grade7', 'Grade8', 'Grade9', 'Grade10', 'Grade11'],
    # From 2029 onwards: Full K-12
}

# ============================================================================
# TUITION & FEES (Annual, in ETB)
# ============================================================================

# Annual tuition by grade (Year 1 prices)
# Based on market research of international schools in Addis Ababa
ANNUAL_TUITION = {
    'KG1': 80000,
    'KG2': 80000,
    'Grade1': 95000,
    'Grade2': 95000,
    'Grade3': 100000,
    'Grade4': 100000,
    'Grade5': 105000,
    'Grade6': 115000,
    'Grade7': 115000,
    'Grade8': 120000,
    'Grade9': 120000,
    'Grade10': 130000,
    'Grade11': 135000,
    'Grade12': 135000,
}

# Other fees (annual per student)
REGISTRATION_FEE = 5000  # One-time per student (paid at enrollment)
ANNUAL_MATERIALS_FEE = 8000  # Books, supplies, etc.
TECHNOLOGY_FEE = 5000  # Annual tech fee
ACTIVITY_FEE = 6000  # Sports, arts, extracurricular

# ============================================================================
# ANCILLARY REVENUE STREAMS
# ============================================================================

# Transportation (optional for students)
TRANSPORT_FEE_ANNUAL = 25000  # Per student per year
TRANSPORT_PARTICIPATION_RATE = 0.65  # 65% of students use transport

# Meal Program (optional)
MEAL_PROGRAM_FEE_ANNUAL = 18000  # Per student per year
MEAL_PARTICIPATION_RATE = 0.80  # 80% of students

# Uniform Sales (one-time per student, profit margin)
UNIFORM_REVENUE_PER_STUDENT = 3500  # Annual average (replacements)

# After-school programs
AFTER_SCHOOL_FEE_ANNUAL = 12000  # Per participating student
AFTER_SCHOOL_PARTICIPATION_RATE = 0.40  # 40% participation

# ============================================================================
# CAPITAL EXPENDITURE (CAPEX)
# ============================================================================

# Land (already owned - no cost)
LAND_COST = 0

# Construction costs (per square meter in ETB)
CONSTRUCTION_COST_PER_SQM = 15000  # Mid-range construction quality

# Building requirements
BUILDING_AREA = {
    'Classrooms': 2500,  # sqm (30 classrooms @ ~80 sqm each)
    'Administration': 400,  # sqm
    'Library': 300,  # sqm
    'Science Labs': 400,  # sqm (4 labs)
    'Computer Labs': 200,  # sqm (2 labs)
    'Cafeteria': 500,  # sqm
    'Auditorium': 600,  # sqm
    'Sports Facilities': 1000,  # sqm (indoor)
    'Chapel': 300,  # sqm (Christian foundation)
    'Staff Rooms': 200,  # sqm
    'Clinic': 100,  # sqm
    'Common Areas': 500,  # sqm (hallways, etc.)
}

TOTAL_BUILDING_AREA = sum(BUILDING_AREA.values())  # 7,000 sqm

# Outdoor facilities
OUTDOOR_FACILITIES = {
    'Playground': 800000,  # ETB
    'Sports Field': 1500000,  # ETB
    'Parking Lot': 600000,  # ETB
    'Landscaping': 500000,  # ETB
}

# Furniture & Equipment (per classroom/facility)
FURNITURE_COSTS = {
    'Classroom_Furniture': 100000,  # Per classroom (30 classrooms)
    'Office_Furniture': 500000,  # All offices
    'Library_Furniture': 300000,  # Library
    'Lab_Equipment': 400000,  # Per lab (6 labs)
    'Cafeteria_Equipment': 600000,  # Kitchen & dining
    'Sports_Equipment': 400000,  # Initial sports equipment
}

# Technology Infrastructure
TECHNOLOGY_COSTS = {
    'Computer_Labs': 3000000,  # 60 computers + setup
    'Classroom_Tech': 80000,  # Per classroom (projector, smartboard)
    'Network_Infrastructure': 1500000,  # WiFi, servers, cabling
    'Security_Systems': 800000,  # CCTV, access control
    'Admin_Software': 500000,  # ERP, LMS licenses
}

# Initial Setup Costs
INITIAL_SETUP_COSTS = {
    'Legal_Licensing': 300000,  # Business registration, permits
    'Curriculum_Development': 500000,  # Materials, training
    'Marketing_Launch': 800000,  # Pre-launch marketing
    'Staff_Recruitment': 400000,  # Recruitment costs
    'Initial_Inventory': 600000,  # Books, supplies, uniforms stock
    'Contingency': 2000000,  # 10% contingency buffer
}

# ============================================================================
# OPERATING EXPENDITURE (OPEX)
# ============================================================================

# STAFFING
# Student-teacher ratio
STUDENT_TEACHER_RATIO = 15  # International standard

# Staff structure (at full capacity)
STAFF_STRUCTURE = {
    # Academic Staff
    'Principal': {'count': 1, 'monthly_salary': 80000},
    'Vice_Principal': {'count': 1, 'monthly_salary': 60000},
    'Academic_Coordinator': {'count': 2, 'monthly_salary': 45000},
    'Teachers': {'count': 35, 'monthly_salary': 30000},  # Calculated from ratio
    'Teaching_Assistants': {'count': 10, 'monthly_salary': 15000},
    'Librarian': {'count': 2, 'monthly_salary': 20000},
    'Lab_Technicians': {'count': 3, 'monthly_salary': 18000},
    'IT_Staff': {'count': 2, 'monthly_salary': 25000},

    # Administrative Staff
    'Finance_Manager': {'count': 1, 'monthly_salary': 40000},
    'HR_Manager': {'count': 1, 'monthly_salary': 35000},
    'Admin_Staff': {'count': 4, 'monthly_salary': 18000},
    'Receptionist': {'count': 2, 'monthly_salary': 12000},

    # Support Staff
    'Nurse': {'count': 2, 'monthly_salary': 20000},
    'Counselor': {'count': 2, 'monthly_salary': 25000},
    'Security_Guards': {'count': 6, 'monthly_salary': 8000},
    'Maintenance_Staff': {'count': 4, 'monthly_salary': 10000},
    'Cleaning_Staff': {'count': 8, 'monthly_salary': 7000},
    'Cafeteria_Staff': {'count': 6, 'monthly_salary': 9000},
    'Transport_Drivers': {'count': 5, 'monthly_salary': 12000},

    # Christian Ministry
    'Chaplain': {'count': 1, 'monthly_salary': 30000},
}

# Benefits & taxes (% of gross salary)
EMPLOYEE_BENEFITS_RATE = 0.20  # 20% (pension, insurance, etc.)
PAYROLL_TAX_RATE = 0.11  # 11% employer contribution (Ethiopia)

# Utilities (monthly at full capacity)
UTILITIES_MONTHLY = {
    'Electricity': 150000,  # ETB/month
    'Water': 50000,  # ETB/month
    'Internet': 15000,  # ETB/month
    'Phone': 10000,  # ETB/month
}

# Maintenance & Repairs (annual)
MAINTENANCE_ANNUAL = {
    'Building_Maintenance': 800000,  # 1% of building value
    'Equipment_Maintenance': 400000,
    'Grounds_Maintenance': 300000,
    'Vehicle_Maintenance': 250000,
}

# Learning Materials & Supplies (annual)
LEARNING_MATERIALS_ANNUAL = {
    'Textbooks_per_student': 5000,
    'Classroom_Supplies': 300000,
    'Lab_Supplies': 400000,
    'Library_Books': 200000,
    'Sports_Equipment': 150000,
    'Art_Supplies': 150000,
}

# Administrative Expenses (annual)
ADMINISTRATIVE_ANNUAL = {
    'Office_Supplies': 200000,
    'Insurance': 600000,  # Property, liability
    'Legal_Accounting': 300000,
    'Bank_Charges': 100000,
    'Subscriptions_Software': 400000,  # LMS, accounting, etc.
}

# Marketing & Student Recruitment (annual)
MARKETING_ANNUAL = {
    'Advertising': 500000,
    'Events_Open_House': 300000,
    'Website_Social_Media': 200000,
    'Promotional_Materials': 200000,
}

# Professional Development (annual)
PROFESSIONAL_DEVELOPMENT = {
    'Teacher_Training': 600000,  # Workshops, conferences
    'Staff_Development': 300000,
}

# Other Operating Costs
OTHER_OPEX_ANNUAL = {
    'Student_Activities': 400000,
    'Field_Trips': 300000,
    'Community_Outreach': 200000,  # Christian mission focus
    'Miscellaneous': 300000,
}

# ============================================================================
# FINANCIAL METRICS TARGETS
# ============================================================================
TARGET_OPERATING_MARGIN = 0.20  # 20% operating margin at maturity
MINIMUM_CASH_RESERVE_MONTHS = 3  # 3 months of operating expenses
TARGET_IRR = 0.18  # 18% target IRR
TARGET_PAYBACK_PERIOD = 7  # years

# ============================================================================
# WORKING CAPITAL ASSUMPTIONS
# ============================================================================
ACCOUNTS_RECEIVABLE_DAYS = 30  # Days to collect tuition
INVENTORY_DAYS = 60  # Days of supplies on hand
ACCOUNTS_PAYABLE_DAYS = 45  # Days to pay suppliers

# ============================================================================
# FINANCING ASSUMPTIONS (if needed)
# ============================================================================
EQUITY_CONTRIBUTION = 0.40  # 40% equity
DEBT_CONTRIBUTION = 0.60  # 60% debt (if needed)
LOAN_INTEREST_RATE = 0.14  # 14% annual interest (Ethiopian bank rate)
LOAN_TERM_YEARS = 10  # 10-year loan term

# ============================================================================
# SENSITIVITY ANALYSIS PARAMETERS
# ============================================================================
SENSITIVITY_VARIABLES = {
    'enrollment': [-20, -10, 0, 10, 20],  # % change
    'tuition': [-15, -10, 0, 10, 15],  # % change
    'opex': [-10, 0, 10, 20, 30],  # % change
    'capex': [-15, 0, 15, 30, 45],  # % change
}

# ============================================================================
# SCENARIOS
# ============================================================================
SCENARIOS = {
    'Base_Case': {
        'enrollment_factor': 1.0,
        'tuition_factor': 1.0,
        'opex_factor': 1.0,
        'description': 'Expected case with stated assumptions'
    },
    'Optimistic': {
        'enrollment_factor': 1.15,  # 15% higher enrollment
        'tuition_factor': 1.10,  # 10% higher tuition
        'opex_factor': 0.95,  # 5% lower costs (efficiency)
        'description': 'Strong market acceptance and operational efficiency'
    },
    'Conservative': {
        'enrollment_factor': 0.80,  # 20% lower enrollment
        'tuition_factor': 0.90,  # 10% lower tuition (competitive pressure)
        'opex_factor': 1.15,  # 15% higher costs
        'description': 'Slower growth and higher costs'
    },
    'Worst_Case': {
        'enrollment_factor': 0.65,  # 35% lower enrollment
        'tuition_factor': 0.85,  # 15% lower tuition
        'opex_factor': 1.25,  # 25% higher costs
        'description': 'Severe market challenges'
    }
}
