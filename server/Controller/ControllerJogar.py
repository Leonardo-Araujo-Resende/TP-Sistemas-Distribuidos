
class ControllerJogar():
    def __init__(self):
        self.qt_users_ready = 0
        self.game_is_ready = False
    
    def set_user_ready(self):
        self.qt_users_ready += 1
    
    def set_game_ready(self):
        self.game_is_ready = True       
    
    