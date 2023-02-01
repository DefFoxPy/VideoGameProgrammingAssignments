/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Mint


    This file contains the definition of the class NormalMode.
*/

#include <src/NormalMode.hpp>

NormalMode::NormalMode(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird) :
    GameMode(_world, _bird) {}


void NormalMode::handle_inputs(const sf::Event& event) noexcept 
{
    if (event.key.code == sf::Keyboard::Up) {
        bird->jump();
    }
} 

void NormalMode::update(float dt) noexcept
{
    bird->update(dt);
    world->update(dt);
}