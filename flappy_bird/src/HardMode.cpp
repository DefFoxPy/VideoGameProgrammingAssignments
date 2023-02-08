/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: CarrlosULA


    This file contains the definition of the class HardMode.
*/

#include <src/HardMode.hpp>

HardMode::HardMode(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird) :
    GameMode(_world, _bird) {}


void HardMode::handle_inputs(const sf::Event& event) noexcept 
{
    if (event.key.code == sf::Keyboard::Up) 
    {
        bird->jump();
    }
    
    else if (event.key.code == sf::Keyboard::Left)
    {
        bird->left();
    }
    else if (event.key.code == sf::Keyboard::Right)
    {
        bird->right();
    }  
} 

void HardMode::update(float dt) noexcept
{
    bird->update(dt);
    world->update(dt, true);
}