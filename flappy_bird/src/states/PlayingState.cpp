/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of the class PlayingBaseState.
*/

#include <Settings.hpp>
#include <src/text_utilities.hpp>
#include <src/states/StateMachine.hpp>
#include <src/states/PlayingState.hpp>
#include <src/NormalMode.hpp>

PlayingState::PlayingState(StateMachine* sm) noexcept
    : BaseState{sm}
{

}

void PlayingState::enter(std::shared_ptr<World> _world, std::shared_ptr<Bird> _bird, int _score) noexcept
{
    world = _world;
    score = _score;
    world->reset(true);
    
    if (_bird == nullptr)
    {
        bird = std::make_shared<Bird>(
            Settings::VIRTUAL_WIDTH / 2 - Settings::BIRD_WIDTH / 2, Settings::VIRTUAL_HEIGHT / 2 - Settings::BIRD_HEIGHT / 2,
            Settings::BIRD_WIDTH, Settings::BIRD_HEIGHT
        );
    }
    else
    {
        bird = _bird;
    }

    if (gameMode == nullptr) 
    {
        auto currentGameMode = state_machine->getGameMode();

        if (currentGameMode == "Normal") 
        {
            gameMode = std::make_shared<NormalMode>(world, bird);
        }
    }
}

void PlayingState::handle_inputs(const sf::Event& event) noexcept
{
    gameMode->handle_inputs(event);

    if (event.key.code == sf::Keyboard::P) 
    {
        state_machine->change_state("pause", world, bird, score);
    }
}

void PlayingState::update(float dt) noexcept
{
    gameMode->update(dt);

    if (world->collides(bird->get_collision_rect()))
    {
        Settings::sounds["explosion"].play();
        Settings::sounds["hurt"].play();
        state_machine->change_state("count_down");
    }

    if (world->update_scored(bird->get_collision_rect()))
    {
        ++score;
        Settings::sounds["score"].play();
    }
}

void PlayingState::render(sf::RenderTarget& target) const noexcept
{
    world->render(target);
    bird->render(target);
    render_text(target, 20, 10, "Score: " + std::to_string(score), Settings::FLAPPY_TEXT_SIZE, "flappy", sf::Color::White);
}