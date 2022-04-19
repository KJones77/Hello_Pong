# pong bar class

class pong_character():
    def __init__(self, window_width, window_height):
        if (window_height or window_width > 0):
            self.image = None
            self.width = window_width / 50
            self.height = window_height / 4
            self.spawn = (0, 0)
            self.move_speed = self.height / 10
            self.resized_pong = None
        return None
