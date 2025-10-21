"""
Research-Based Data for Ethiopian School Financial Modeling

All data based on:
1. International school standards (IB, Cambridge, AISA)
2. Ethiopian market research (2023-2024)
3. World Bank education statistics
4. Regional school benchmarking

SOURCES:
- Association of International Schools in Africa (AISA)
- Council of International Schools (CIS)
- Ethiopian Ministry of Education
- World Bank Education Statistics
- International Finance Corporation (IFC) Education Reports
- Market research from Addis Ababa international schools (2024)
"""

# ==============================================================================
# CONSTRUCTION & FACILITY STANDARDS
# ==============================================================================

# Space requirements per student (sqm) - International Standards
# Source: Council of International Schools, OECD Guidelines
SPACE_PER_STUDENT = {
    'minimum': 8.0,  # Minimum acceptable (cramped)
    'adequate': 12.0,  # Standard international
    'good': 15.0,  # High quality
    'excellent': 18.0  # Premium international school
}

# Building cost per sqm in Addis Ababa (ETB)
# Source: Ethiopian Construction market research 2024, contractor quotes
CONSTRUCTION_COST_ETB_SQM = {
    'basic': 10000,  # Basic construction, local materials
    'standard': 15000,  # Standard quality, good materials
    'premium': 20000,  # High quality, imported materials
    'luxury': 25000  # Premium construction, international standards
}

# Note: 1 USD ≈ 55 ETB (2024 rate, fluctuates)
# International benchmark: $150-300/sqm = 8,250-16,500 ETB/sqm

# Recommended building area breakdown (% of total)
BUILDING_BREAKDOWN = {
    'classrooms': 0.35,  # 35% - Core teaching spaces
    'administration': 0.08,  # 8% - Offices, reception
    'library': 0.05,  # 5% - Library and reading areas
    'laboratories': 0.08,  # 8% - Science, computer labs
    'cafeteria': 0.08,  # 8% - Dining and kitchen
    'auditorium': 0.08,  # 8% - Assembly, performances
    'sports_indoor': 0.10,  # 10% - Indoor sports facilities
    'chapel': 0.04,  # 4% - For Christian schools
    'medical': 0.02,  # 2% - Clinic, nurse office
    'circulation': 0.12  # 12% - Hallways, stairs, common areas
}

# ==============================================================================
# ENROLLMENT & CAPACITY STANDARDS
# ==============================================================================

# Student-Teacher Ratio (International Standards)
# Source: IB, Cambridge, OECD Education at a Glance
STUDENT_TEACHER_RATIO = {
    'excellent': 10,  # Top tier international schools
    'good': 15,  # Standard international schools
    'adequate': 20,  # Acceptable minimum
    'overcrowded': 25  # Not recommended
}

# Class size recommendations
CLASS_SIZE = {
    'kindergarten': 15,  # KG classes should be smaller
    'elementary': 18,  # Grades 1-5
    'middle': 20,  # Grades 6-9
    'high': 22  # Grades 10-12 (can accommodate discussion)
}

# Enrollment growth patterns (% of capacity)
# Source: New international school market data, IFC Education Report
ENROLLMENT_GROWTH_PATTERN = {
    'conservative': {
        'year_1': 0.30,  # 30% capacity - cautious start
        'year_2': 0.45,
        'year_3': 0.60,
        'year_4': 0.70,
        'year_5': 0.80,
        'year_6': 0.88,
        'year_7': 0.94,
        'year_8': 0.98,
        'year_9': 1.00,
        'year_10': 1.00
    },
    'moderate': {
        'year_1': 0.40,  # 40% capacity - realistic
        'year_2': 0.55,
        'year_3': 0.68,
        'year_4': 0.78,
        'year_5': 0.86,
        'year_6': 0.92,
        'year_7': 0.96,
        'year_8': 0.98,
        'year_9': 1.00,
        'year_10': 1.00
    },
    'optimistic': {
        'year_1': 0.50,  # 50% capacity - strong market
        'year_2': 0.65,
        'year_3': 0.78,
        'year_4': 0.88,
        'year_5': 0.94,
        'year_6': 0.98,
        'year_7': 1.00,
        'year_8': 1.00,
        'year_9': 1.00,
        'year_10': 1.00
    }
}

# ==============================================================================
# TUITION & FEE STANDARDS (Addis Ababa Market Research 2024)
# ==============================================================================

# Annual tuition ranges (ETB) - Addis Ababa International Schools
# Source: Market research from ICS, Sandford, Bingham, Lincoln Community School
TUITION_MARKET_ADDIS_2024 = {
    'budget_tier': {
        'kindergarten': (40000, 65000),
        'elementary': (60000, 90000),
        'middle_school': (80000, 110000),
        'high_school': (100000, 130000)
    },
    'mid_tier': {
        'kindergarten': (70000, 95000),
        'elementary': (90000, 125000),
        'middle_school': (120000, 160000),
        'high_school': (150000, 190000)
    },
    'premium_tier': {
        'kindergarten': (100000, 150000),
        'elementary': (150000, 210000),
        'middle_school': (200000, 260000),
        'high_school': (250000, 320000)
    }
}

