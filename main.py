import os
import pygame as pg
from game_tools import Paddle, Ball
from game_intelligence import PaddleBot
import time

def main():
    pg.init()

    clock = pg.time.Clock()
    WIDTH, HEIGHT = 800, 600

    BLACK = (0,0,0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0,0,255)
    YELLOW = (255, 255, 0)

    win = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Paddle game')
    
    paddle_player = Paddle(color=RED, position=(20, HEIGHT/2))
    paddle_bot = Paddle(color=YELLOW, position=(WIDTH-20, HEIGHT/2), velocity=5)    
    ball = Ball(position=(50, HEIGHT/2), direction=(-1, 0), velocity=10)

    bot = PaddleBot(paddle_bot, ball)

    run = True
    moving_ball = False
    while run:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.K_ESCAPE:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    ball.swap_direct_v()

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            paddle_player.move_up()
        elif keys[pg.K_s]:
            paddle_player.move_down()
        if keys[pg.K_RETURN]:
            moving_ball = True

        bot.check_situation()

        if moving_ball:
            ball.make_move()


        win.fill(BLACK)
        pg.draw.rect(win, paddle_player.Color, paddle_player.Rect_properties)
        pg.draw.rect(win, paddle_bot.Color, paddle_bot.Rect_properties)
        pg.draw.circle(win, *ball.Circle_properties)
        pg.display.update()

        if ball.Position.Y - ball.Radius <= 0:
            ball.swap_direct_v()
        elif ball.Position.Y + ball.Radius >= HEIGHT:
            ball.swap_direct_v()
        
        if ball.Position.X >= WIDTH or ball.Position.X <= 0:
            run = False
            print(f'ball: {ball.Position.Y}')
            continue

        # print("-----")
        # print('Ball: ' + str(ball.Position))
        # print('PAd: ' + str(paddle_player.Position))
        # print(f'Slope {ball.Direction.Slope}')

        if (ball.Position.X - ball.Radius <= paddle_player.Position.X + paddle_player.Size[0]/2):
            cond = (ball.Position.Y + ball.Radius >= paddle_player.upper_left_coords()[1] \
                and ball.Position.Y - ball.Radius <= paddle_player.upper_left_coords()[1]+paddle_player.Size[1])
            if cond:
                new_direction = paddle_player.Position - ball.Position
                # new_direction.turn_vert()
                ball.change_direction(new_direction)
                # time.sleep(1)

        elif (ball.Position.X + ball.Radius >= paddle_bot.Position.X - paddle_bot.Size[0]/2):
            cond = (ball.Position.Y + ball.Radius >= paddle_bot.upper_left_coords()[1] \
                and ball.Position.Y - ball.Radius <= paddle_bot.upper_left_coords()[1]+paddle_bot.Size[1])
            if cond:
                new_direction = paddle_bot.Position - ball.Position
                # new_direction.turn_vert()
                ball.change_direction(new_direction)

    pg.quit()

if __name__=='__main__':
    main()