import streamlit as st
import database
import utils
import crud
import pandas as pd

def main():
    database.criar_tabela()
    conn = database.conectar_banco()

    st.title("Sistema de Cadastro")
    menu = st.sidebar.selectbox("Menu", ["Cadastrar", "Listar", "Atualizar", "Remover"])

    if menu == "Cadastrar":
        st.header("Cadastrar Cliente")
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        email = st.text_input("E-mail")

        if st.button("Cadastrar"):
            msg = crud.cadastrar_clientes(conn, nome, cpf, email)
            st.success(msg)

    elif menu == "Listar":
        st.header("Lista de Clientes")
        clientes = crud.ler_clientes(conn)

        if clientes:
            df = pd.DataFrame(clientes)
            st.dataframe(df)
        else:
            st.info("Nenhum cliente cadastrado.")

    elif menu == "Atualizar":
        st.header("Atualizar Cliente")
        cpf = st.text_input("CPF: ")
        nome = st.text_input("Novo Nome")
        email = st.text_input("Novo E-mail")

        if st.button("Atualizar"):
            msg = crud.atualizar_clientes(conn, nome, cpf, email)
            st.success(msg)

    elif menu == "Remover":
        st.header("Remover Cliente")
        cpf = st.text_input("CPF do Cliente a Remover")

        if st.button("Remover"):
            msg = crud.remover_cliente(conn, cpf)
            st.success(msg)

    conn.close()


if __name__ == '__main__':
    main()
