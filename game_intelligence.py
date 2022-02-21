from game_tools import Ball, Paddle

class PaddleBot:
    def __init__(self, paddle:Paddle, ball:Ball):
        self.me = paddle
        self.ball = ball

        self.checked = False
        self.target_position = 1e6
        self.last_way = self.ball.Direction.Way

    def check_situation(self):
        if self.ball.Direction.Way == 'R' and self.last_way == 'R':
            if not self.checked:
                y0 = self.ball.Position.Y
                offset = self.ball.Radius
                y_top = self.me.window_height - 2*offset
                x_dist = self.me.Position.X - self.ball.Position.X - self.ball.Radius - self.me.Size[0]/2
                s = self.ball.Direction.Slope
                
                if s == 0:
                    x_top = 0
                    x_1 = 0
                    self.target_position = y0
                else:
                    print('here')
                    x_top = y_top/s
                    x_1 = (y_top + offset - y0)/s
                    n = ((x_dist*s + y0)//y_top -1)
                    self.target_position = abs((-y_top)*((n+1)%2) + (x_dist - (x_1 + n*x_top))*s)

                print(self.target_position)
        
                self.checked = True
        
            if abs(self.me.Position.Y - self.target_position) >= self.ball.Velocity:
                if self.me.Position.Y  > self.target_position:
                    self.me.move_up()
                else:
                    self.me.move_down()
        elif self.ball.Direction.Way == 'L' and self.checked:
            self.checked = False
            self.target_position = 1e6

        self.last_way = self.ball.Direction.Way
    

