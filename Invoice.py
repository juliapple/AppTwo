elif page == "Gerar Fatura PDF":
st.title("Gerar Fatura em PDF")

member_id = st.text_input("ID do Membro para Fatura")

if st.button("Gerar PDF"):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name, category FROM members WHERE member_id = ?", (member_id,))
    info = c.fetchone()

    if info:
        name, category = info
        c.execute("SELECT SUM(days_parked) FROM parking_records WHERE member_id = ?", (member_id,))
        dias = c.fetchone()[0] or 0
        total = calculate_parking_fee(category, dias)
        generate_invoice_pdf(name, total)
        st.success(f"Fatura gerada com sucesso para {name}!")
    else:
        st.warning("Membro não encontrado.")
    conn.close()

