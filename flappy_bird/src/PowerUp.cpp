/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Mint, CarlosULA


    This file contains the definition of the class PowerUp.
*/

#include <Settings.hpp>
#include <src/PowerUp.hpp>

PowerUp::PowerUp(float _x, float _y) noexcept
    : x{_x}, y{_y}, sprite{Settings::textures["potion"]}
{

}

sf::FloatRect PowerUp::get_collision_rect() const noexcept
{
    return sf::FloatRect{x, y, Settings::POTION_WIDTH, Settings::POTION_HEIGHT};
}

bool PowerUp::is_out_of_game() const noexcept
{
    return x < -Settings::POTION_WIDTH;
}

void PowerUp::update(float dt) noexcept
{
    x += -Settings::MAIN_SCROLL_SPEED * dt;
    sprite.setPosition(x, y);
}

void PowerUp::render(sf::RenderTarget& target) const noexcept
{
    target.draw(sprite);
}

void PowerUp::reset(float _x, float _y) noexcept
{
    x = _x;
    y = _y;
}