from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from termcolor import colored
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import random

t=True
db = create_engine("sqlite:///meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios" 
    id=Column("id",Integer, primary_key=True, autoincrement=True)
    nome=Column("nome", String)
    email=Column("email", String)
    senha=Column("senha", String)
    ativo=Column("ativo", Boolean)

    def __init__(self, nome, email, senha, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        pass
Base.metadata.create_all(bind=db)

def GerarCodigo():
    codigo = random.randint(1000,9999)
    return str(codigo)

def MandarEmail(para, assunto, texto):
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587
    usuario = os.getenv('EMAIL_USER')
    senha = os.getenv('EMAIL_PASS')

    if not usuario or not senha:
        return 'Erro: credenciais de e-mail não configuradas nas variáveis de ambiente.'


    mensagem = MIMEMultipart()
    mensagem['From'] = usuario
    mensagem['To'] = para
    mensagem['Subject'] = assunto
    mensagem.attach(MIMEText(texto, 'plain'))


    try:
        with smtplib.SMTP(smtp_host, smtp_port) as servidor:
            servidor.starttls()
            servidor.login(usuario, senha)
            servidor.sendmail(usuario, para, mensagem.as_string())
        return 'Email enviado com sucesso!'
    except Exception as e:
        return f'Erro ao enviar e-mail: {e}'

def Create_User(nome,email,senha):
    try:
        user = Usuario(nome=nome, email=email, senha=senha, ativo=True)
        session.add(user)
        session.commit()
        print(colored("CONTA CRIADA COM SUCESSO!", "green"))

        admin_email_status = MandarEmail(
            "artificialomc@gmail.com",
            "🚛 UMA CONTA FOI CRIADA!",
            f"🆔 ID: {user.id}\n🟢 NOME: {user.nome}\n🟢 EMAIL: {user.email}"
        )

        user_email = MandarEmail(
            email,
            f"🎉 Bem-vindo(a) ao nosso banco de dados!",
            f"Olá, {nome.capitalize()}!\n🟢 É uma grande alegria tê-lo(a) conosco. 🎊\nEstamos aqui para garantir que você se sinta valorizado(a) e bem recebido(a) nesta nova jornada.\nNossa prioridade é proporcionar uma experiência incrível para você. Se precisar de qualquer coisa, não hesite em nos procurar. Estamos sempre prontos para ajudar. 💡\nSeja muito bem-vindo(a) à nossa comunidade. Vamos construir algo especial juntos! 🤝\nAtenciosamente,\nEquipe BL  / BL (Banco_Log)"
        )

        print(admin_email_status)

        print(user_email)

        time.sleep(6)

    except Exception as e:
        print(f"OCORREU UM ERRO: {e}")

def Update_User(action,id):
    if id or action:
        user=session.query(Usuario).filter_by(id=id).first()
        if action == 1:
            new_name = input("DIGITE O NOME: ")
            
            admin_email_status = MandarEmail(
            "artificialomc@gmail.com",
            "🔄 Alteração de Nome de Usuário",
            f"Olá, Admin.\n\n🔄 Informamos que o nome do usuário {user.nome.capitalize()} ID:{user.id} foi alterado com sucesso no sistema. O novo nome é: {new_name.capitalize()}.\n\nEssa alteração foi realizada por um administrador conforme a solicitação do usuário ou por decisão interna. \n\n Se precisar de mais informações, não hesite em nos procurar.\n\nAtenciosamente,\nEquipe BL  / BL (Banco_Log)"

        )

            user_email = MandarEmail(
            user.email,
            f"🚀 Seu Nome Foi Alterado com Sucesso!",
            f"Olá, {user.nome.capitalize()}.\n\n🚀 A sua conta foi atualizada com sucesso! Seu nome foi alterado para: {new_name.capitalize()}.\n\nAgradecemos por confiar em nosso sistema. Se precisar de mais alguma coisa ou tiver dúvidas, estamos sempre à disposição para ajudá-lo(a).\n\nAtenciosamente,\nEquipe BL / BL (Banco_Log)"
        )
            
            print(admin_email_status)

            print(user_email)

            time.sleep(6)

            user.nome=new_name
            session.add(user)
            session.commit()
            print(colored("ALTERAÇÃO FEITA COM SUCESSO!", "green"))
        elif action == 2:
            new_password = input("DIGITE A SENHA: ")

            admin_email_status = MandarEmail(
            "artificialomc@gmail.com",
            "🔒 Alteração de Senha de Usuário",
            f"Olá, Admin.\n\n🔒 Informamos que a senha do usuário {user.nome.capitalize()} ID:{user.id} foi alterada com sucesso no sistema. Essa alteração foi realizada por um administrador ou conforme a solicitação do próprio usuário.\n\nSe precisar de mais informações ou tiver alguma dúvida, entre em contato conosco.\n\nAtenciosamente,\nEquipe BL / BL (Banco_Log)"
            )

            user_email = MandarEmail(
            user.email,
            f"🚀 Sua Senha Foi Alterada com Sucesso!",
            f"Olá, {user.nome.capitalize()}.\n\n🚀 Sua senha foi alterada com sucesso! Agora, você pode acessar sua conta com a nova senha.\n\nSe não foi você quem fez essa alteração, ou se tiver alguma dúvida, entre em contato conosco imediatamente.\n\nAtenciosamente,\nEquipe BL / BL (Banco_Log)"
            )

            print(admin_email_status)

            print(user_email)

            time.sleep(6)

            user.senha=new_password
            session.add(user)
            session.commit()
            print(colored("ALTERAÇÃO FEITA COM SUCESSO!", "green"))
        elif action == 3:
            loop = True
            cod=GerarCodigo()
            cod_verficacao = MandarEmail(
            user.email,
            "🔔 Alerta de Mudança de E-mail + Código de Verificação",
            f"Olá, {user.nome.capitalize()}.\n\n🔔 Estamos realizando uma atualização em sua conta. O e-mail associado à sua conta está sendo alterado.\n\nPara confirmar que foi você quem solicitou essa mudança, por favor, use o código de verificação abaixo:\n\n📝 Código de Verificação: {cod}\n\nSe você não solicitou essa alteração, entre em contato imediatamente para proteger sua conta.\n\nAtenciosamente,\nEquipe BL / BL (Banco_Log)"
            )
            admin_email_status = MandarEmail(
            "artificialomc@gmail.com",
            "⚠️ Alteração de E-mail de Usuário",
            f"Olá, Admin.\n\n⚠️ O e-mail do usuário {user.nome.capitalize()} ID{user.id} está sendo alterado. A solicitação foi feita recentemente, e estamos aguardando a confirmação do código de verificação.\n\nPor favor, esteja atento caso haja algum problema ou solicitação de cancelamento dessa alteração.\n\nAtenciosamente,\nEquipe BL / BL (Banco_Log)"
            )
            print(admin_email_status)

            print(cod_verficacao)

            time.sleep(6)
            while loop:
                cod_email = input("DIGITE O CÓDIGO DE VERIFICAÇÃO: ")
                if cod_email == cod:
                    new_email=input("DIGITE O NOVO EMAIL: ")
                    e=To_Check(new_email)
                if e:
                    a_email=user.email
                    user.email=new_email

                    admin_email_status = MandarEmail(
                    "artificialomc@gmail.com",
                    "⚙️ E-mail Alterado - Confirmação",
                    f"Olá, Admin.\n\n✅ O e-mail do usuário {user.nome.capitalize()} ID{user.id} foi alterado com sucesso. A alteração foi concluída e agora o usuário usa o novo e-mail para acessar sua conta.\n\nPor favor, esteja atento para quaisquer outras solicitações ou alterações de dados dos usuários.\n\nAtenciosamente,\nEquipe BL / BL (Banco_Log)"
                    )
                    a_user_email = MandarEmail(
                    a_email,
                    f"🔔 Notificação de Alteração de E-mail",
                    f"Olá, {user.nome.capitalize()}.\n\n👋 Informamos que o e-mail associado à sua conta foi alterado recentemente. Caso você não tenha sido responsável por essa alteração, por favor, entre em contato conosco imediatamente para que possamos resolver qualquer problema.\n\nSe a alteração foi sua, não há mais nada que você precise fazer. O novo e-mail será agora utilizado para as futuras comunicações e acessos à sua conta.\n\nAtenciosamente,\nEquipe BL / BL (Banco_Log)"
                    )
                    
                    user_email = MandarEmail(
                    user.email,
                    f"🚀 Sua Senha Foi Alterada com Sucesso!",
                    f"Olá, {user.nome.capitalize()}.\n\n✅ Informamos que o seu e-mail foi alterado com sucesso! A partir de agora, você usará o novo e-mail para acessar sua conta.\n\nSe você não foi o responsável por essa alteração, entre em contato conosco imediatamente para resolvermos qualquer problema.\n\nAgradecemos por fazer parte da nossa comunidade!\n\nAtenciosamente,\nEquipe BL / BL (Banco_Log)"
                    )

                    print(admin_email_status)
                    print(user_email)
                    print(a_user_email)
                    
                    time.sleep(6)

                    session.add(user)
                    session.commit()
                    print(colored("ALTERAÇÃO FEITA COM SUCESSO!", "green"))
                    loop=False
                else:
                    print(colored("ESSE EMAIL JÁ ESTÁ REGISTRADO EM UMA CONTA! DIGITE OUTRO!", "yellow"))
    else:
        print("AS INFORMAÇÕES PARA EXECUTAR A FUNÇÃO NÃO FORAM PREENCHIDAS.")

def Delete_User(id):
    user = session.query(Usuario).filter_by(id=id).first()
    
    msg_admin=MandarEmail(
        "artificialomc@gmail.com",
        "🚨 Conta Deletada - Ação Administrativa",
        f"Olá, Admin.\n\n🚨 Informamos que a conta:\nID:{user.id}\nNOME:{user.nome}\n Foi deletada com sucesso por um administrador. Ação concluída conforme as diretrizes do sistema.\n\nSe precisar de mais detalhes ou tiver alguma dúvida sobre essa operação, estamos à disposição para esclarecimentos.\n\nAtenciosamente,\nEquipe BL  / BL (Banco_Log)"
    )

    msg_user=MandarEmail(
        user.email,
        "⚠️ Sua Conta foi Deletada",
        f"Olá, {user.nome.capitalize()}.\n⚠️ Sua conta foi deletada por um administrador. 🗑️\nSe você acredita que isso foi um engano ou gostaria de saber mais detalhes, por favor, entre em contato conosco para esclarecer a situação.\nQueremos garantir a transparência e estamos à disposição para ajudar da melhor forma possível. 💬\n\nAtenciosamente,\nEquipe BL  / BL (Banco_Log)"
    )

    print(msg_admin)
    print(msg_user)

    time.sleep(6)

    session.delete(user)
    session.commit()
    print(colored("CONTA DELETADA COM SUCESSO!", "green"))

def To_Check(emailt):
    v_e=session.query(Usuario).filter_by(email=emailt).first()
    if v_e:
        return False
    else:
        return True
while t:
    print("OQUE VOCÊ QUER FAZER NO BANCO DE DADOS?")
    print("1.CRIAR USUÁRIOS")
    print("2.ATUALIZAR USUÁRIOS")
    print("3.DELETAR USUÁRIOS")
    print("4.SAIR")
    escolha=input("DIGITE SUA ESCOLHA: ")
    if escolha == "1":
        loop=True
        print(colored("OK PARA CRIAR USUARIOS PRECISAMOS DE INFORMAÇÕES BASICAS!", "yellow"))
        nome=input("DIGITE O NOME: ")
        email1=input("DIGITE O EMAIL: ")
        senha=input("DIGTE A SENHA: ")
        c_senha=input("CONFIRME A SENHA: ")
        verification=To_Check(email1)
        if nome and email1 and senha and c_senha:
            if verification:
                if senha == c_senha:
                    Create_User(nome,email1,senha)
                else:
                    print(colored("SENHAS NAO CONFEREM!", "yellow"))
            else:
                print(colored("ESTE E-MAIL JÁ EXISTE!", "yellow"))
        else:
            print(colored("NÃO ACEITAMOS NENHUM DOS CAMPOS VAZIOS!", "yellow"))
    
    elif escolha == "2":
        confirm=False
        print(colored("PARA ATUALIZAR QUALQUER USUÁRIO PRECISAREMOS DO ID!", "yellow"))
        id=input("DIGITE O ID: ")
        if id:
            user = session.query(Usuario).all()
            for users in user:
                if users.id == int(id):
                    nome=users.nome
                    email=users.email
                    senha=users.senha
                    confirm=True
                    break
            if confirm:
                update=True
                print(colored(f"ID:{id}", "green"))
                print(colored(f"NOME:{nome}", "green"))
                print(colored(f"EMAIL:{email}", "green"))
                print(colored(f"SENHA:{senha}", "green"))
                print(colored("OQUE VOCÊ DESEJA ALTERA-LO?", "yellow"))
                while update:
                    escolha_up=input("DIGITE OQUE VOCÊ QUER ALTERAR: ")
                    if escolha_up == "nome" or escolha_up == "Nome" or escolha_up == "NOME":
                        Update_User(1,id)
                        break
                    elif escolha_up == "email" or escolha_up == "Email" or escolha_up == "EMAIL":
                        Update_User(3,id)
                        break
                    elif escolha_up == "senha" or escolha_up == "Senha" or escolha_up == "SENHA":
                        Update_User(2,id)
                        break
                    elif escolha_up == "id" or escolha_up == "Id" or escolha_up == "ID":
                        print(colored("NÃO MUDAMOS O ID DO USER", "yellow"))
                    elif escolha_up == "sair" or escolha_up == "Sair" or escolha_up == "SAIR":
                        break
                    else:
                        print(colored("VOCÊ NÃO DIGITOU NENHUM CAMPO QUE CORRESPONDA COM ALTERAÇÃO ESCREVA SOMENTE O NOME DO QUE VOCÊ QUER ALTERAR EX:NOME", "yellow"))
            else:
                print(colored("NÃO ENCONTRAMOS ESSE ID", "yellow"))
    elif escolha == "3":
        confirm=False
        print(colored("PARA DELETAR QUALQUER USUÁRIO PRECISAREMOS DO ID!", "yellow"))
        id=input("DIGITE O ID: ")
        if id:
            user = session.query(Usuario).all()
            for users in user:
                if users.id == int(id):
                    nome=users.nome
                    email=users.email
                    senha=users.senha
                    confirm=True
                    break
            if confirm:
                delete=True
                escolha_up=input(f"VOCÊ TEM CERTEZA QUE QUER DELETAR O ID:{id} : ")
                while delete:
                    if escolha_up == "sim" or escolha_up == "Sim" or escolha_up == "SIM":
                        Delete_User(id)
                        break
                    elif escolha_up == "nao" or escolha_up == "Nao" or escolha_up == "NAO" or escolha_up == "não" or escolha_up == "Não" or escolha_up == "NÃO":
                        break
                    else:
                        print(colored("VOCÊ NÃO DIGITOU NENHUM CAMPO QUE CORRESPONDA COM DELETAR ESCREVA SOMENTE SIM OU NAO", "yellow"))
    elif escolha == "4":
        break