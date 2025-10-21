# Ethiopian International Christian School - Financial Feasibility Model

## 🎓 Two Ways to Use This Model

### 1. 🌐 **Interactive Web App** (Recommended for Non-Technical Users)
**User-friendly web application - No finance or coding knowledge required!**

```bash
# Launch the web app
./launch_app.sh

# Or manually:
streamlit run app.py
```

**Features:**
- ✅ Simple, intuitive interface
- ✅ Real-time calculations as you adjust inputs
- ✅ Interactive charts and visualizations
- ✅ Research-based defaults from international standards
- ✅ Built-in validation and warnings
- ✅ Download Excel reports with one click
- ✅ Perfect for stakeholder presentations

**📖 Read APP_GUIDE.md for detailed instructions**

### 2. 💻 **Python Scripts** (For Technical Users)
**Full control over all parameters and calculations**

```bash
# Generate Excel dashboard
python main.py
```

**Features:**
- ✅ Customizable Python code
- ✅ Edit config/assumptions.py for detailed control
- ✅ Run individual models for testing
- ✅ Advanced scenario analysis
- ✅ Professional Excel output with charts

---

## Project Overview
Comprehensive financial feasibility study for an international Christian school in Addis Ababa, Ethiopia.

**Based on Research & International Standards:**
- International Baccalaureate (IB) guidelines
- Cambridge International standards
- Ethiopian Ministry of Education regulations
- Addis Ababa market research (2024)
- World Bank education statistics

### School Profile
- **Location**: Addis Ababa, Ethiopia
- **Curriculum**: International curriculum with Christian foundation
- **Grade Levels**: K-9 (initial), expanding to K-12
- **Launch Date**: September 2026
- **Land**: Already secured (no acquisition cost)

## Model Structure

### 1. Assumptions (`config/assumptions.py`)
- Enrollment projections and capacity
- Tuition fee structure
- Revenue assumptions (ancillary services)
- Cost assumptions (salaries, operations)
- Timeline and growth rates

### 2. Revenue Model (`src/revenue_model.py`)
- Tuition revenue by grade
- Registration and enrollment fees
- Ancillary services (transport, meals, uniforms)
- Other revenue streams

### 3. Capital Expenditure (`src/capex_model.py`)
- Building construction costs
- Furniture and equipment
- Technology infrastructure
- Initial setup costs

### 4. Operating Expenditure (`src/opex_model.py`)
- Staff salaries and benefits
- Utilities and maintenance
- Learning materials and supplies
- Administrative costs
- Marketing and recruitment

### 5. Financial Statements (`src/financial_statements.py`)
- Profit & Loss Statement
- Cash Flow Statement
- Balance Sheet

### 6. Analysis & Metrics (`src/analysis.py`)
- NPV (Net Present Value)
- IRR (Internal Rate of Return)
- Payback Period
- Break-even Analysis
- Sensitivity Analysis

## Getting Started

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Model
```bash
python main.py
```

### Output
Results are generated in the `output/` directory:
- Excel workbook with all financial statements
- PDF summary report
- Scenario comparison charts

## Directory Structure
```
FINMOD/
├── config/
│   └── assumptions.py          # All assumptions and parameters
├── src/
│   ├── revenue_model.py        # Revenue projections
│   ├── capex_model.py          # Capital expenditure
│   ├── opex_model.py           # Operating expenditure
│   ├── financial_statements.py # Financial statements
│   ├── analysis.py             # Financial metrics
│   └── utils.py                # Utility functions
├── output/                     # Generated reports
├── data/                       # Reference data (if any)
├── main.py                     # Main execution script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Key Assumptions (Customizable)

### Ethiopian Context
- Currency: Ethiopian Birr (ETB)
- Academic Calendar: September - June
- Student-Teacher Ratio: 15:1 (international standard)
- Exchange Rate: ~55 ETB/USD (as of 2024)

### School Benchmarks (International Schools in Ethiopia)
- Tuition Range: 50,000 - 200,000 ETB/year depending on grade
- Enrollment Growth: 20-30% annually in early years
- Operating Margin Target: 15-25% at maturity

## Next Steps
1. Review and customize assumptions in `config/assumptions.py`
2. Run the model: `python main.py`
3. Analyze outputs in `output/` directory
4. Adjust scenarios and re-run for sensitivity analysis

## Notes
- All financial projections are in Ethiopian Birr (ETB)
- Model includes 10-year projection period
- Inflation and currency considerations included
- Based on international school best practices
