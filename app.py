"""
Ethiopian School Financial Modeling - Interactive Web Application

A user-friendly web app for creating financial feasibility studies for schools in Ethiopia.
No finance or accounting knowledge required!

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(__file__))

from src.revenue_model import RevenueModel
from src.capex_model import CAPEXModel
from src.opex_model import OPEXModel
from src.financial_statements import FinancialStatements
from src.analysis import FinancialAnalysis
from src.excel_dashboard import ExcelDashboard
from config import assumptions as asmp

# Page config
st.set_page_config(
    page_title="Ethiopian School Financial Model",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .big-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #1f4e78;
    }
    .success-box {
        padding: 20px;
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        border-radius: 5px;
        margin: 10px 0;
    }
    .warning-box {
        padding: 20px;
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        border-radius: 5px;
        margin: 10px 0;
    }
    .danger-box {
        padding: 20px;
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)


def format_etb(amount):
    """Format amount as Ethiopian Birr"""
    return f"ETB {amount:,.0f}"


def format_usd(amount):
    """Format amount as USD"""
    return f"${amount:,.0f}"


def main():
    # Header
    st.markdown("<h1 style='text-align: center; color: #1f4e78;'>🎓 Ethiopian School Financial Model</h1>",
                unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666;'>Plan Your School Launch with Confidence</h3>",
                unsafe_allow_html=True)
    st.markdown("---")

    # Sidebar - School Setup
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/1f4e78/ffffff?text=Your+School+Here",
                 use_column_width=True)

        st.markdown("## 🏫 School Setup")

        school_name = st.text_input("School Name", "Ethiopian International Christian School")
        location = st.text_input("Location", "Addis Ababa, Ethiopia")

        launch_year = st.selectbox("Launch Year", [2025, 2026, 2027, 2028], index=1)
        launch_month = st.selectbox("Launch Month",
                                    ["January", "February", "March", "April", "May", "June",
                                     "July", "August", "September", "October", "November", "December"],
                                    index=8)  # September

        st.markdown("---")
        st.markdown("## 💡 Quick Tips")
        st.info("""
        📊 **Adjust the parameters** on each tab to match your school plan

        🔄 **Results update instantly** as you change inputs

        📥 **Download** your Excel report anytime

        💰 All amounts in Ethiopian Birr (ETB)
        """)

    # Main tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Dashboard",
        "💰 Investment & Costs",
        "📈 Revenue & Fees",
        "👥 Students & Staff",
        "📉 Results & Analysis",
        "📥 Download Report"
    ])

    # Initialize session state for parameters
    if 'params' not in st.session_state:
        st.session_state.params = {}

    # TAB 1: DASHBOARD
    with tab1:
        st.markdown("### 🎯 Quick Overview")
        st.markdown("See your school's financial viability at a glance. Adjust parameters in other tabs.")

        # Quick inputs for immediate feedback
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 🏗️ Construction")
            building_size = st.number_input(
                "Building Size (sqm)",
                min_value=3000,
                max_value=15000,
                value=7000,
                step=500,
                help="Total covered area including classrooms, offices, facilities"
            )
            cost_per_sqm = st.number_input(
                "Construction Cost (ETB/sqm)",
                min_value=8000,
                max_value=25000,
                value=15000,
                step=1000,
                help="Based on Ethiopian construction market rates"
            )

        with col2:
            st.markdown("#### 🎓 Students")
            year1_students = st.number_input(
                "Year 1 Students",
                min_value=50,
                max_value=500,
                value=176,
                step=10,
                help="How many students will enroll in your first year?"
            )
            full_capacity = st.number_input(
                "Full Capacity",
                min_value=200,
                max_value=1000,
                value=560,
                step=20,
                help="Maximum students when fully operational"
            )

        with col3:
            st.markdown("#### 💵 Tuition")
            avg_tuition = st.number_input(
                "Average Tuition (ETB/year)",
                min_value=30000,
                max_value=200000,
                value=100000,
                step=5000,
                help="Average annual tuition across all grades"
            )

        # Calculate quick metrics
        construction_cost = building_size * cost_per_sqm
        equipment_tech = construction_cost * 0.25  # ~25% of construction
        setup_costs = construction_cost * 0.05  # ~5% of construction
        total_capex = construction_cost + equipment_tech + setup_costs

        year1_revenue = year1_students * avg_tuition * 1.2  # 1.2x for other fees

        # Display quick results
        st.markdown("---")
        st.markdown("### 💡 Quick Estimate")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Investment", format_etb(total_capex),
                     delta=format_usd(total_capex/55), delta_color="off")

        with col2:
            st.metric("Year 1 Revenue", format_etb(year1_revenue),
                     delta=f"{year1_students} students")

        with col3:
            years_to_full = round((full_capacity - year1_students) / (year1_students * 0.2), 1)
            st.metric("Years to Full Capacity", f"{years_to_full} years",
                     delta=f"{full_capacity} students")

        with col4:
            simple_roi = (year1_revenue - (total_capex * 0.2)) / total_capex * 100
            st.metric("Est. Return", f"{simple_roi:.1f}%",
                     delta="per year" if simple_roi > 0 else "")

        st.info("👆 **These are simplified estimates.** Use other tabs for detailed modeling and click 'Results & Analysis' for full financial projections!")

    # TAB 2: INVESTMENT & COSTS
    with tab2:
        st.markdown("### 💰 Investment Requirements & Costs")
        st.markdown("Tell us about your construction plans and initial investment.")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🏗️ Construction & Facilities")

            with st.expander("ℹ️ How much building space do you need?", expanded=True):
                st.markdown("""
                **Typical space requirements:**
                - **Small school** (200-300 students): 3,000-4,000 sqm
                - **Medium school** (300-500 students): 5,000-7,000 sqm
                - **Large school** (500-800 students): 7,000-10,000 sqm

                Includes: Classrooms, offices, library, labs, cafeteria, auditorium, sports facilities
                """)

            total_building_area = st.slider(
                "Total Building Area (sqm)",
                min_value=3000,
                max_value=12000,
                value=7000,
                step=500
            )

            construction_cost_sqm = st.slider(
                "Construction Cost per sqm (ETB)",
                min_value=8000,
                max_value=25000,
                value=15000,
                step=1000,
                help="Quality: 8-12k=Basic, 12-18k=Standard, 18-25k=Premium"
            )

            st.markdown("**Construction Breakdown:**")
            st.markdown(f"- Classrooms (35%): {format_etb(total_building_area * 0.35 * construction_cost_sqm)}")
            st.markdown(f"- Admin & Offices (10%): {format_etb(total_building_area * 0.10 * construction_cost_sqm)}")
            st.markdown(f"- Facilities (55%): {format_etb(total_building_area * 0.55 * construction_cost_sqm)}")

            st.markdown("---")

            outdoor_facilities = st.number_input(
                "Outdoor Facilities (ETB)",
                min_value=1000000,
                max_value=10000000,
                value=3400000,
                step=500000,
                help="Playground, sports field, parking, landscaping"
            )

        with col2:
            st.markdown("#### 🖥️ Equipment & Technology")

            num_classrooms = st.number_input(
                "Number of Classrooms",
                min_value=10,
                max_value=50,
                value=30,
                step=1
            )

            furniture_per_classroom = st.number_input(
                "Furniture per Classroom (ETB)",
                min_value=50000,
                max_value=200000,
                value=100000,
                step=10000,
                help="Desks, chairs, teacher desk, storage"
            )

            tech_per_classroom = st.number_input(
                "Technology per Classroom (ETB)",
                min_value=30000,
                max_value=150000,
                value=80000,
                step=10000,
                help="Projector, smartboard, sound system"
            )

            st.markdown("---")

            computer_lab_cost = st.number_input(
                "Computer Labs (ETB)",
                min_value=1000000,
                max_value=5000000,
                value=3000000,
                step=500000,
                help="2-3 labs with computers, software, networking"
            )

            other_equipment = st.number_input(
                "Other Equipment (ETB)",
                min_value=2000000,
                max_value=10000000,
                value=5000000,
                step=500000,
                help="Science labs, library, sports, cafeteria equipment"
            )

            initial_setup = st.number_input(
                "Initial Setup Costs (ETB)",
                min_value=2000000,
                max_value=10000000,
                value=4600000,
                step=500000,
                help="Legal, licensing, curriculum, marketing, initial inventory"
            )

        # Calculate total CAPEX
        total_construction = total_building_area * construction_cost_sqm + outdoor_facilities
        total_equipment = (num_classrooms * (furniture_per_classroom + tech_per_classroom) +
                          computer_lab_cost + other_equipment)
        total_capex_calc = total_construction + total_equipment + initial_setup

        st.markdown("---")
        st.markdown("### 💰 Total Investment Required")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Construction", format_etb(total_construction))
        with col2:
            st.metric("Equipment & Tech", format_etb(total_equipment))
        with col3:
            st.metric("Setup Costs", format_etb(initial_setup))
        with col4:
            st.metric("**TOTAL INVESTMENT**", format_etb(total_capex_calc),
                     delta=format_usd(total_capex_calc/55))

        # Financing structure
        st.markdown("---")
        st.markdown("### 🏦 Financing Structure")

        col1, col2 = st.columns(2)

        with col1:
            equity_percent = st.slider(
                "Equity (Own Money) %",
                min_value=20,
                max_value=100,
                value=40,
                step=5,
                help="Percentage funded from own capital/investors"
            )

            equity_amount = total_capex_calc * (equity_percent / 100)
            st.success(f"**Equity Required:** {format_etb(equity_amount)}")

        with col2:
            debt_percent = 100 - equity_percent
            interest_rate = st.slider(
                "Loan Interest Rate %",
                min_value=8.0,
                max_value=20.0,
                value=14.0,
                step=0.5,
                help="Annual interest rate from Ethiopian banks"
            )

            debt_amount = total_capex_calc * (debt_percent / 100)
            st.info(f"**Debt (Loan):** {format_etb(debt_amount)}")

            if debt_amount > 0:
                annual_payment = debt_amount * (interest_rate/100) / (1 - (1 + interest_rate/100)**-10)
                st.caption(f"Est. Annual Payment: {format_etb(annual_payment)} (10 years)")

        # Store in session state
        st.session_state.params['total_capex'] = total_capex_calc
        st.session_state.params['equity_percent'] = equity_percent
        st.session_state.params['debt_percent'] = debt_percent

    # TAB 3: REVENUE & FEES
    with tab3:
        st.markdown("### 📈 Revenue: Tuition & Fees")
        st.markdown("Set your tuition rates based on market research in Addis Ababa.")

        # Market reference
        with st.expander("📊 Tuition Market Research - Addis Ababa International Schools", expanded=True):
            st.markdown("""
            **Current Market Rates (2024-2025):**

            | School Type | KG/Pre-K | Elementary | Middle School | High School |
            |------------|----------|------------|---------------|-------------|
            | **Budget International** | 40-60k | 60-80k | 80-100k | 100-120k |
            | **Mid-Range International** | 70-90k | 90-120k | 120-150k | 150-180k |
            | **Premium International** | 100-150k | 150-200k | 200-250k | 250-300k |

            *ETB per year, based on ICS, Sandford, Bingham Academy*
            """)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎨 Kindergarten & Elementary")

            kg_tuition = st.number_input(
                "KG (Pre-K & KG1-2) - Annual Tuition (ETB)",
                min_value=30000,
                max_value=200000,
                value=80000,
                step=5000
            )

            elem_lower = st.number_input(
                "Elementary (Grade 1-3) - Annual Tuition (ETB)",
                min_value=40000,
                max_value=250000,
                value=95000,
                step=5000
            )

            elem_upper = st.number_input(
                "Elementary (Grade 4-5) - Annual Tuition (ETB)",
                min_value=50000,
                max_value=250000,
                value=105000,
                step=5000
            )

        with col2:
            st.markdown("#### 🎓 Middle & High School")

            middle_tuition = st.number_input(
                "Middle School (Grade 6-9) - Annual Tuition (ETB)",
                min_value=60000,
                max_value=300000,
                value=120000,
                step=5000
            )

            high_tuition = st.number_input(
                "High School (Grade 10-12) - Annual Tuition (ETB)",
                min_value=80000,
                max_value=350000,
                value=135000,
                step=5000
            )

        st.markdown("---")
        st.markdown("#### 💳 Additional Fees (Annual per Student)")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            registration_fee = st.number_input(
                "Registration (one-time)",
                min_value=2000,
                max_value=20000,
                value=5000,
                step=500
            )

        with col2:
            materials_fee = st.number_input(
                "Books & Materials",
                min_value=3000,
                max_value=15000,
                value=8000,
                step=500
            )

        with col3:
            technology_fee = st.number_input(
                "Technology Fee",
                min_value=2000,
                max_value=10000,
                value=5000,
                step=500
            )

        with col4:
            activity_fee = st.number_input(
                "Activity Fee",
                min_value=2000,
                max_value=15000,
                value=6000,
                step=500
            )

        st.markdown("---")
        st.markdown("#### 🚌 Optional Services (% of students who use)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Transportation**")
            transport_rate = st.slider(
                "% of Students Using Transport",
                min_value=0,
                max_value=100,
                value=65,
                step=5
            )
            transport_fee = st.number_input(
                "Annual Transport Fee (ETB)",
                min_value=10000,
                max_value=50000,
                value=25000,
                step=1000
            )

        with col2:
            st.markdown("**Meal Program**")
            meal_rate = st.slider(
                "% of Students in Meal Program",
                min_value=0,
                max_value=100,
                value=80,
                step=5
            )
            meal_fee = st.number_input(
                "Annual Meal Fee (ETB)",
                min_value=8000,
                max_value=40000,
                value=18000,
                step=1000
            )

        # Calculate average revenue per student
        avg_tuition_all = (kg_tuition + elem_lower + elem_upper + middle_tuition + high_tuition) / 5
        avg_fees = registration_fee/4 + materials_fee + technology_fee + activity_fee  # Registration amortized
        avg_optional = (transport_fee * transport_rate/100) + (meal_fee * meal_rate/100)
        avg_revenue_per_student = avg_tuition_all + avg_fees + avg_optional

        st.markdown("---")
        st.success(f"**💰 Average Revenue per Student:** {format_etb(avg_revenue_per_student)} per year")

        # Store in session state
        st.session_state.params['avg_revenue_per_student'] = avg_revenue_per_student

    # TAB 4: STUDENTS & STAFF
    with tab4:
        st.markdown("### 👥 Student Enrollment & Staff Planning")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎓 Enrollment Projections")

            with st.expander("ℹ️ How to project enrollment?", expanded=True):
                st.markdown("""
                **Realistic enrollment growth:**
                - **Year 1**: 30-50% of capacity (building reputation)
                - **Year 2-3**: 50-70% (word of mouth spreads)
                - **Year 4-6**: 70-90% (established school)
                - **Year 7+**: 90-100% (full capacity)

                Be conservative! Better to exceed than underperform.
                """)

            total_capacity = st.number_input(
                "Full School Capacity (students)",
                min_value=200,
                max_value=1000,
                value=560,
                step=20,
                help="Maximum students when all grades at full capacity"
            )

            year1_percentage = st.slider(
                "Year 1 Enrollment (% of capacity)",
                min_value=20,
                max_value=80,
                value=40,
                step=5,
                help="First year is critical - be realistic!"
            )

            year1_enrollment = int(total_capacity * year1_percentage / 100)

            st.markdown("**Enrollment Growth:**")
            year2_pct = st.slider("Year 2 (%)", 30, 90, 55, 5)
            year3_pct = st.slider("Year 3 (%)", 40, 95, 68, 5)
            year4_pct = st.slider("Year 4 (%)", 50, 100, 78, 5)
            year5_pct = st.slider("Year 5 (%)", 60, 100, 86, 5)

            # Create growth chart
            years = ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5']
            enrollment_pcts = [year1_percentage, year2_pct, year3_pct, year4_pct, year5_pct]
            enrollments = [int(total_capacity * pct / 100) for pct in enrollment_pcts]

            fig_enrollment = go.Figure()
            fig_enrollment.add_trace(go.Bar(
                x=years,
                y=enrollments,
                text=enrollments,
                textposition='auto',
                marker_color='#1f77b4'
            ))
            fig_enrollment.update_layout(
                title="Enrollment Growth Projection",
                yaxis_title="Number of Students",
                height=300
            )
            st.plotly_chart(fig_enrollment, use_container_width=True)

        with col2:
            st.markdown("#### 👨‍🏫 Staffing Requirements")

            student_teacher_ratio = st.slider(
                "Student-Teacher Ratio",
                min_value=10,
                max_value=25,
                value=15,
                step=1,
                help="International standard: 12-18 students per teacher"
            )

            teachers_needed_yr1 = max(int(year1_enrollment / student_teacher_ratio), 5)

            st.info(f"**Year 1:** Need approximately **{teachers_needed_yr1} teachers**")

            st.markdown("---")
            st.markdown("**Salary Structure (Monthly, ETB):**")

            principal_salary = st.number_input(
                "Principal/Head of School",
                min_value=40000,
                max_value=150000,
                value=80000,
                step=5000
            )

            teacher_salary = st.number_input(
                "Teachers (average)",
                min_value=15000,
                max_value=60000,
                value=30000,
                step=2000
            )

            admin_salary = st.number_input(
                "Admin Staff (average)",
                min_value=10000,
                max_value=40000,
                value=18000,
                step=1000
            )

            support_salary = st.number_input(
                "Support Staff (average)",
                min_value=6000,
                max_value=20000,
                value=9000,
                step=500
            )

            # Calculate Year 1 staff costs
            num_admin = max(int(year1_enrollment / 70), 4)  # ~1 admin per 70 students
            num_support = max(int(year1_enrollment / 30), 8)  # ~1 support per 30 students

            monthly_staff_cost = (
                principal_salary +
                (teachers_needed_yr1 * teacher_salary) +
                (num_admin * admin_salary) +
                (num_support * support_salary)
            )

            annual_staff_cost = monthly_staff_cost * 12 * 1.31  # +31% for benefits and taxes

            st.markdown("---")
            st.markdown(f"**Year 1 Staffing:**")
            st.markdown(f"- Principal: 1")
            st.markdown(f"- Teachers: {teachers_needed_yr1}")
            st.markdown(f"- Admin Staff: {num_admin}")
            st.markdown(f"- Support Staff: {num_support}")
            st.markdown(f"- **Total Staff:** {1 + teachers_needed_yr1 + num_admin + num_support}")

            st.success(f"**Total Staff Cost (Year 1):** {format_etb(annual_staff_cost)}/year")

        # Operating expenses estimate
        st.markdown("---")
        st.markdown("### 💸 Other Operating Expenses (Annual)")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            utilities_monthly = st.number_input(
                "Utilities (Monthly)",
                min_value=50000,
                max_value=500000,
                value=150000,
                step=10000,
                help="Electricity, water, internet"
            )

        with col2:
            maintenance_annual = st.number_input(
                "Maintenance (Annual)",
                min_value=200000,
                max_value=3000000,
                value=800000,
                step=100000,
                help="Building, equipment repairs"
            )

        with col3:
            materials_annual = st.number_input(
                "Learning Materials",
                min_value=300000,
                max_value=3000000,
                value=1000000,
                step=100000,
                help="Books, supplies, equipment"
            )

        with col4:
            marketing_annual = st.number_input(
                "Marketing (Annual)",
                min_value=200000,
                max_value=3000000,
                value=1200000,
                step=100000,
                help="More in early years"
            )

        total_opex_yr1 = (
            annual_staff_cost +
            (utilities_monthly * 12) +
            maintenance_annual +
            materials_annual +
            marketing_annual +
            (year1_enrollment * 10000)  # Other costs per student
        )

        st.info(f"**💰 Total Operating Expenses (Year 1):** {format_etb(total_opex_yr1)}")

        # Store in session state
        st.session_state.params['year1_enrollment'] = year1_enrollment
        st.session_state.params['total_opex_yr1'] = total_opex_yr1

    # TAB 5: RESULTS & ANALYSIS
    with tab5:
        st.markdown("### 📊 Financial Analysis & Projections")

        # Calculate simple projections
        total_capex_val = st.session_state.params.get('total_capex', 128400000)
        avg_revenue = st.session_state.params.get('avg_revenue_per_student', 120000)
        year1_students = st.session_state.params.get('year1_enrollment', 176)
        opex_yr1 = st.session_state.params.get('total_opex_yr1', 40000000)

        # Year 1 financials
        revenue_yr1 = year1_students * avg_revenue
        ebitda_yr1 = revenue_yr1 - opex_yr1

        # Display key metrics
        st.markdown("### 💡 Year 1 Financial Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Investment", format_etb(total_capex_val),
                     delta=format_usd(total_capex_val/55))

        with col2:
            st.metric("Year 1 Revenue", format_etb(revenue_yr1),
                     delta=f"{year1_students} students")

        with col3:
            st.metric("Operating Expenses", format_etb(opex_yr1),
                     delta=f"{(opex_yr1/revenue_yr1*100):.0f}% of revenue")

        with col4:
            color = "normal" if ebitda_yr1 > 0 else "inverse"
            st.metric("Operating Profit (EBITDA)", format_etb(ebitda_yr1),
                     delta="Profit" if ebitda_yr1 > 0 else "Loss")

        # Investment decision
        st.markdown("---")

        # Simple NPV calculation (simplified)
        years_projection = 10
        growth_rate = 0.25  # 25% revenue growth
        discount_rate = 0.15  # 15% discount rate

        cash_flows = []
        for year in range(years_projection):
            if year == 0:
                cf = -total_capex_val  # Initial investment
            else:
                revenue = revenue_yr1 * ((1 + growth_rate) ** year)
                opex = opex_yr1 * ((1 + 0.18) ** year)  # 18% opex growth (inflation)
                cf = (revenue - opex) * 0.7  # After depreciation and tax
            cash_flows.append(cf)

        # Calculate NPV
        npv = sum([cf / ((1 + discount_rate) ** i) for i, cf in enumerate(cash_flows)])

        # Calculate simple payback
        cumulative = 0
        payback_years = years_projection
        for i, cf in enumerate(cash_flows):
            cumulative += cf
            if cumulative > 0 and payback_years == years_projection:
                payback_years = i

        # Investment decision
        if npv > 0 and ebitda_yr1 > -revenue_yr1 * 0.5:  # Reasonable first year loss
            st.markdown("""
                <div class="success-box">
                <h3>✅ FINANCIALLY VIABLE</h3>
                <p><strong>This school project shows strong investment potential!</strong></p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Net Present Value (NPV)", format_etb(npv),
                         delta="Positive ✅")
            with col2:
                st.metric("Est. Payback Period", f"{payback_years} years",
                         delta="Good" if payback_years <= 6 else "Long")
            with col3:
                roi = (npv / total_capex_val) * 100
                st.metric("Return on Investment", f"{roi:.1f}%",
                         delta="Strong" if roi > 20 else "Moderate")

        elif npv > 0:
            st.markdown("""
                <div class="warning-box">
                <h3>⚠️ MARGINAL VIABILITY</h3>
                <p><strong>The project is viable but has risks.</strong> Consider adjusting assumptions or reducing costs.</p>
                </div>
            """, unsafe_allow_html=True)

            st.metric("Net Present Value (NPV)", format_etb(npv))
            st.warning("💡 **Suggestions:** Increase tuition, reduce costs, or improve enrollment projections")

        else:
            st.markdown("""
                <div class="danger-box">
                <h3>❌ NOT FINANCIALLY VIABLE</h3>
                <p><strong>Based on current assumptions, this project may not succeed.</strong></p>
                </div>
            """, unsafe_allow_html=True)

            st.metric("Net Present Value (NPV)", format_etb(npv), delta="Negative ❌")

            st.error("""
            🚨 **Critical Issues to Address:**
            - Are construction costs too high? (Try to reduce by 20-30%)
            - Is enrollment projection realistic? (Can you get more students?)
            - Are tuition fees competitive? (Research market rates)
            - Can operating costs be optimized? (Review staffing and expenses)
            """)

        # 10-year projection chart
        st.markdown("---")
        st.markdown("### 📈 10-Year Revenue & Profit Projection")

        years_labels = [f"Year {i+1}" for i in range(10)]
        revenues = []
        profits = []

        for year in range(10):
            rev = revenue_yr1 * ((1 + growth_rate) ** year)
            opex = opex_yr1 * ((1 + 0.18) ** year)
            revenues.append(rev)
            profits.append(rev - opex)

        fig_projection = go.Figure()
        fig_projection.add_trace(go.Bar(
            name='Revenue',
            x=years_labels,
            y=revenues,
            marker_color='#1f77b4'
        ))
        fig_projection.add_trace(go.Bar(
            name='Operating Profit',
            x=years_labels,
            y=profits,
            marker_color='#2ca02c'
        ))

        fig_projection.update_layout(
            barmode='group',
            height=400,
            yaxis_title="Amount (ETB)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig_projection, use_container_width=True)

        # Key assumptions reminder
        st.markdown("---")
        st.info("""
        **📋 Key Assumptions Used:**
        - Revenue growth: 25% annually (from enrollment growth and tuition increases)
        - Operating cost growth: 18% annually (Ethiopian inflation)
        - Discount rate: 15%
        - Tax & depreciation: ~30% of profit

        💡 **Remember:** These are projections based on your inputs. Actual results will vary!
        """)

    # TAB 6: DOWNLOAD REPORT
    with tab6:
        st.markdown("### 📥 Download Your Financial Model")

        st.markdown("""
        Generate a comprehensive Excel report with:
        - ✅ Executive Dashboard with KPIs
        - ✅ 10-year financial projections
        - ✅ Detailed revenue and expense breakdowns
        - ✅ Cash flow analysis
        - ✅ Interactive charts
        - ✅ Scenario comparisons
        """)

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 Quick Download")
            st.markdown("Use default assumptions from the backend model")

            if st.button("📥 Generate Standard Report", type="primary", use_container_width=True):
                with st.spinner("Generating Excel dashboard..."):
                    try:
                        dashboard = ExcelDashboard(scenario='Base_Case')
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f'School_Financial_Dashboard_{timestamp}.xlsx'
                        filepath = dashboard.export(filename)

                        # Provide download link
                        with open(filepath, 'rb') as f:
                            st.download_button(
                                label="⬇️ Download Excel Report",
                                data=f,
                                file_name=filename,
                                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                use_container_width=True
                            )

                        st.success("✅ Report generated successfully!")
                        st.info(f"📁 Also saved to: `output/{filename}`")

                    except Exception as e:
                        st.error(f"❌ Error generating report: {str(e)}")

        with col2:
            st.markdown("#### 🎯 Custom Report")
            st.markdown("Coming soon: Generate report with your custom inputs from the app")

            st.button("🔧 Generate Custom Report", disabled=True, use_container_width=True)
            st.caption("⏳ Feature under development")

        st.markdown("---")

        st.markdown("### 📧 Share with Stakeholders")

        st.markdown("""
        **Who should review this model?**
        - ✅ Investors & funding partners
        - ✅ Bank loan officers
        - ✅ School board members
        - ✅ Ministry of Education officials
        - ✅ Architecture & construction teams
        - ✅ Educational consultants
        """)

        st.markdown("---")

        st.markdown("### 📚 Additional Resources")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            **📖 Documentation**
            - README.md
            - QUICKSTART.md
            - Assumptions guide
            """)

        with col2:
            st.markdown("""
            **🔧 Customize**
            - Edit config/assumptions.py
            - Modify revenue models
            - Adjust cost structures
            """)

        with col3:
            st.markdown("""
            **📞 Support**
            - Review code on GitHub
            - Check documentation
            - Consult with experts
            """)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🎓 Ethiopian School Financial Model | Built with Python, Streamlit & ❤️</p>
        <p>⚠️ This model is for planning purposes only. Always consult with financial and legal professionals.</p>
        <p>© 2025 | <a href="https://github.com">View on GitHub</a></p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
