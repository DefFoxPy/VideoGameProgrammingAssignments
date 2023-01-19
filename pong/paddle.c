/*
    ISPPJ1 2023
    Study Case: Pong

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of the functions to init a pong paddle,
    update it, and render it.
*/

#include <allegro5/allegro_primitives.h>

#include "settings.h"
#include "paddle.h"
#include <math.h> // para usar el valor absoluto

void init_paddle(struct Paddle* paddle, float x, float y, float w, float h, bool ia)
{
    paddle->x = x;
    paddle->y = y;
    paddle->width = w;
    paddle->height = h;
    paddle->IA = ia;    // asignación de IA
    paddle->vy = 0;
}

void build_paddle_hitbox(struct Paddle paddle, struct Hitbox* hitbox)
{
    hitbox->x1 = paddle.x;
    hitbox->y1 = paddle.y;
    hitbox->x2 = paddle.x + paddle.width;
    hitbox->y2 = paddle.y + paddle.height;
}

void ia_movement(struct Paddle* paddle, struct Ball ball)
{
    if (paddle->IA)
    {
         /* AI movements
            In this case it will follow the movement of the ball.
            the AI will move when the ball is in its field
            otherwise it will be placed in the middle
        */
        float paddle_middle = paddle->y + paddle->height / 2;

        // determine if the ball is in the territory of the IA (backboard side)
        bool is_our_side = fabs(ball.x + ball.width/2 - paddle->x + paddle->width) < TABLE_WIDTH / 2;
        // conditional to determine if the ball reaches the paddle.
        bool is_ball_coming = (ball.vx < 0 && paddle->x < TABLE_WIDTH / 2) ||
                             (ball.vx > 0 && paddle->x > TABLE_WIDTH / 2); 

        if (is_our_side && is_ball_coming)
        {
            bool aux = ball.y + ball.height / 2 < paddle_middle;
            float difference = fabs(ball.y + ball.height / 2 - paddle_middle);  
            
            if (aux && difference > BALL_SIZE) 
            {
                paddle->vy = -PADDLE_SPEED;
            }
            else if (!aux && difference > BALL_SIZE) 
            {
                paddle->vy = PADDLE_SPEED;
            }
            else 
            {
                paddle->vy = 0;
            }
        }
        else if (!is_ball_coming) // paddle must go to the middle
        {  
            float difference = fabs(paddle_middle - TABLE_HEIGHT / 2);

            if (paddle_middle > TABLE_HEIGHT / 2 && difference > PADDLE_WIDTH) 
            {
                paddle->vy = -PADDLE_SPEED;
            }
            else if (paddle_middle < TABLE_HEIGHT / 2 && difference > PADDLE_WIDTH) 
            {
                paddle->vy = PADDLE_SPEED;
            }
            else {
                paddle->vy = 0;
            }
        }
        else   
        {
            paddle->vy = 0;
        }
    }    
}

void update_paddle(struct Paddle* paddle, float dt)
{
    paddle->y += paddle->vy * dt;
    paddle->y = MAX(0, MIN(paddle->y, TABLE_HEIGHT - PADDLE_HEIGHT));
}

void render_paddle(struct Paddle paddle)
{
    al_draw_filled_rectangle(
        paddle.x, paddle.y, paddle.x + paddle.width, paddle.y + paddle.height,
        al_map_rgb(255, 255, 255)
    );
}
