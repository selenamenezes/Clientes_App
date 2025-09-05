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