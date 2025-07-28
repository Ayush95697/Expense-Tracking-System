import streamlit as st
from datetime import datetime
import requests
import pandas as pd

# Set your FastAPI backend URL
API_URL = "http://127.0.0.1:8000"

st.title("💸 Expense Tracking System")

# Tabs for Add/Update and Analytics
tab1, tab2 = st.tabs(["➕ Add / Update Expenses", "📊 Analytics"])

# Define categories
categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

# --------------- TAB 1: ADD / UPDATE EXPENSES -----------------
with tab1:
    selected_date = st.date_input("Select Date", datetime(2024, 8, 1), label_visibility="collapsed")

    # Fetch existing expenses for that date
    try:
        res = requests.get(f"{API_URL}/expenses/{selected_date}")
        if res.status_code == 200:
            existing_expenses = res.json()
        else:
            st.warning("No data found or error fetching data.")
            existing_expenses = []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        existing_expenses = []

    # Expense form
    with st.form(key="expense_form"):
        st.markdown("### Enter up to 5 expenses")
        col1, col2, col3 = st.columns(3)
        with col1: st.text("Amount")
        with col2: st.text("Category")
        with col3: st.text("Notes")

        expenses = []

        for i in range(5):
            if i < len(existing_expenses):
                default_amount = existing_expenses[i]["amount"]
                default_category = existing_expenses[i]["category"]
                default_notes = existing_expenses[i]["notes"]
            else:
                default_amount = 0.0
                default_category = "Shopping"
                default_notes = "---"

            col1, col2, col3 = st.columns(3)

            with col1:
                amount_input = st.number_input(
                    label="Amount",
                    min_value=0.0,
                    step=1.0,
                    value=default_amount,
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )

            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(default_category) if default_category in categories else 2,
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )

            with col3:
                notes_input = st.text_input(
                    label="Notes",
                    value=default_notes,
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        submit = st.form_submit_button("💾 Save Expenses")
        if submit:
            filtered_expenses = [e for e in expenses if e["amount"] > 0]
            try:
                post_res = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
                if post_res.status_code == 200:
                    st.success("✅ Expenses updated successfully!")
                else:
                    st.error(f"❌ Error: {post_res.status_code} - {post_res.text}")
            except Exception as e:
                st.error(f"Error sending request: {e}")

# ---------------- TAB 2: ANALYTICS -------------------
with tab2:
    st.subheader("Select a date range to view expense analytics")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 15))

    if st.button("📊 Get Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
        }

        try:
            analytics_res = requests.post(f"{API_URL}/analytics", json=payload)
            if analytics_res.status_code == 200:
                data_json = analytics_res.json()

                data = {
                    "Category": list(data_json.keys()),
                    "Total": [data_json[cat]["total"] for cat in data_json],
                    "Percentage": [data_json[cat]["percentage"] for cat in data_json]
                }

                df = pd.DataFrame(data)
                df_sorted = df.sort_values("Percentage", ascending=False)

                st.title("📈 Expense Breakdown")
                st.bar_chart(df_sorted.set_index("Category")["Percentage"])
                st.table(df_sorted)
            else:
                st.error(f"❌ Error: {analytics_res.status_code} - {analytics_res.text}")
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
