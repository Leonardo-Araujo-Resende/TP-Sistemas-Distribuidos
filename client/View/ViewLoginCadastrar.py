import arcade 
import arcade.csscolor
import arcade.gui
from arcade.gui import UILabel
from arcade.gui.widgets import UIInputText
from controller.ControllerLoginCadastrar import *

class ViewLoginCadastrar(arcade.Window):

    def __init__(self, width, height, title, controller_log_cad: ControllerLoginCadastrar):
        super().__init__(width, height, title, center_window=True)
                
        self.corEscura = arcade.color_from_hex_string("#08D8FF")
        self.corClara = arcade.color_from_hex_string("#220B60")       

        arcade.set_background_color(self.corEscura)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        #Titulo
        self.manager.add(
            UILabel( text="Corrida Maluca", x=width/2 - 500/2, y=500, width=500, height=80, align="center", font_name="Roboto", font_size=40,text_color=self.corClara)
        )
        
        #Usuario
        self.manager.add(
            UILabel( text="Usuário*", x=width/2 - 270/2, y=430, width=270, height=30, font_name="Roboto", font_size=16,text_color=self.corClara)
        )
        self.input_usuario = UIInputText(x=width/2 - 270/2, y=380, width=320, height=30, font_name="Roboto", font_size=15, text_color=self.corClara)
        self.manager.add(self.input_usuario)

        #Senha
        self.input_senha = UILabel(text="Senha*", x=width/2 - 270/2, y=330, width=270, height=30, font_name="Roboto", font_size=16,text_color=self.corClara)
        self.manager.add(self.input_senha)
        self.manager.add(
            UIInputText(x=width/2 - 270/2, y=280, width=270, height=30, font_name="Roboto", font_size=15, text_color=self.corClara)
        )
        

        botao_style = {
            "font_name": "Roboto",
            "font_size": 15,
            "font_color": self.corClara,
            "border_width": 2,
            "border_color": self.corClara,
            "bg_color": self.corEscura,

            "bg_color_pressed": arcade.color.BLACK,
            "border_color_pressed": self.corEscura,  
            "font_color_pressed": self.corClara,
        }
        
        #Botao logar
        botao_logar = arcade.gui.UIFlatButton(x=500,y=170,text="Logar",height=60,width=300,style=botao_style)
        self.manager.add(botao_logar)
        
        @botao_logar.event
        def on_click(event):
            
            if controller_log_cad.sign_in(self.get_input_usuario(), self.get_input_senha()) == 0:
                self.exibe_msg_usuario("Login feito")
            else:
                self.exibe_msg_usuario("Credenciais incorretas")


        #Botao cadastrar
        botao_cadastrar = arcade.gui.UIFlatButton(x=500,y=100,text="Cadastrar",height=60,width=300,style=botao_style)
        self.manager.add(botao_cadastrar)

        @botao_cadastrar.event
        def on_click(event):
            if controller_log_cad.sign_up(self.get_input_usuario(), self.get_input_senha()) == 0:
                self.exibe_msg_usuario("Usuario cadastrado com sucesso")
            else:
                self.exibe_msg_usuario("Usuario ja existe")
            

        #Mensagens
        self.mensagem_usuario = UILabel( text="", x=width/2 - 400/2, y=50, width=400, height=30, font_name="Roboto", align="center",font_size=10,text_color=arcade.color.RED)
        self.manager.add(self.mensagem_usuario)
        

    def on_draw(self):
        self.clear()
        self.manager.draw()

        #Retangulo Usuario
        arcade.draw_lrtb_rectangle_outline(
            left = 500,
            right = 800,
            top = 430,
            bottom = 370,
            color = self.corClara
        )

        #Retangulo Senha
        arcade.draw_lrtb_rectangle_outline(
            left = 500,
            right = 800,
            top = 330,
            bottom = 270,
            color = self.corClara
        )


        #Retangulo Tudo
        arcade.draw_lrtb_rectangle_outline(
            left = 400,
            right = 900,
            top = 650,
            bottom = 50,
            color = self.corClara
        )

    def get_input_usuario(self):
        return self.input_usuario.text

    def get_input_senha(self):
        return self.input_senha.text

    def exibe_msg_usuario(self, msg):
        self.mensagem_usuario.text = msg
        arcade.schedule( self.apagar_msg_usuario , 5)
    
    def apagar_msg_usuario(self, delta_time):
        self.mensagem_usuario.text = ""
        arcade.unschedule(self.apagar_msg_usuario)

