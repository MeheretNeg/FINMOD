"""
CAPEX Model - Capital Expenditure calculations
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from config import assumptions as asmp
from src import utils


class CAPEXModel:
    """Calculate all capital expenditures"""

    def __init__(self, scenario: str = 'Base_Case'):
        """
        Initialize CAPEX model

        Args:
            scenario: Scenario name from assumptions
        """
        self.scenario = scenario
        self.scenario_capex_factor = asmp.SCENARIOS[scenario].get('capex_factor', 1.0)

    def calculate_construction_costs(self) -> float:
        """
        Calculate total building construction costs

        Returns:
            Total construction cost
        """
        total_area = asmp.TOTAL_BUILDING_AREA
        cost_per_sqm = asmp.CONSTRUCTION_COST_PER_SQM

        construction_cost = total_area * cost_per_sqm * self.scenario_capex_factor

        return construction_cost

    def calculate_outdoor_facilities(self) -> float:
        """
        Calculate outdoor facilities costs

        Returns:
            Total outdoor facilities cost
        """
        total_cost = sum(asmp.OUTDOOR_FACILITIES.values()) * self.scenario_capex_factor
        return total_cost

    def calculate_furniture_costs(self) -> float:
        """
        Calculate all furniture and equipment costs

        Returns:
            Total furniture cost
        """
        total_cost = 0

        # Classroom furniture (per number of classrooms)
        num_classrooms = 30  # From assumptions (K-12 full capacity)
        total_cost += asmp.FURNITURE_COSTS['Classroom_Furniture'] * num_classrooms

        # Office furniture
        total_cost += asmp.FURNITURE_COSTS['Office_Furniture']

        # Library furniture
        total_cost += asmp.FURNITURE_COSTS['Library_Furniture']

        # Lab equipment (6 labs: 4 science + 2 computer)
        num_labs = 6
        total_cost += asmp.FURNITURE_COSTS['Lab_Equipment'] * num_labs

        # Cafeteria equipment
        total_cost += asmp.FURNITURE_COSTS['Cafeteria_Equipment']

        # Sports equipment
        total_cost += asmp.FURNITURE_COSTS['Sports_Equipment']

        return total_cost * self.scenario_capex_factor

    def calculate_technology_costs(self) -> float:
        """
        Calculate technology infrastructure costs

        Returns:
            Total technology cost
        """
        total_cost = 0

        # Computer labs
        total_cost += asmp.TECHNOLOGY_COSTS['Computer_Labs']

        # Classroom technology (per classroom)
        num_classrooms = 30
        total_cost += asmp.TECHNOLOGY_COSTS['Classroom_Tech'] * num_classrooms

        # Network infrastructure
        total_cost += asmp.TECHNOLOGY_COSTS['Network_Infrastructure']

        # Security systems
        total_cost += asmp.TECHNOLOGY_COSTS['Security_Systems']

        # Admin software
        total_cost += asmp.TECHNOLOGY_COSTS['Admin_Software']

        return total_cost * self.scenario_capex_factor

    def calculate_initial_setup_costs(self) -> float:
        """
        Calculate initial setup and pre-launch costs

        Returns:
            Total setup costs
        """
        total_cost = sum(asmp.INITIAL_SETUP_COSTS.values()) * self.scenario_capex_factor
        return total_cost

    def calculate_total_capex(self) -> Dict[str, float]:
        """
        Calculate all CAPEX items

        Returns:
            Dictionary with CAPEX categories and amounts
        """
        capex = {
            'Land': asmp.LAND_COST,  # Already owned
            'Construction': self.calculate_construction_costs(),
            'Outdoor_Facilities': self.calculate_outdoor_facilities(),
            'Furniture_Equipment': self.calculate_furniture_costs(),
            'Technology': self.calculate_technology_costs(),
            'Initial_Setup': self.calculate_initial_setup_costs(),
        }

        capex['Total'] = sum(capex.values())

        return capex

    def get_capex_breakdown(self) -> pd.DataFrame:
        """
        Get CAPEX breakdown as DataFrame

        Returns:
            DataFrame with CAPEX categories
        """
        capex = self.calculate_total_capex()

        df = pd.DataFrame(list(capex.items()), columns=['Category', 'Amount_ETB'])

        # Add percentage of total
        total = capex['Total']
        df['Percentage'] = (df['Amount_ETB'] / total * 100).round(2)

        return df

    def get_detailed_breakdown(self) -> Dict[str, pd.DataFrame]:
        """
        Get detailed breakdown of each CAPEX category

        Returns:
            Dictionary of DataFrames for each category
        """
        breakdowns = {}

        # Construction breakdown
        construction_data = []
        for space, area in asmp.BUILDING_AREA.items():
            cost = area * asmp.CONSTRUCTION_COST_PER_SQM * self.scenario_capex_factor
            construction_data.append({
                'Space': space,
                'Area_SQM': area,
                'Cost_per_SQM': asmp.CONSTRUCTION_COST_PER_SQM * self.scenario_capex_factor,
                'Total_Cost': cost
            })
        breakdowns['Construction'] = pd.DataFrame(construction_data)

        # Outdoor facilities breakdown
        outdoor_data = []
        for facility, cost in asmp.OUTDOOR_FACILITIES.items():
            outdoor_data.append({
                'Facility': facility,
                'Cost': cost * self.scenario_capex_factor
            })
        breakdowns['Outdoor_Facilities'] = pd.DataFrame(outdoor_data)

        # Furniture breakdown
        furniture_data = []
        num_classrooms = 30
        num_labs = 6

        furniture_items = {
            'Classroom_Furniture': ('Classroom Furniture', num_classrooms),
            'Office_Furniture': ('Office Furniture', 1),
            'Library_Furniture': ('Library Furniture', 1),
            'Lab_Equipment': ('Lab Equipment', num_labs),
            'Cafeteria_Equipment': ('Cafeteria Equipment', 1),
            'Sports_Equipment': ('Sports Equipment', 1),
        }

        for key, (name, qty) in furniture_items.items():
            unit_cost = asmp.FURNITURE_COSTS[key] * self.scenario_capex_factor
            furniture_data.append({
                'Item': name,
                'Quantity': qty,
                'Unit_Cost': unit_cost,
                'Total_Cost': unit_cost * qty
            })
        breakdowns['Furniture_Equipment'] = pd.DataFrame(furniture_data)

        # Technology breakdown
        tech_data = []
        tech_items = {
            'Computer_Labs': ('Computer Labs', 1),
            'Classroom_Tech': ('Classroom Technology', num_classrooms),
            'Network_Infrastructure': ('Network Infrastructure', 1),
            'Security_Systems': ('Security Systems', 1),
            'Admin_Software': ('Admin Software', 1),
        }

        for key, (name, qty) in tech_items.items():
            unit_cost = asmp.TECHNOLOGY_COSTS[key] * self.scenario_capex_factor
            tech_data.append({
                'Item': name,
                'Quantity': qty,
                'Unit_Cost': unit_cost,
                'Total_Cost': unit_cost * qty
            })
        breakdowns['Technology'] = pd.DataFrame(tech_data)

        # Setup costs breakdown
        setup_data = []
        for item, cost in asmp.INITIAL_SETUP_COSTS.items():
            setup_data.append({
                'Item': item,
                'Cost': cost * self.scenario_capex_factor
            })
        breakdowns['Initial_Setup'] = pd.DataFrame(setup_data)

        return breakdowns


if __name__ == '__main__':
    # Test the CAPEX model
    print("=" * 80)
    print("CAPEX MODEL TEST - BASE CASE")
    print("=" * 80)

    model = CAPEXModel(scenario='Base_Case')

    # Summary
    df_summary = model.get_capex_breakdown()
    print("\nCAPEX Summary:")
    print(df_summary.to_string(index=False))

    # Detailed breakdowns
    breakdowns = model.get_detailed_breakdown()

    print("\n" + "=" * 80)
    print("DETAILED BREAKDOWNS")
    print("=" * 80)

    for category, df in breakdowns.items():
        print(f"\n{category}:")
        print(df.to_string(index=False))

    total_capex = model.calculate_total_capex()['Total']
    print(f"\n{'=' * 80}")
    print(f"TOTAL CAPEX REQUIRED: {utils.format_currency(total_capex)}")
    print(f"{'=' * 80}")
