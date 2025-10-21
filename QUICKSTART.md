# Quick Start Guide

## Ethiopian International Christian School - Financial Model

### Overview
This financial model provides a comprehensive 10-year feasibility analysis for launching an international Christian school in Addis Ababa, Ethiopia.

### Initial Results Summary

Based on the default assumptions, here are the key findings:

#### 💰 Investment Required
- **Total CAPEX**: ETB 128.4 million (~$2.3 million USD)
- **Equity (40%)**: ETB 51.4 million
- **Debt (60%)**: ETB 77.0 million

#### 📊 Financial Viability
- **NPV (15% discount)**: ETB 46.9 million ✅ POSITIVE
- **IRR**: 45.0% ✅ Well above 15% target
- **Payback Period**: 4.8 years
- **Break-Even**: Year 2030 (4 years after launch)

#### 📈 Revenue Projections
- **Year 1**: ETB 29.1 million (176 students)
- **Year 10**: ETB 334.4 million (560 students at full capacity)
- **10-Year Total**: ETB 1.66 billion
- **Revenue Growth**: 31.2% CAGR

#### 💵 Profitability
- **Average Operating Margin**: 15.2%
- **Average Net Margin**: 2.5%
- **Year 10 Net Income**: ETB 31.9 million

### Decision: ✅ FINANCIALLY VIABLE

The project shows **strong investment potential** with:
- Positive NPV of ETB 46.9 million
- IRR of 45% (significantly exceeds 15% target)
- Break-even achieved in 4 years
- Healthy operating margins at maturity

---

## How to Use This Model

### 1. Review the Excel Output

The model generates a comprehensive Excel workbook with multiple sheets:

- **Executive_Summary**: Key metrics at a glance
- **Revenue_Projections**: Detailed revenue by source
- **CAPEX_Summary**: Capital expenditure breakdown
- **OPEX_Projections**: Operating expenses by category
- **Profit_Loss**: 10-year P&L statement
- **Cash_Flow**: Cash flow statement
- **Balance_Sheet**: Projected balance sheets
- **Scenario_Comparison**: Base, Optimistic, Conservative, Worst Case
- **Sensitivity_XXX**: Sensitivity analysis for key variables
- **CAPEX_XXX**: Detailed CAPEX breakdowns

### 2. Customize Assumptions

Edit `config/assumptions.py` to adjust:

#### Enrollment & Capacity
```python
STUDENTS_PER_CLASS = 20  # Class size
SECTIONS_PER_GRADE = {...}  # Classes per grade
ENROLLMENT_RAMP = {...}  # Growth trajectory
```

#### Tuition & Fees
```python
ANNUAL_TUITION = {
    'KG1': 80000,
    'Grade1': 95000,
    ...
}
```

#### Costs
```python
CONSTRUCTION_COST_PER_SQM = 15000
STAFF_STRUCTURE = {...}
UTILITIES_MONTHLY = {...}
```

#### Economic Assumptions
```python
ANNUAL_INFLATION_RATE = 0.20  # 20%
TUITION_INCREASE_RATE = 0.15  # 15%
DISCOUNT_RATE = 0.15  # 15%
```

### 3. Re-run the Model

```bash
python main.py
```

A new Excel file will be generated in the `output/` directory with updated projections.

### 4. Test Individual Components

You can also test individual modules:

```bash
# Test revenue model
python src/revenue_model.py

# Test CAPEX model
python src/capex_model.py

# Test OPEX model
python src/opex_model.py

# Test financial statements
python src/financial_statements.py

# Test analysis
python src/analysis.py
```

---

## Key Assumptions to Validate

Before finalizing your feasibility study, validate these key assumptions with local market research:

### 1. **Tuition Levels**
- Current model: KG: 80k, Grades 1-5: 95-105k, Grades 6-9: 115-120k ETB
- **Action**: Compare with other international schools in Addis Ababa
- Schools to research: International Community School, Sandford International, etc.

### 2. **Construction Costs**
- Current model: 15,000 ETB/sqm
- **Action**: Get quotes from local contractors
- Consider: Building quality, location, current material costs

### 3. **Enrollment Projections**
- Current model: 40% capacity in Year 1, 100% by Year 9
- **Action**: Research demand, conduct parent surveys
- Consider: Competition, target market size, location accessibility

### 4. **Staff Salaries**
- Current model: Teachers at 30k ETB/month, Principal at 80k ETB/month
- **Action**: Research competitive salaries for international school staff
- Consider: Expatriate vs. local staff mix, experience levels

### 5. **Operating Costs**
- Current model: Various assumptions for utilities, maintenance, etc.
- **Action**: Get quotes from service providers
- Consider: Ethiopian inflation trends, currency fluctuations

---

## Scenarios Included

The model includes 4 pre-built scenarios:

1. **Base Case**: Expected scenario with stated assumptions
2. **Optimistic**: 15% higher enrollment, 10% higher tuition, 5% lower costs
3. **Conservative**: 20% lower enrollment, 10% lower tuition, 15% higher costs
4. **Worst Case**: 35% lower enrollment, 15% lower tuition, 25% higher costs

All scenarios are compared in the Excel output.

---

## Next Steps

### Immediate Actions:
1. ✅ Review the Excel output with stakeholders
2. 📋 Validate key assumptions with local market research
3. 💰 Secure commitments for equity funding (ETB 51.4M)
4. 🏦 Approach banks for debt financing (ETB 77.0M)
5. 📍 Finalize land location and begin design

### Before Construction:
1. Conduct detailed market research
2. Develop curriculum and hire academic leadership
3. Obtain all necessary licenses and permits
4. Create detailed architectural plans
5. Finalize contractor selection

### Before Launch:
1. Complete construction and setup
2. Recruit and train staff
3. Execute marketing and enrollment campaign
4. Set up administrative systems
5. Conduct soft opening and testing

---

## Support & Customization

To customize the model further:
- Edit `config/assumptions.py` for all parameters
- Modify individual models in `src/` for custom logic
- Adjust scenarios in `config/assumptions.py` under `SCENARIOS`
- Add new revenue streams or cost categories as needed

---

## Questions?

Common questions:

**Q: Can I change the currency?**
A: Yes, edit `CURRENCY` and `USD_TO_ETB_RATE` in assumptions.py

**Q: Can I model a different school size?**
A: Yes, edit `SECTIONS_PER_GRADE` and `STUDENTS_PER_CLASS`

**Q: Can I add more years?**
A: Yes, edit `PROJECTION_YEARS` in assumptions.py

**Q: How do I model different enrollment scenarios?**
A: Edit `ENROLLMENT_RAMP` dictionary or create new scenarios

**Q: Can I change the grade levels?**
A: Yes, edit `GRADE_LEVELS` and related dictionaries

---

## Important Notes

⚠️ **Risk Factors to Consider:**
- Currency fluctuation (ETB/USD exchange rate)
- High inflation in Ethiopia (20%+)
- Political and economic stability
- Competition from existing schools
- Regulatory changes
- Enrollment uncertainties

⚠️ **This model is for planning purposes only.** Always:
- Conduct thorough market research
- Consult with local experts
- Validate all assumptions
- Seek professional financial and legal advice
- Consider local context and risks

---

**Good luck with your school project! 🎓**
