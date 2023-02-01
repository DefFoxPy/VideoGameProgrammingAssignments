/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Mint


    This file contains the declaration of the class NormalMode.
*/

#pragma once

#include <src/GameMode.hpp>

class NormalMode : public GameMode 
{
public:
    NormalMode(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird);

    void handle_inputs(const sf::Event& event) noexcept;

    void update(float dt) noexcept;
};