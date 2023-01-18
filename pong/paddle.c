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

void ia(struct Paddle* paddle, struct Ball ball)
{
    if (paddle->IA)
    {
         /* Movimientos de la IA
            En este caso seguirá el movimiento de la pelota
            la IA se moverá cuando la pelota esté en su campo
            sino se colocará en una posición neutra
        */
        float paddle_centro = paddle->y + paddle->height / 2;

        // determinar si la pelota está en el territorio de la IA (lado del tablero)
        bool en_territorio = fabs(ball.x + ball.width/2 - paddle->x + paddle->width) < TABLE_WIDTH / 2;
        // condicional forzado pasa saber si la pelota biene al jugador  
        bool esta_viniendo = (ball.vx < 0 && paddle->x < TABLE_WIDTH / 2) ||
                             (ball.vx > 0 && paddle->x > TABLE_WIDTH / 2); 

        if (en_territorio && esta_viniendo)
        {
            // verdadero si la pelota está por arriba del jugador, caso contrario false
            bool aux = ball.y + ball.height / 2 < paddle_centro;
            // una variable que le indica a la IA a que diferencia hacer el cambio de velocidad
            // para generar un movimiento más fluido
            float diferencia = fabs(ball.y + ball.height / 2 - paddle_centro);  
            
            if (aux && diferencia > BALL_SIZE) 
            {
                paddle->vy = -PADDLE_SPEED;
            }
            else if (!aux && diferencia > BALL_SIZE) 
            {
                paddle->vy = PADDLE_SPEED;
            }
            else 
            {
                paddle->vy = 0;
            }
        }
        else if (!esta_viniendo) // dirigirse al centro de la pantalla
        {  
            float diferencia = fabs(paddle_centro - TABLE_HEIGHT / 2);

            if (paddle_centro > TABLE_HEIGHT / 2 && diferencia > PADDLE_WIDTH) 
            {
                paddle->vy = -PADDLE_SPEED;
            }
            else if (paddle_centro < TABLE_HEIGHT / 2 && diferencia > PADDLE_WIDTH) 
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
