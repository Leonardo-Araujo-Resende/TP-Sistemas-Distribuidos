# import threading
# import arcade

# class ControllerLoginCadastrar:
#     def __init__(self, ViewLoginCadastrar):
#         self.view = ViewLoginCadastrar

#     def get_usuario(self):
#         usuario = self.view.get_input_usuario()
#         senha = self.view.get_input_senha()
#         return usuario, senha

#     def verifica_usuario_senha_corretos(self, usuario, senha):
#         if usuario == "" or senha == "":
#             return False
#         else:
#             return True

#     def logar(self):
#         usuario, senha = self.get_usuario()
#         if self.verifica_usuario_senha_corretos(usuario,senha):
#             print("Pesquisa no banco")
#         else:
#             self.view.exibe_msg_usuario("Usuario ou Senha incorretos")
            


#     def cadastrar(self):
#         usuario, senha = self.get_usuario()
#         if self.verifica_usuario_senha_corretos(usuario,senha):
#             print("Cadastra usuario no banco")
#         else:
#             self.view.exibe_msg_usuario("Usuario ou Senha incorretos")

