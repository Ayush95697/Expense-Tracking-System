import streamlit as st
from datetime import datetime
import requests
import pandas as pd








API_URL="http://127.0.0.1:8000"

st.title("Expense Tracking System")
tab1 , tab2=st.tabs(["ADD/Update","Analytics"])
categories=["Rent","Food","Shopping","Entertainment","Other"]

with tab1:
    selected_date=st.date_input(" Enter Date", datetime(2024,8,1),label_visibility="collapsed")
    response=requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code==200:
        existing_expense=response.json()

    else:
        st.error("Something went wrong")
        existing_expense=[]

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text(f"Amount")
        with col2:
            st.text(f"Category")
        with col3:
            st.text(f"Notes")
        expenses=[]
        for i in range(5):
            if i < len(existing_expense):
                amount = existing_expense[i]["amount"]
                category = existing_expense[i]["category"]
                notes = existing_expense[i]["notes"]
            else:
                amount = 0.0
                category = "Shopping"
                notes = "---"
            col1, col2 ,col3 = st.columns(3)
            with col1:

                amount_input=st.number_input("Amount", min_value=0.0, step=1.0,value=amount,key=f"Amount {i}",label_visibility="collapsed")
            with col2:

                category_input=st.selectbox("Category",options= categories,index=categories.index(category), key=f"Category {i}",label_visibility="collapsed")
            with col3:

                notes_input = st.text_input("Notes",value=notes,key=f"Notes {i}",label_visibility="collapsed")

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input
            })

        submit_button=st.form_submit_button()
        if submit_button:
            filtered_expenses=[expenses for expenses in expenses if expenses["amount"] >0]
            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code==200:
                st.success("Expense successfully updated")
            else:
                st.error("Something went wrong")

    with tab2:
        col1, col2=st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime(2024, 8, 1))
        with col2:
            end_date=st.date_input("End Date", datetime(2024, 8, 1))

        if st.button("Get Analytics"):
            payload = {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
            }
            response = requests.post(f"{API_URL}/analytics", json=payload)
            response=response.json()

#         now to convert the given response into proper table

        data={
            "Category": list(response.keys()),
            "Total":[response[category]["total"] for category in response],
            "Percentage":[response[category]["percentage"] for category in response],
        }
        df=pd.DataFrame(data)
        df_sorted=df.sort_values("Percentage",ascending=False)
        st.title("Expense Breakdown")
        st.bar_chart(df_sorted.set_index(["Category"])["Percentage"])
        st.table(df_sorted)