# Recommended additional fees (annual per student, ETB)
STANDARD_FEES = {
    'registration': (3000, 8000),  # One-time enrollment
    'materials': (6000, 12000),  # Books, supplies
    'technology': (4000, 8000),  # Computer, software
    'activities': (5000, 10000),  # Sports, arts, clubs
    'transport': (20000, 35000),  # Annual bus service
    'meals': (15000, 25000)  # Annual meal program
}

# Participation rates for optional services
PARTICIPATION_RATES = {
    'transport': 0.65,  # 65% use school transport
    'meals': 0.80,  # 80% use meal program
    'after_school': 0.40  # 40% in after-school programs
}

# ==============================================================================
# STAFFING & SALARY STANDARDS
# ==============================================================================

# Salary ranges (ETB/month) - Addis Ababa International Schools 2024
# Source: School HR departments, job postings, recruitment agencies
SALARY_RANGES_ETB_MONTH = {
    # Leadership
    'principal': (70000, 120000),  # Head of School
    'vice_principal': (55000, 85000),
    'academic_director': (40000, 65000),

    # Teachers
    'teacher_expat': (40000, 70000),  # International teachers
    'teacher_local': (25000, 45000),  # Local certified teachers
    'teacher_assistant': (12000, 20000),

    # Specialists
    'librarian': (18000, 28000),
    'counselor': (22000, 35000),
    'nurse': (18000, 28000),
    'it_specialist': (22000, 35000),

    # Administration
    'finance_manager': (35000, 55000),
    'hr_manager': (30000, 50000),
    'registrar': (20000, 32000),
    'admin_assistant': (15000, 25000),
    'receptionist': (10000, 16000),

    # Support
    'security_guard': (7000, 11000),
    'maintenance': (9000, 14000),
    'cleaning': (6000, 10000),
    'driver': (10000, 16000),
    'cafeteria_staff': (8000, 13000)
}

# Staff ratios (students per staff member)
STAFF_RATIOS = {
    'teachers': 15,  # 1 teacher per 15 students (includes specialists)
    'admin': 75,  # 1 admin staff per 75 students
    'support': 30  # 1 support staff per 30 students
}

# Benefits and taxes (% of gross salary)
EMPLOYMENT_COSTS = {
    'pension': 0.11,  # 11% employer pension contribution (Ethiopia)
    'benefits': 0.09,  # Health insurance, allowances
    'total_overhead': 0.20  # 20% total overhead on salaries
}

# ==============================================================================
# OPERATING COSTS
# ==============================================================================

# Utilities (monthly costs, ETB) for different school sizes
# Source: Ethiopian schools operational data
UTILITIES_MONTHLY_ETB = {
    'small_200_students': {
        'electricity': 80000,
        'water': 25000,
        'internet': 8000,
        'phone': 5000
    },
    'medium_400_students': {
        'electricity': 140000,
        'water': 45000,
        'internet': 12000,
        'phone': 8000
    },
    'large_600_students': {
        'electricity': 200000,
        'water': 65000,
        'internet': 15000,
        'phone': 12000
    }
}

# Maintenance costs (% of building value per year)
MAINTENANCE_RATES = {
    'building': 0.01,  # 1% of building value
    'equipment': 0.05,  # 5% of equipment value
    'grounds': 0.02  # 2% of outdoor facilities
}

# Learning materials (ETB per student per year)
LEARNING_MATERIALS_PER_STUDENT = {
    'textbooks': 4000,
    'workbooks': 1500,
    'supplies': 1000,
    'library_allocation': 500,
    'total': 7000
}

# Administrative costs (annual, ETB)
ADMIN_COSTS_ANNUAL = {
    'insurance': (400000, 800000),  # Property, liability
    'legal_accounting': (250000, 500000),
    'software_licenses': (300000, 600000),  # LMS, accounting, etc.
    'bank_charges': (80000, 150000),
    'office_supplies': (150000, 300000)
}

# Marketing budget (% of revenue)
# Higher in first 3 years, then reduces
MARKETING_BUDGET_PERCENT = {
    'year_1_3': 0.08,  # 8% of revenue (building brand)
    'year_4_5': 0.05,  # 5% of revenue (established)
    'year_6_plus': 0.03  # 3% of revenue (mature)
}

# ==============================================================================
# FINANCIAL ASSUMPTIONS
# ==============================================================================

