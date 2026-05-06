import streamlit as st
import pandas as pd
import math

# Updated Assets from User
PSPCL_LOGO_URL = "https://pspcl.in/assets/images/logo.png"
BEECLUE_LOGO_PNG = "https://raw.githubusercontent.com/iamanujnarang/LDHF/e5748e037b76a52a47d610a88c3a3c70f72f1c9a/BEECLUE.png"
INSTA_ICON = "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png"
FB_ICON = "https://upload.wikimedia.org/wikipedia/commons/1/1b/Facebook_icon.svg"
X_ICON = "https://upload.wikimedia.org/wikipedia/commons/5/53/X_logo_2023_original.svg"
LINKEDIN_ICON = "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png"

def main():
    st.set_page_config(page_title="PSPCL Load Calculator", layout="centered")

    # Custom CSS for Branding and Footer
    st.markdown(f"""
        <style>
        .footer-container {{ text-align: center; padding: 30px; margin-top: 50px; border-top: 1px solid #e2e8f0; }}
        .made-with-love {{ font-size: 1.1rem; margin-bottom: 15px; }}
        .heart-symbol {{ color: #e11d48; }}
        .social-icon {{ width: 25px; height: 25px; margin: 0 10px; transition: transform 0.2s; }}
        .social-icon:hover {{ transform: scale(1.2); }}
        .beeclue-img {{ width: 140px; margin-top: 10px; }}
        .powered-text {{ color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }}
        </style>
    """, unsafe_allow_html=True)

    # Header with PSPCL Logo
    col_logo, col_title = st.columns([1, 4])
    with col_logo:
        st.image(PSPCL_LOGO_URL, width=100)
    with col_title:
        st.title("PSPCL Connected Load Calculator")
        st.caption("Based on Annexure-1: Computation of Connected Load[cite: 1]")

    category = st.selectbox(
        "Select Supply Category",
        ["Domestic/Bulk Supply", "Other than Domestic/Bulk Supply (NRS/Industrial)"],
        index=0
    )

    st.divider()
    
    # Input Data - Defaulting to empty/zero
    col1, col2 = st.columns(2)
    inputs = {}

    with col1:
        st.subheader("💡 Lighting & Points")
        inputs['Fan Point'] = st.number_input("Fan Points", min_value=0, value=0)
        inputs['Light Point'] = st.number_input("Light Points", min_value=0, value=0)
        inputs['Wall Socket (60W)'] = st.number_input("Wall Sockets (60W)", min_value=0, value=0)
        inputs['Power Plug (1000W)'] = st.number_input("Power Plugs (1000W)", min_value=0, value=0)
        
    with col2:
        st.subheader("❄️ Standard Appliances")
        inputs['Air Conditioner (1.5 Ton)'] = st.number_input("AC Units", min_value=0, value=0)
        inputs['Geyser (1500W)'] = st.number_input("Geysers", min_value=0, value=0)
        inputs['Refrigerator (250W)'] = st.number_input("Refrigerators", min_value=0, value=0)
        inputs['Dessert Cooler (250W)'] = st.number_input("Coolers", min_value=0, value=0)
        inputs['Washing Machine (500W)'] = st.number_input("Washing Machines", min_value=0, value=0)

    # Special Equipment in Expander
    with st.expander("⚙️ Special Equipment (Motive Load, UPS, Welding)"):
        inputs['Water Pump / Motive Load (Watts)'] = st.number_input("Actual Watts", min_value=0, value=0)
        inputs['3-Phase Socket (6kW)'] = st.number_input("3-Phase Sockets Qty", min_value=0, value=0)
        inputs['UPS Rating (kVA)'] = st.number_input("UPS kVA", min_value=0.0, value=0.0)
        inputs['Welding Set (kVA)'] = st.number_input("Welding kVA", min_value=0.0, value=0.0)

    # Logic Implementation for Summary Table[cite: 1]
    table_data = []
    total_kw = 0.0

    # 1. Fans (Domestic: 1/3 counted | Other: All counted)[cite: 1]
    f_qty = inputs['Fan Point']
    f_val = (math.ceil(f_qty / 3) * 60 / 1000) if category == "Domestic/Bulk Supply" else (f_qty * 60 / 1000)
    if f_qty > 0: table_data.append(["Fan Point", f_qty, f"{f_val:.3f} kW"])
    total_kw += f_val

    # 2. Lights (Domestic: 1/2 counted | Other: All counted)[cite: 1]
    l_qty = inputs['Light Point']
    l_val = (math.ceil(l_qty / 2) * 40 / 1000) if category == "Domestic/Bulk Supply" else (l_qty * 40 / 1000)
    if l_qty > 0: table_data.append(["Light Point", l_qty, f"{l_val:.3f} kW"])
    total_kw += l_val

    # 3. Sockets (Domestic: 1/4 | Other: 1/3 for 60W)[cite: 1]
    w_qty = inputs['Wall Socket (60W)']
    w_div = 4 if category == "Domestic/Bulk Supply" else 3
    w_val = (math.ceil(w_qty / w_div) * 60 / 1000)
    if w_qty > 0: table_data.append(["Wall Socket (60W)", w_qty, f"{w_val:.3f} kW"])
    total_kw += w_val

    # 4. Power Plugs (Domestic: 1/2 | Other: 1/4)[cite: 1]
    p_qty = inputs['Power Plug (1000W)']
    p_div = 2 if category == "Domestic/Bulk Supply" else 4
    p_val = (math.ceil(p_qty / p_div) * 1000 / 1000)
    if p_qty > 0: table_data.append(["Power Plug (1000W)", p_qty, f"{p_val:.3f} kW"])
    total_kw += p_val

    # 5. Heavy Appliances (100% rating)[cite: 1]
    heavy_items = [
        ('Air Conditioner (1.5 Ton)', 2500), ('Geyser (1500W)', 1500), 
        ('Refrigerator (250W)', 250), ('Dessert Cooler (250W)', 250), 
        ('Washing Machine (500W)', 500)
    ]
    for name, watt in heavy_items:
        qty = inputs[name]
        val = (qty * watt / 1000)
        if qty > 0:
            table_data.append([name, qty, f"{val:.3f} kW"])
            total_kw += val

    # 6. Special Factors[cite: 1]
    motive = inputs['Water Pump / Motive Load (Watts)'] / 1000
    if motive > 0:
        table_data.append(["Motive Load/Pump", "Actual", f"{motive:.3f} kW"])
        total_kw += motive

    ups = inputs['UPS Rating (kVA)'] * 0.90
    if ups > 0:
        table_data.append(["UPS (0.90 PF)", f"{inputs['UPS Rating (kVA)']} kVA", f"{ups:.3f} kW"])
        total_kw += ups

    weld = inputs['Welding Set (kVA)'] * 0.40
    if weld > 0:
        table_data.append(["Welding Set (0.40 PF)", f"{inputs['Welding Set (kVA)']} kVA", f"{weld:.3f} kW"])
        total_kw += weld

    tp_qty = inputs['3-Phase Socket (6kW)']
    tp_val = math.ceil(tp_qty / 2) * 6.0
    if tp_qty > 0:
        table_data.append(["3-Phase Sockets (6kW)", tp_qty, f"{tp_val:.3f} kW"])
        total_kw += tp_val

    # Results Section
    st.divider()
    if table_data:
        st.subheader("📋 Load Computation Table")
        df = pd.DataFrame(table_data, columns=["Description", "Quantity/Rating", "Computed Load"])
        st.table(df)
        st.success(f"### Total Connected Load: {total_kw:.3f} kW")
    else:
        st.info("Please enter quantities above to calculate the load.")

    # Footer[cite: 1]
    footer_html = f"""
    <div class="footer-container">
        <div class="made-with-love">Made with <span class="heart-symbol">❤️</span> by <b>Er. Anuj Narang, JE PSPCL</b></div>
        <div style="margin-bottom: 25px;">
            <a href="https://instagram.com/iamanujnarang" target="_blank"><img src="{INSTA_ICON}" class="social-icon"></a>
            <a href="https://facebook.com/iamanujnarang" target="_blank"><img src="{FB_ICON}" class="social-icon"></a>
            <a href="https://x.com/iamanujnarang" target="_blank"><img src="{X_ICON}" class="social-icon"></a>
            <a href="https://linkedin.com/in/iamanujnarang" target="_blank"><img src="{LINKEDIN_ICON}" class="social-icon"></a>
        </div>
        <div style="margin-top: 25px;">
            <div class="powered-text">In Strategic Collaboration with</div>
            <a href="https://beeclue.com" target="_blank">
                <img src="{BEECLUE_LOGO_PNG}" class="beeclue-img">
            </a>
        </div>
        <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 25px;">© 2026 | Supply Code 2024 Guidelines</div>
    </div>"""
    
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
