import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="🧾 Super Store Invoice Generator", layout="centered")

st.title("🧾 Super Store Invoice Generator")

# --- Customer Details ---
st.header("🧑 Customer Details")
customer_name = st.text_input("Customer Name")
invoice_date = st.date_input("Invoice Date", datetime.now().date())

# --- Product Entry ---
st.header("🛒 Add Products")
products = []

with st.form("product_form", clear_on_submit=True):
    product_name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price = st.number_input("Unit Price", min_value=0.0, value=0.0, step=0.01)
    submitted = st.form_submit_button("➕ Add to Invoice")
    if submitted and product_name:
        products.append({"Product": product_name, "Qty": quantity, "Unit Price": price, "Total": quantity * price})
        if "invoice_items" not in st.session_state:
            st.session_state.invoice_items = []
        st.session_state.invoice_items.append(products[0])

# --- Invoice Table ---
st.header("🧾 Invoice Preview")

if "invoice_items" in st.session_state and st.session_state.invoice_items:
    df = pd.DataFrame(st.session_state.invoice_items)
    st.dataframe(df, use_container_width=True)

    subtotal = sum(item['Total'] for item in st.session_state.invoice_items)
    tax = subtotal * 0.10  # 10% tax
    grand_total = subtotal + tax

    st.markdown(f"**Subtotal:** ${subtotal:.2f}")
    st.markdown(f"**Tax (10%):** ${tax:.2f}")
    st.markdown(f"**Grand Total:** ${grand_total:.2f}")
else:
    st.info("Add products to generate invoice.")

# --- Reset ---
if st.button("🗑️ Reset Invoice"):
    st.session_state.invoice_items = []

