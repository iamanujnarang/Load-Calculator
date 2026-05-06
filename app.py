import streamlit as st
import math

def main():
    st.set_page_config(page_title="PSPCL Load Calculator", layout="wide")
    
    st.title("⚡ PSPCL Connected Load Calculator")
    st.write("Computation as per **Annexure-1** of PSPCL regulations.")

    # Category Selection
    category = st.selectbox(
        "Select Supply Category",
        ["Domestic/Bulk Supply", "Other (NRS/Industrial/General)"]
    )

    st.divider()
    
    # Input Data Containers
    col1, col2 = st.columns(2)
    load_data = {}

    with col1:
        st.subheader("Lighting & Small Sockets")
        load_data['fan'] = st.number_input("Fan Points", min_value=0, step=1)
        load_data['light'] = st.number_input("Light Points", min_value=0, step=1)
        load_data['wall_socket'] = st.number_input("Wall Sockets (60W)", min_value=0, step=1)
        load_data['power_plug'] = st.number_input("Power Plugs (1000W)", min_value=0, step=1)
        
    with col2:
        st.subheader("Heavy Appliances")
        load_data['ac_1_5'] = st.number_input("AC (1.5 Ton/2500W)", min_value=0, step=1)
        load_data['geyser'] = st.number_input("Geyser (1500W)", min_value=0, step=1)
        load_data['fridge'] = st.number_input("Refrigerator (250W)", min_value=0, step=1)
        load_data['cooler'] = st.number_input("Dessert Cooler (250W)", min_value=0, step=1)
        load_data['washing'] = st.number_input("Washing Machine (500W)", min_value=0, step=1)

    st.subheader("Special Equipment & Conversions")
    c3, c4 = st.columns(2)
    with c3:
        motive_load = st.number_input("Other Motive Load / Water Pump (Actual Watts)", min_value=0.0, step=10.0)
        ups_kva = st.number_input("UPS Rating (kVA)", min_value=0.0, step=0.1)
    with c4:
        three_phase_sockets = st.number_input("3-Phase Sockets (NRS/Ind/AP) - Qty", min_value=0, step=1)
        welding_kva = st.number_input("Welding Set (kVA)", min_value=0.0, step=0.1)

    # Calculation Logic
    total_kw = 0.0

    # 1. Fans & Lights
    if category == "Domestic/Bulk Supply":
        total_kw += math.ceil(load_data['fan'] / 3) * 60 / 1000  # 1/3 counted
        total_kw += math.ceil(load_data['light'] / 2) * 40 / 1000 # 1/2 counted
        total_kw += math.ceil(load_data['wall_socket'] / 4) * 60 / 1000 # 1/4 counted
        total_kw += math.ceil(load_data['power_plug'] / 2) * 1000 / 1000 # 1/2 counted
    else:
        total_kw += (load_data['fan'] * 60) / 1000 # All counted
        total_kw += (load_data['light'] * 40) / 1000 # All counted
        total_kw += math.ceil(load_data['wall_socket'] / 3) * 60 / 1000 # 1/3 counted
        total_kw += math.ceil(load_data['power_plug'] / 4) * 1000 / 1000 # 1/4 counted

    # 2. Appliances (All counted unless specified)
    total_kw += (load_data['ac_1_5'] * 2500) / 1000
    total_kw += (load_data['geyser'] * 1500) / 1000
    total_kw += (load_data['fridge'] * 250) / 1000
    total_kw += (load_data['cooler'] * 250) / 1000
    total_kw += (load_data['washing'] * 500) / 1000
    total_kw += motive_load / 1000

    # 3. 3-Phase Sockets (6kW each, 1/2 counted)
    total_kw += math.ceil(three_phase_sockets / 2) * 6.0

    # 4. UPS & Welding Conversions
    total_kw += (ups_kva * 0.90)  # UPS PF = 0.90
    total_kw += (welding_kva * 0.40) # Welding PF = 0.40

    # Display Result
    st.divider()
    st.header(f"Calculated Connected Load: {total_kw:.2f} kW")
    
    if total_kw > 7:
        st.info("💡 Note: Loads above 7kW generally require a 3-phase connection.")
    
    with st.expander("View Calculation Rules"):
        st.write("""
        * **Diversity Factors:** Applied to Fans (1/3), Lights (1/2), and Sockets as per Annexure-1.
        * **Fractions:** Any fraction of lamp/fan/socket is counted as one.
        * **UPS:** kVA converted to kW using 0.90 PF[cite: 1].
        * **Welding:** kVA converted to kW using 0.40 PF[cite: 1].
        """)

if __name__ == "__main__":
    main()
