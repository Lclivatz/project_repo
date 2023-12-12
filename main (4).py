import streamlit as st


class Footprint:
    def __init__(self):
        self.sectors = {}
        self.benchmark = {}
        self.value = {}

    def emission_sector(self, sector, use_cases):
        self.sectors[sector] = {use_case: 0 for use_case in use_cases}
        self.benchmark[sector] = {use_case: 0 for use_case in use_cases}
        self.value[sector] = {use_case: 0 for use_case in use_cases}

    def input_value(self, sector, use_case):
        if sector in self.sectors and use_case in self.sectors[sector]:
            value = st.number_input(" ", value=None, placeholder=f"Enter Value for {use_case} in tCO2eq")
            if value is not None:
                st.session_state.setdefault(sector, {})[use_case] = value
                self.value[sector][use_case] = value

    def emission_benchmark(self, sector, use_case, value):
        if sector in self.benchmark and use_case in self.sectors[sector]:
            self.benchmark[sector][use_case] = value

    def display_values(self, sector):
        if sector in self.sectors:
            st.write(f"Values for {sector}:")
            total = 0
            for use_case, value in st.session_state.get(sector, {}).items():
                benchmark = self.benchmark[sector][use_case]
                st.write(f"{use_case}: {value} (Standard Emissions: {benchmark})")

                if value > benchmark:
                    st.warning(f"  - Excess Emissions compared to Standard of {value - benchmark} tCO2eq")
                elif value < benchmark:
                    st.success(f"  - Below Standard Emissions by {benchmark - value} tCO2eq")

                total += value
            st.write(f"Total: {total}")

def initialize_sectors(footprint_manager):
    sectors_data = {
        "Energy": ["Electricity", "Fuel Combustion", "Thermal Energy"],
        "Production and Manufacturing": ["Production Processes"],
        "Transportation and Storage": ["Logistics"],
        "Water Supply and Waste Management": ["Water Treatment"],
        "Wholesale and Retail Trade": ["Distribution Centers"],
        "Agriculture": ["Livestock", "Farming"],
    }

    for sector, use_cases in sectors_data.items():
        footprint_manager.emission_sector(sector, use_cases)

    footprint_manager.emission_benchmark("Energy", "Electricity", 1000)
    footprint_manager.emission_benchmark("Energy", "Fuel Combustion", 500)
    footprint_manager.emission_benchmark("Production and Manufacturing", "Production Processes", 200)
    footprint_manager.emission_benchmark("Transportation and Storage", "Logistics", 300)
    footprint_manager.emission_benchmark("Water Supply and Waste Management", "Water Treatment", 150)
    footprint_manager.emission_benchmark("Wholesale and Retail Trade", "Distribution Centers", 100)
    footprint_manager.emission_benchmark("Agriculture", "Livestock", 50)
    footprint_manager.emission_benchmark("Agriculture", "Farming", 80)


def main_menu(footprint_manager):
    st.title("Carbon Footprint Tracker")
    options = ["Add/Update Values", "Display Emissions", "Exit"]

    choice = st.sidebar.selectbox("Select Option", options)

    if choice == "Add/Update Values":
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()))
        st.session_state.selected_sector = sector
        for use_case in footprint_manager.sectors.get(sector, {}):
            footprint_manager.input_value(sector, use_case)

    elif choice == "Display Emissions":
        sector = st.selectbox("Choose Sector", list(footprint_manager.sectors.keys()))
        footprint_manager.display_values(sector)
        st.caption("Benchmark Source: ")

    elif choice == "Exit":
        st.text("Thank you for using our Carbon Footprint Tracker")


if __name__ == "__main__":
    footprint_manager = Footprint()
    initialize_sectors(footprint_manager)
    main_menu(footprint_manager)