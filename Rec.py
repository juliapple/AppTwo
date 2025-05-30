if page == "Cadastro de Estacionamento":
  st.title("Cadastro de Estacionamento")

  name = st.text_input("Nome do Membro")
  member_id = st.text_input("ID do Membro")
  category = st.selectbox("Categoria", [
      "Full Town", "Full Town Family", "Full Country", "Full Country Family"
  ])
  days = st.number_input("Dias Estacionados", min_value=0)

  if st.button("Salvar Estacionamento"):
      conn = get_connection()
      c = conn.cursor()
      c.execute("CREATE TABLE IF NOT EXISTS members (name TEXT, member_id TEXT PRIMARY KEY, category TEXT)")
      c.execute("INSERT OR IGNORE INTO members VALUES (?, ?, ?)", (name, member_id, category))
      c.execute("CREATE TABLE IF NOT EXISTS parking_records (member_id TEXT, days_parked INT)")
      c.execute("INSERT INTO parking_records VALUES (?, ?)", (member_id, days))
      conn.commit()
      conn.close()
      st.success("Estacionamento registrado com sucesso!")
