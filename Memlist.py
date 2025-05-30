elif page == "Lista de Membros":
st.title("Todos os Membros")

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
        st.write(f"**{row[0]}** (ID: {row[1]} | {row[2]}) — {row[3]} dias")
else:
    st.warning("Nenhum membro encontrado.")
