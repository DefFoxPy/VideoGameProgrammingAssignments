/*
    ISPPJ1 2023
    Study Case: Pong

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of a pong paddle and the declaration
    of the functions to init it, update it, and render it.
*/

#pragma once

#include "hitbox.h"
#include "ball.h"

struct Paddle
{
    float x;
    float y;
    float width;
    float height;
    float vy;
    bool IA; // indica si será un jugador o la IA el que va a jugar
};

void init_paddle(struct Paddle* paddle, float x, float y, float w, float h, bool ia);

void build_paddle_hitbox(struct Paddle paddle, struct Hitbox* hitbox);

void update_paddle(struct Paddle* paddle, float dt);

void ia(struct Paddle* paddle, struct Ball ball);

void render_paddle(struct Paddle paddle);
