elif page == "Relatório Financeiro":
st.title("Resumo Financeiro")

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

total_geral = 0
for categoria, dias in data:
    valor = calculate_parking_fee(categoria, dias)
    total_geral += valor
    st.write(f"{categoria}: {dias} dias → €{valor}")

st.subheader(f"Faturamento total: €{total_geral}")
