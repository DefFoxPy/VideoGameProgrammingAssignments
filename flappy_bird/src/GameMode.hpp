/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Mint


    This file contains the definition of the class GameMode.
*/

#pragma once 

#include <SFML/Graphics.hpp>

#include <src/Bird.hpp>
#include <src/World.hpp>

class GameMode 
{
public:
    GameMode(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird) :
        bird{_bird}, world{_world} {}

    virtual void handle_inputs(const sf::Event& event) noexcept {}

    virtual void update(float dt) noexcept {}

protected:
    std::shared_ptr<Bird> bird;
    std::shared_ptr<World> world;
};