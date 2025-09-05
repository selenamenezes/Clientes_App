import utils

def cadastrar_clientes(conn, nome, cpf, email):
    cursor = conn.cursor()
    cpf = utils.formatar_cpf(cpf)

    if not utils.verificar_email(email):
        return "E-mail inválido."
    if not cpf:
        return "CPF inválido."

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
            "cpf": utils.formatar_cpf(cliente[1]),
            "email": cliente[2],
        })
    return clientes 


def atualizar_clientes(conn, nome, cpf, email):

    cursor = conn.cursor()
    f_cpf = utils.formatar_cpf(cpf)

    if not utils.verificar_email(email):
        return "E-mail inválido."
    if not f_cpf:
        return "CPF inválido."

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
    f_cpf = utils.formatar_cpf(cpf)

    if not f_cpf:
        return "CPF inválido"

    cursor.execute('select cpf from cliente where cpf = ?', (f_cpf,))
    if cursor.fetchone():
        cursor.execute('delete from cliente where cpf = ?', (f_cpf,))
        conn.commit()
        return "Cliente removido!"
    else:
        return "Cliente não encontrado."
