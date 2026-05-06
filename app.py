import streamlit as st
import pandas as pd
import math
from io import BytesIO

# Assets
PSPCL_LOGO_URL = "https://pspcl.in/assets/images/logo.png"
BEECLUE_LOGO_PNG = "https://raw.githubusercontent.com/iamanujnarang/LDHF/e5748e037b76a52a47d610a88c3a3c70f72f1c9a/BEECLUE.png"
INSTA_ICON = "https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png"
FB_ICON = "https://upload.wikimedia.org/wikipedia/commons/1/1b/Facebook_icon.svg"
X_ICON = "https://upload.wikimedia.org/wikipedia/commons/5/53/X_logo_2023_original.svg"
LINKEDIN_ICON = "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png"

def main():
    st.set_page_config(page_title="PSPCL Load Calculator Pro", layout="wide")

    # Advanced CSS for modern UI
    st.markdown(f"""
        <style>
        .centered-logo {{ display: flex; justify-content: center; margin-bottom: 10px; }}
        .header-text {{ text-align: center; margin-bottom: 30px; }}
        .stNumberInput div div input {{ font-weight: bold; }}
        .footer-container {{ text-align: center; padding: 40px; margin-top: 60px; border-top: 1px solid #e2e8f0; background-color: #f8fafc; }}
        .social-icon {{ width: 28px; height: 28px; margin: 0 12px; transition: 0.3s; }}
        .social-icon:hover {{ transform: translateY(-3px); }}
        .beeclue-img {{ width: 150px; margin-top: 15px; filter: grayscale(20%); }}
        .metric-card {{ background: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); border: 1px solid #f1f5f9; }}
        </style>
    """, unsafe_allow_html=True)

    # Top Header
    st.markdown(f'<div class="centered-logo"><img src="{PSPCL_LOGO_URL}" width="130"></div>', unsafe_allow_html=True)
    st.markdown('<div class="header-text"><h1>PSPCL Connected Load Calculator</h1><p>Official Guidelines: Supply Code 2024 (Annexure-1)</p></div>', unsafe_allow_html=True)

    # Category Selection
    category = st.selectbox(
        "Select Connection Category",
        ["Domestic/Bulk Supply", "Other than Domestic/Bulk Supply (NRS/Industrial)"],
        help="Diversity factors change based on this selection."
    )

    st.divider()
    
    # ---------------------------
    # Main Input Section
    # ---------------------------
    inputs = {}
    
    # Quick Access Header (Motor, Fan, Light)
    st.subheader("🚀 Quick Entry (High Frequency Items)")
    qc1, qc2, qc3 = st.columns(3)
    
    with qc1:
        st.markdown("🌀 **Ceiling Fan (60W)**")
        inputs['Fan Point'] = st.number_input("Qty", min_value=0, value=0, key="fan_q", label_visibility="collapsed")
    with qc2:
        st.markdown("💡 **Light Point (40W)**")
        inputs['Light Point'] = st.number_input("Qty", min_value=0, value=0, key="light_q", label_visibility="collapsed")
    with qc3:
        st.markdown("🚜 **Water Pump (Motor)**")
        bhp = st.number_input("Rating in BHP", min_value=0.0, step=0.5, value=0.0, help="1 BHP ≈ 0.746 kW")
        inputs['Motor BHP'] = bhp

    st.write("") # Spacer

    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown("### 🔌 Sockets & Plugs")
            inputs['Wall Socket (60W)'] = st.number_input("Wall Sockets (60W)", min_value=0, value=0)
            inputs['Power Plug (1000W)'] = st.number_input("Power Plugs (1000W)", min_value=0, value=0)
            
    with col2:
        with st.container():
            st.markdown("### ❄️ Appliances")
            inputs['Air Conditioner (2500W)'] = st.number_input("AC 1.5 Ton (2500W)", min_value=0, value=0)
            inputs['Geyser (1500W)'] = st.number_input("Geyser (1500W)", min_value=0, value=0)
            inputs['Refrigerator (250W)'] = st.number_input("Refrigerator (250W)", min_value=0, value=0)
            inputs['Dessert Cooler (250W)'] = st.number_input("Cooler (250W)", min_value=0, value=0)
            inputs['Washing Machine (500W)'] = st.number_input("Washing Machine (500W)", min_value=0, value=0)

    # Secondary Items
    with st.expander("⚙️ Advanced Equipment (UPS, Welding, 3-Phase)"):
        inputs['3-Phase Socket (6kW)'] = st.number_input("3-Phase Sockets (6000W)", min_value=0, value=0)
        inputs['UPS Rating (kVA)'] = st.number_input("UPS (kVA)", min_value=0.0, value=0.0)
        inputs['Welding Set (kVA)'] = st.number_input("Welding (kVA)", min_value=0.0, value=0.0)

    # ---------------------------
    # Calculation Engine[cite: 1]
    # ---------------------------
    table_data = []
    total_kw = 0.0

    # 1. Fans (DS: 1/3 counted)[cite: 1]
    f_qty = inputs['Fan Point']
    f_val = (math.ceil(f_qty / 3) * 60 / 1000) if category == "Domestic/Bulk Supply" else (f_qty * 60 / 1000)
    if f_qty > 0: table_data.append(["Fan Point (60W)", f_qty, f"{f_val:.3f} kW"])
    total_kw += f_val

    # 2. Lights (DS: 1/2 counted)[cite: 1]
    l_qty = inputs['Light Point']
    l_val = (math.ceil(l_qty / 2) * 40 / 1000) if category == "Domestic/Bulk Supply" else (l_qty * 40 / 1000)
    if l_qty > 0: table_data.append(["Light Point (40W)", l_qty, f"{l_val:.3f} kW"])
    total_kw += l_val

    # 3. Wall Sockets (DS: 1/4 | NRS: 1/3)[cite: 1]
    w_qty = inputs['Wall Socket (60W)']
    w_div = 4 if category == "Domestic/Bulk Supply" else 3
    w_val = (math.ceil(w_qty / w_div) * 60 / 1000)
    if w_qty > 0: table_data.append(["Wall Socket (60W)", w_qty, f"{w_val:.3f} kW"])
    total_kw += w_val

    # 4. Power Plugs (DS: 1/4 | NRS: 1/2)[cite: 1]
    p_qty = inputs['Power Plug (1000W)']
    p_div = 4 if category == "Domestic/Bulk Supply" else 2
    p_val = (math.ceil(p_qty / p_div) * 1000 / 1000)
    if p_qty > 0: table_data.append(["Power Plug (1000W)", p_qty, f"{p_val:.3f} kW"])
    total_kw += p_val

    # 5. Motor Load (BHP to kW)[cite: 1]
    m_val = inputs['Motor BHP'] * 0.746
    if m_val > 0:
        table_data.append([f"Motor ({inputs['Motor BHP']} BHP)", "Actual", f"{m_val:.3f} kW"])
        total_kw += m_val

    # 6. Standard Heavy Items[cite: 1]
    heavy_map = [
        ('Air Conditioner (2500W)', 2500), ('Geyser (1500W)', 1500),
        ('Refrigerator (250W)', 250), ('Dessert Cooler (250W)', 250),
        ('Washing Machine (500W)', 500)
    ]
    for name, watt in heavy_map:
        qty = inputs[name]
        val = (qty * watt / 1000)
        if qty > 0:
            table_data.append([name, qty, f"{val:.3f} kW"])
            total_kw += val

    # 7. Special Items[cite: 1]
    tp_val = math.ceil(inputs['3-Phase Socket (6kW)'] / 2) * 6.0
    if tp_val > 0:
        table_data.append(["3-Phase Socket (6kW)", inputs['3-Phase Socket (6kW)'], f"{tp_val:.3f} kW"])
        total_kw += tp_val

    ups_val = inputs['UPS Rating (kVA)'] * 0.90
    if ups_val > 0:
        table_data.append(["UPS (0.90 PF)", f"{inputs['UPS Rating (kVA)']} kVA", f"{ups_val:.3f} kW"])
        total_kw += ups_val

    weld_val = inputs['Welding Set (kVA)'] * 0.40
    if weld_val > 0:
        table_data.append(["Welding (0.40 PF)", f"{inputs['Welding Set (kVA)']} kVA", f"{weld_val:.3f} kW"])
        total_kw += weld_val

    # ---------------------------
    # Results & Export
    # ---------------------------
    st.divider()
    if table_data:
        st.subheader("📋 Computation Summary")
        df = pd.DataFrame(table_data, columns=["Description", "Quantity/Rating", "Load (kW)"])
        st.dataframe(df, use_container_width=True)
        
        # Grand Total Card
        st.markdown(f"""
            <div class="metric-card">
                <h2 style="color: #1e293b; margin:0;">Total Connected Load</h2>
                <h1 style="color: #0284c7; margin:0;">{total_kw:.3f} kW</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Export Option
        st.write("")
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Load_Sheet')
            # Add total to excel
            summary_df = pd.DataFrame([["TOTAL LOAD", "", f"{total_kw:.3f} kW"]], columns=df.columns)
            summary_df.to_excel(writer, index=False, startrow=len(df)+2, header=False)
        
        st.download_button(
            label="📥 Download Computation Sheet (Excel)",
            data=output.getvalue(),
            file_name="PSPCL_Load_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.info("Start entering item quantities to generate the report.")

    # ---------------------------
    # Footer
    # ---------------------------
    footer_html = f"""
<div class="footer-container"> <div class="made-with-love">Made with <span class="heart-symbol">❤️</span> by <b>Er. Anuj Narang, JE PSPCL</b></div> <div style="margin-bottom: 25px;"> <a href="https://instagram.com/iamanujnarang" target="_blank"><img src="{INSTA_ICON}" class="social-icon"></a> <a href="https://facebook.com/iamanujnarang" target="_blank"><img src="{FB_ICON}" class="social-icon"></a> <a href="https://x.com/iamanujnarang" target="_blank"><img src="{X_ICON}" class="social-icon"></a> <a href="https://linkedin.com/in/iamanujnarang" target="_blank"><img src="{LINKEDIN_ICON}" class="social-icon"></a> </div> <!-- Beeclue without box --> <div style="margin-top: 25px;"> <div class="powered-text">In Strategic Collaboration with</div> <a href="https://beeclue.com" target="_blank"> <img src="{BEECLUE_LOGO_PNG}" class="beeclue-img"> </a> </div> <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 25px;">© 2026 | PSPCL Guidelines</div> </div>"""
    st.markdown(footer_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
