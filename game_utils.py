import wrapper


def handle_collisions(ball, paddle1, paddle2):
    super_charge_range = 2

    paddle = paddle1
    ball = ball
    left = paddle.pos[0]
    right = left + paddle.size[0]
    ball_left = ball.pos[0]
    ball_right = ball_left + ball.size[0]
    top = paddle.pos[1]
    bottom = top + paddle.size[1]
    ball_top = ball.pos[1]
    ball_bottom = ball_top + ball.size[1]
    if left <= ball_right and right >= ball_left and top <= ball_bottom and bottom >= ball_top:
        """if top + ((bottom - top) / 2 - super_charge_range) <= ball_top + ((ball_bottom - ball_top) / 2) <= top + (
                (bottom - top) / 2 + super_charge_range):
            ball.boost = True
        else:
            ball.boost = False"""
        wrapper.main.ping_sound.play()
        ball.direction *= -1
        ball.angle = (ball.pos[1] - paddle.pos[1]) / paddle.size[1]
        ball.pos[0] = paddle.pos[0] + paddle.size[0] + 1
        wrapper.main.bounces += 1
    else:
        paddle = paddle2
        left = paddle.pos[0]
        right = left + paddle.size[0]
        ball_left = ball.pos[0]
        ball_right = ball_left + ball.size[0]
        top = paddle.pos[1]
        bottom = top + paddle.size[1]
        ball_top = ball.pos[1]
        ball_bottom = ball_top + ball.size[1]
        if right >= ball_left and left <= ball_right and top <= ball_bottom and bottom >= ball_top:
            """if top + ((bottom - top) / 2 - super_charge_range) <= ball_top + ((ball_bottom - ball_top) / 2) <= top + (
                    (bottom - top) / 2 + super_charge_range):
                ball.boost = True
            else:
                ball.boost = False"""
            wrapper.main.ping_sound.play()
            ball.direction *= -1
            ball.angle = (ball.pos[1] - paddle.pos[1]) / paddle.size[1]
            ball.pos[0] = paddle.pos[0] - ball.size[0] - 1
            wrapper.main.bounces += 1