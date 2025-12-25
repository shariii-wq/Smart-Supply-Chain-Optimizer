import streamlit as st
import math
import pandas as pd

# 1. DATABASE SETUP
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": 101, "name": "Wireless Mouse", "stock": 45, "cost": 15.0, "h_cost": 2.0, "o_cost": 50.0, "lead": 5, "usage": 10, "safety": 20, "supplier": "TechSupply Co."},
        {"id": 102, "name": "Gaming Keyboard", "stock": 10, "cost": 40.0, "h_cost": 5.0, "o_cost": 60.0, "lead": 7, "usage": 5, "safety": 15, "supplier": "GamerGear Ltd."}
    ]

# 2. CORE LOGIC
def calculate_eoq(demand, order_cost, holding_cost):
    annual_demand = demand * 365
    result = math.sqrt((2 * annual_demand * order_cost) / holding_cost)
    return round(result, 2)

def calculate_rop(daily_usage, lead_time, safety_stock):
    return (daily_usage * lead_time) + safety_stock

# 3. INTERFACE
st.title("📦 Smart Supply Chain Optimizer")

st.sidebar.header("User Access")
user_role = st.sidebar.selectbox("Login as:", ["Select Role", "Warehouse Staff", "Procurement Officer", "System Admin"])

if user_role == "Warehouse Staff":
    st.header("Inventory Management")
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
    st.write("System Status: 99.9% Uptime")
    df = pd.DataFrame(st.session_state.inventory)
    st.bar_chart(df, x="name", y="stock")
    st.subheader("30-Day Demand Forecast")
    for item in st.session_state.inventory:
        forecast = item['usage'] * 30
        st.write(f"🔮 {item['name']}: {forecast} units predicted.")
else:
    st.info("Please select your role in the sidebar to begin.")