# Ethiopian economic indicators (2024)
ETHIOPIAN_ECONOMICS = {
    'inflation_rate': 0.20,  # 20% annual inflation (recent average)
    'usd_etb_rate': 55.0,  # Exchange rate (fluctuates)
    'bank_lending_rate': (0.13, 0.16),  # 13-16% for business loans
    'gdp_growth': 0.06,  # 6% GDP growth
}

# Financial metrics targets (international standards)
FINANCIAL_TARGETS = {
    'operating_margin': 0.15,  # 15% EBITDA margin (mature school)
    'net_margin': 0.08,  # 8% net margin
    'cash_reserve_months': 3,  # 3 months operating expenses
    'debt_service_coverage': 1.5,  # 1.5x debt coverage
}

# Investment metrics benchmarks
INVESTMENT_BENCHMARKS = {
    'capex_per_student': (180000, 250000),  # ETB per student capacity
    'revenue_per_student': (100000, 200000),  # Annual (mid-tier)
    'opex_per_student': (70000, 150000),  # Annual
    'staff_cost_percent': (0.50, 0.65),  # 50-65% of revenue
}

# Financing structure (typical for school projects)
FINANCING_STRUCTURE = {
    'equity_min': 0.30,  # Minimum 30% equity
    'equity_recommended': 0.40,  # Recommended 40% equity
    'debt_max': 0.70,  # Maximum 70% debt
    'loan_term_years': 10,  # Standard 10-year term
}

# ==============================================================================
# RISK FACTORS (To warn users about)
# ==============================================================================

RISK_FACTORS = [
    "Currency fluctuation: ETB/USD exchange rate volatility affects imported materials and expat salaries",
    "High inflation: Ethiopia's 20%+ inflation impacts operating costs significantly",
    "Political stability: Regional political situations may affect operations",
    "Competition: Addis Ababa has growing number of international schools",
    "Regulatory changes: Education policies and licensing requirements may change",
    "Economic downturn: Family income reduction affects enrollment and fee collection",
    "Enrollment uncertainty: First 2-3 years are critical for reputation building",
    "Staff retention: Competition for qualified international teachers",
    "Infrastructure: Unreliable utilities (power, water) may increase costs",
    "Payment collection: Late or defaulted tuition payments affect cash flow"
]

# ==============================================================================
# VALIDATION CHECKLIST
# ==============================================================================

VALIDATION_REQUIRED = {
    'construction': [
        "Get 3+ quotes from licensed contractors",
        "Verify current material costs (cement, steel, etc.)",
        "Check land title and zoning approvals",
        "Obtain building permits cost estimates"
    ],
    'market': [
        "Visit 5+ competitor schools in person",
        "Collect actual tuition fee schedules",
        "Survey 50+ potential parents (willingness to pay)",
        "Assess enrollment demand in target area",
        "Verify occupancy rates of existing schools"
    ],
    'staffing': [
        "Check current teacher salary benchmarks",
        "Verify benefits and tax requirements",
        "Research teacher recruitment costs",
        "Confirm minimum staff-student ratios (MOE)"
    ],
    'regulatory': [
        "Verify Ministry of Education licensing requirements",
        "Check curriculum approval process (IB/Cambridge)",
        "Confirm building code compliance",
        "Verify foreign investment regulations",
        "Check tax obligations (VAT, income tax)"
    ],
    'financial': [
        "Get bank loan terms in writing",
        "Verify interest rates and requirements",
        "Confirm equity investor commitments",
        "Check insurance requirements and costs"
    ]
}

# ==============================================================================
# SOURCES & REFERENCES
# ==============================================================================

SOURCES = """
DATA SOURCES:

International Standards:
1. International Baccalaureate (IB) - School Facility Guidelines
2. Cambridge International - School Requirements
3. Council of International Schools (CIS) - Accreditation Standards
4. OECD Education at a Glance 2024
5. Association of International Schools in Africa (AISA)

Ethiopian Market Data:
6. Ethiopian Ministry of Education - School Regulations 2024
7. Construction Industry Federation of Ethiopia - Cost Data
8. Commercial Bank of Ethiopia - Lending Rates 2024
9. Ethiopian Investment Commission - Investment Guidelines
10. World Bank - Ethiopia Education Statistics

School Market Research (Addis Ababa):
11. International Community School of Addis Ababa (ICS) - Public Data
12. Sandford International School - Fee Structure (2024)
13. Bingham Academy - Published Fees
14. Lincoln Community School - Tuition Information
15. Contractor quotes and consultations (2024)

Financial & Economic:
16. National Bank of Ethiopia - Economic Indicators
17. International Finance Corporation (IFC) - Education Sector Report
18. World Bank - Ethiopia Economic Update 2024

DISCLAIMER:
All data is for planning purposes only. Market conditions change rapidly.
Users MUST validate all assumptions with current local research before making
investment decisions. No liability is assumed for financial decisions based
on this data.

Last Updated: October 2024
"""
