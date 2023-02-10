/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Mint


    This file contains the definition of the class PauseState.
*/

#include <Settings.hpp>
#include <src/text_utilities.hpp>
#include <src/states/StateMachine.hpp>
#include <src/states/PauseState.hpp>

PauseState::PauseState(StateMachine* sm) noexcept
    : BaseState{sm}
{

}

void PauseState::enter(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird, int _score) noexcept
{
    world = _world;
    bird = _bird;
    score = _score;

    Settings::music.pause();
    Settings::music_potion.pause();
}

void PauseState::handle_inputs(const sf::Event& event) noexcept
{
    if (event.key.code == sf::Keyboard::P) 
    {
        state_machine->change_state("playing", world, bird, score);
    }
}

void PauseState::update(float dt) noexcept 
{
    world->update(0.0);
    bird->update(0.0);
}

void PauseState::render(sf::RenderTarget& target) const noexcept 
{
    world->render(target);
    bird->render(target);
    render_text(target, Settings::VIRTUAL_WIDTH / 2, Settings::VIRTUAL_HEIGHT / 2, "Game paused\npress 'P' to continue", Settings::FLAPPY_TEXT_SIZE, "flappy", sf::Color::White, true);
    render_text(target, 20, 10, "Score: " + std::to_string(score), Settings::FLAPPY_TEXT_SIZE, "flappy", sf::Color::White);
}   