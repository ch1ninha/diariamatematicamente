
def check_online(session):
    """
    Checa se existe a chave 'online_user' no dicionario da sessão
    Entrada -> session, dicionario que contem a sessão presente.
    Saida -> Se tive 'online_user' dentro da sessão, retorna Verdadeiro, caso contrario, Falso
    """
    if "online_user" not in session:
        return False
    return True

