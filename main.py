import streamlit as st
import pandas as pd

import sqlite3

def conectar_banco():
    return sqlite3.connect("banco.db")

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("""
        create table if not exists cliente (
            nome text not null,
            cpf text not null primary key,
            email text not null unique
        )
    """)
    conn.commit()
    conn.close()

def formatar_cpf(cpf):
    cpf = cpf.replace("-", "").replace(" ", "").replace(".", "").strip()
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    else:
        return False
    
def verificar_email(email):
    email = email.strip()
    if "." and "@" in email:
        return True
    else:
        return False

def cadastrar_clientes(conn, nome, cpf, email):
    cursor = conn.cursor()
    cpf = formatar_cpf(cpf)

    if not verificar_email(email):
        return "E-mail inválido."
    if not cpf:
        return "CPF inválido."
    
    if not nome:
        return "Digite um nome"

    cursor.execute(
        'select cpf, email from cliente where cpf = ? or email = ?',
        (cpf, email)
    )
    if cursor.fetchone():
        return "Cliente já cadastrado."


    cursor.execute(
        'insert into cliente(nome, cpf, email) VALUES (?, ?, ?)',
        (nome.title(), cpf, email)
    )
    conn.commit()
    return "Cliente cadastrado com sucesso!"


def ler_clientes(conn):
    cursor = conn.cursor()
    cursor.execute('select * from cliente')
    registros = cursor.fetchall()

    clientes = []
    for cliente in registros:
        clientes.append({
            "nome": cliente[0].title(),
            "cpf": formatar_cpf(cliente[1]),
            "email": cliente[2],
        })
    return clientes 


def atualizar_clientes(conn, nome, cpf, email):

    cursor = conn.cursor()
    f_cpf = formatar_cpf(cpf)

    if not verificar_email(email):
        return "E-mail inválido."
    if not f_cpf:
        return "CPF inválido."
    
    if not nome:
        return "Digite um nome"

    cursor.execute('select * from cliente where cpf = ?', (f_cpf,))
    if cursor.fetchone():
        cursor.execute(
            'update cliente set nome = ?, email = ? where cpf = ?',
            (nome.title(), email, f_cpf)
        )
        conn.commit()
        return "Cliente atualizado com sucesso!"
    else:
        return "Cliente não encontrado."


def remover_cliente(conn, cpf):
    cursor = conn.cursor()
    f_cpf = formatar_cpf(cpf)

    if not f_cpf:
        return "CPF inválido"

    cursor.execute('select cpf from cliente where cpf = ?', (f_cpf,))
    if cursor.fetchone():
        cursor.execute('delete from cliente where cpf = ?', (f_cpf,))
        conn.commit()
        return "Cliente removido!"
    else:
        return "Cliente não encontrado."

def main():
    criar_tabela()
    conn = conectar_banco()

    st.title("Sistema de Cadastro")
    menu = st.sidebar.selectbox("Menu", ["Cadastrar", "Listar", "Atualizar", "Remover"])

    if menu == "Cadastrar":
        st.header("Cadastrar Cliente")
        nome = st.text_input("Nome")
        cpf = st.text_input("CPF")
        email = st.text_input("E-mail")

        if st.button("Cadastrar"):
            msg = cadastrar_clientes(conn, nome, cpf, email)
            st.success(msg)

    elif menu == "Listar":
        st.header("Lista de Clientes")
        clientes = ler_clientes(conn)

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
            msg = atualizar_clientes(conn, nome, cpf, email)
            st.success(msg)

    elif menu == "Remover":
        st.header("Remover Cliente")
        cpf = st.text_input("CPF do Cliente a Remover")

        if st.button("Remover"):
            msg = remover_cliente(conn, cpf)
            st.success(msg)

    conn.close()


if __name__ == '__main__':
    main()
