elif page == "Histórico de Estacionamento":
st.title("Histórico por Membro")

member_id = st.text_input("Digite o ID do membro")
if st.button("Ver histórico"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(days_parked) FROM parking_records WHERE member_id = ?", (member_id,))
    result = c.fetchone()
    total = result[0] or 0
    st.info(f"Total de dias estacionados: {total}")
    conn.close()
