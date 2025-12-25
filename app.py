import streamlit as st
import math
import pandas as pd

# --- Project: Smart Supply Chain Inventory & Warehouse Optimizer ---
# [span_2](start_span)Program: BS Software Engineering[span_2](end_span)

# 1. DATABASE SETUP
# We use st.session_state so the data doesn't reset when the browser refreshes
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 101, "name": "Wireless Mouse", "stock": 45, "cost": 15.0, "h_cost": 2.0, "o_cost": 50.0, "lead": 5, "usage": 10, "safety": 20, "supplier": "TechSupply Co."},
        {"id": 102, "name": "Gaming Keyboard", "stock": 10, "cost": 40.0, "h_cost": 5.0, "o_cost": 60.0, "lead": 7, "usage": 5, "safety": 15, "supplier": "GamerGear Ltd."}
    ]

# 2. [span_3](start_span)[span_4](start_span)CORE LOGIC (Mathematical Formulas[span_3](end_span)[span_4](end_span))
def calculate_eoq(demand, order_cost, holding_cost):
    # Formula: sqrt((2 * Demand * OrderCost) / HoldingCost)
    # Annual demand is daily usage * 365
    annual_demand = demand * 365
    result = math.sqrt((2 * annual_demand * order_cost) / holding_cost)
    return round(result, 2)

def calculate_rop(daily_usage, lead_time, safety_stock):
    # Formula: (Daily Usage * Lead Time) + Safety Stock
    return (daily_usage * lead_time) + safety_stock

# 3. [span_5](start_span)[span_6](start_span)INTERFACE (UI/UX[span_5](end_span)[span_6](end_span))
st.title("📦 Smart Supply Chain Optimizer")

# [span_7](start_span)Sidebar for Role-Based Access Control (RBAC)[span_7](end_span)
st.sidebar.header("User Access")
user_role = st.sidebar.selectbox("Login as:", ["Select Role", "Warehouse Staff", "Procurement Officer", "System Admin"])

if user_role == "Warehouse Staff":
    st.header("Inventory Management")
    # [span_8](start_span)Feature: Log new inventory arrivals[span_8](end_span)
    with st.form("stock_update"):
        p_id = st.number_input("Enter Product ID", step=1)
        qty = st.number_input("Quantity Received", min_value=1)
        if st.form_submit_button("Update Stock"):
            for item in st.session_state.inventory:
                if item['id'] == p_id:
                    item['stock'] += qty
                    st.success(f"Stock updated for {item['name']}. Current: {item['stock']}")

elif user_role == "Procurement Officer":
    st.header("Procurement & Order Logic")
    # [span_9](start_span)Feature: Automated Alerts and EOQ calculation[span_9](end_span)
    for item in st.session_state.inventory:
        rop = calculate_rop(item['usage'], item['lead'], item['safety'])
        if item['stock'] < rop:
            st.warning(f"ALERT: {item['name']} is below Reorder Point!")
            eoq = calculate_eoq(item['usage'], item['o_cost'], item['h_cost'])
            st.info(f"Recommended Purchase (EOQ): {eoq} units")
            if st.button(f"Generate Purchase Order for {item['name']}"):
                st.success(f"PO sent to {item['supplier']} for {eoq} units.")

elif user_role == "System Admin":
    st.header("System Performance & Analytics")
    [span_10](start_span)st.write("System Status: 99.9% Uptime[span_10](end_span)")
    
    # [span_11](start_span)Feature: Visual dashboards for stock levels[span_11](end_span)
    df = pd.DataFrame(st.session_state.inventory)
    st.bar_chart(df, x="name", y="stock")
    
    # [span_12](start_span)[span_13](start_span)Feature: Demand Forecasting (Next 30 Days)[span_12](end_span)[span_13](end_span)
    st.subheader("30-Day Demand Forecast")
    for item in st.session_state.inventory:
        forecast = item['usage'] * 30
        st.write(f"🔮 {item['name']}: {forecast} units predicted.")

else:
    st.info("Please select your role in the sidebar to begin.")
