import streamlit as st
import sqlite3
from billing import calculate_parking_fee, generate_invoice_pdf

st.set_page_config(page_title="RIAC App", layout="centered")

def get_connection():
    return sqlite3.connect("club.db")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", [
    "Register Parking",
    "Parking History",
    "Member List",
    "Financial Report",
    "Generate PDF Invoice"
])

if page == "Register Parking":
    st.title("Register Parking")

    name = st.text_input("Member Name")
    member_id = st.text_input("Member ID")
    category = st.selectbox("Category", [
        "Full Town", "Full Town Family", "Full Country", "Full Country Family"
    ])
    days = st.number_input("Days Parked", min_value=0)

    if st.button("Save Parking Record"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS members (name TEXT, member_id TEXT PRIMARY KEY, category TEXT)")
        c.execute("INSERT OR IGNORE INTO members VALUES (?, ?, ?)", (name, member_id, category))
        c.execute("CREATE TABLE IF NOT EXISTS parking_records (member_id TEXT, days_parked INT)")
        c.execute("INSERT INTO parking_records VALUES (?, ?)", (member_id, days))
        conn.commit()
        conn.close()
        st.success("Parking registered successfully!")

elif page == "Parking History":
    st.title("Member Parking History")

    member_id = st.text_input("Enter Member ID")
    if st.button("Show History"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT SUM(days_parked) FROM parking_records WHERE member_id = ?", (member_id,))
        result = c.fetchone()
        total = result[0] or 0
        st.info(f"Total days parked: {total}")
        conn.close()

elif page == "Member List":
    st.title("Registered Members")

    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT m.name, m.member_id, m.category,
               IFNULL(SUM(p.days_parked), 0) as total_days
        FROM members m
        LEFT JOIN parking_records p ON m.member_id = p.member_id
        GROUP BY m.member_id
    """)
    rows = c.fetchall()
    conn.close()

    if rows:
        for row in rows:
            st.write(f"**{row[0]}** (ID: {row[1]} | {row[2]}) — {row[3]} days")
    else:
        st.warning("No members found.")

elif page == "Financial Report":
    st.title("Financial Report")

    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT m.category, SUM(p.days_parked)
        FROM members m
        JOIN parking_records p ON m.member_id = p.member_id
        GROUP BY m.category
    """)
    data = c.fetchall()
    conn.close()

    total_income = 0
    for category, days in data:
        value = calculate_parking_fee(category, days)
        total_income += value
        st.write(f"{category}: {days} days → €{value}")

    st.subheader(f"Total Revenue: €{total_income}")

elif page == "Generate PDF Invoice":
    st.title("Generate PDF Invoice")

    member_id = st.text_input("Member ID")

    if st.button("Generate Invoice"):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT name, category FROM members WHERE member_id = ?", (member_id,))
        info = c.fetchone()

        if info:
            name, category = info
            c.execute("SELECT SUM(days_parked) FROM parking_records WHERE member_id = ?", (member_id,))
            days = c.fetchone()[0] or 0
            total = calculate_parking_fee(category, days)
            generate_invoice_pdf(name, total)
            st.success(f"PDF invoice generated for {name}!")
        else:
            st.warning("Member not found.")
        conn.close()
