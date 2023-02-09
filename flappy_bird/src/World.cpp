/*
    ISPPJ1 2023
    Study Case: Flappy Bird

    Author: Alejandro Mujica
    alejandro.j.mujic4@gmail.com

    This file contains the definition of the class World.
*/

#include <Settings.hpp>
#include <src/World.hpp>
#include <cstdlib> // para los numeros aleatorios
#include <ctime> // uso del reloj para los numeros aleatorios

World::World(bool _generate_logs) noexcept
    : generate_logs{_generate_logs}, background{Settings::textures["background"]}, ground{Settings::textures["ground"]},
      logs{}, rng{std::default_random_engine{}()}
{
    ground.setPosition(0, Settings::VIRTUAL_HEIGHT - Settings::GROUND_HEIGHT);
    std::uniform_int_distribution<int> dist(0, 80);
    last_log_y = -Settings::LOG_HEIGHT + dist(rng) + 20;
}

void World::reset(bool _generate_logs) noexcept
{
    generate_logs = _generate_logs;
    powerUp_taken = false;
}

bool World::collides(const sf::FloatRect& rect, bool bird_invisible) const noexcept
{
    if (rect.top + rect.height >= Settings::VIRTUAL_HEIGHT)
    {
        return true;
    }
    
    if (!bird_invisible)
    {
        for (auto log_pair: logs)
        {
            if (log_pair->collides(rect))
            {
                return true;
            }
        }
    }

    return false;
}

bool World::collides_with_powerUp(const sf::FloatRect& rect) noexcept
{
    if (powerUp == nullptr)
    {
        return false;
    }

    powerUp_taken = powerUp->get_collision_rect().intersects(rect);

    return powerUp_taken;
}

bool World::update_scored(const sf::FloatRect& rect) noexcept
{
    for (auto log_pair: logs)
    {
        if (log_pair->update_scored(rect))
        {
            return true;
        }
    }

    return false;
}

void World::update(float dt, bool hardmode) noexcept
{   
    if (hardmode) 
    {
        if (generate_logs)
        {
            logs_spawn_timer += dt;
            powerUp_spawn_timer += dt;

            if (logs_spawn_timer >= Settings::TIME_TO_SPAWN_LOGS)
            {
                logs_spawn_timer = 0.f;
                int num = (rand()%40)+10, inf = 10, sup=90;
                std::uniform_int_distribution<int> dist{-30, 30};
                std::uniform_int_distribution<int> dist_x{0, (int)Settings::LOG_WIDTH};

                float y = std::max(-Settings::LOG_HEIGHT + (rand()%sup)+inf, std::min(last_log_y + dist (rng), Settings::VIRTUAL_HEIGHT + (rand()%sup)+inf - Settings::LOG_HEIGHT));
                float x = Settings::VIRTUAL_WIDTH + dist_x(rng);
                float gap = Settings::LOGS_GAP;
                //aplica un rango para los numeros aleateorios, dependiendo de los ultimos valores
                    
                    if(last_log_y > y){
                        std::cout<<"\nif1";
                        if((last_log_y+y)/-last_log_y > 0.3){
                            inf = last_log_y * 1.3;
                            sup = last_log_y;
                        }
                        else{
                            sup = last_log_y * 1.3;
                            inf = last_log_y;
                        }
                    }
                    else if(last_log_y < y){
                        std::cout<<"\nif2";
                        if((last_log_y+y)/-y > 0.3){
                            sup= y* 1.3;
                            inf = y;
                        }
                        else{
                            inf = y * 1.3;
                            sup = y;
                        }
                    }
                    
                last_log_y = y;

                logs.push_back(log_factory.create(x, y, gap));
            }
            
            if (powerUp_spawn_timer >= Settings::TIME_TO_SPAWN_POTION)
            {
                powerUp_spawn_timer = 0.f;
                std::uniform_int_distribution<int> powerUp_dist{(int)Settings::POTION_HEIGHT, (int)Settings::VIRTUAL_HEIGHT - (int)Settings::POTION_HEIGHT};

                float y = powerUp_dist(rng);

                powerUp = powerUp_factory.create(Settings::VIRTUAL_WIDTH, y);
            }
        }    
    }
    else 
    {
        if (generate_logs)
        {
            logs_spawn_timer += dt;

            if (logs_spawn_timer >= Settings::TIME_TO_SPAWN_LOGS)
            {
                logs_spawn_timer = 0.f;

                std::uniform_int_distribution<int> dist{-20, 20};
                float y = std::max(-Settings::LOG_HEIGHT + 10, std::min(last_log_y + dist(rng), Settings::VIRTUAL_HEIGHT + 90 - Settings::LOG_HEIGHT));

                last_log_y = y;

                logs.push_back(log_factory.create(Settings::VIRTUAL_WIDTH, y));
            }
        }
    }
    background_x += -Settings::BACK_SCROLL_SPEED * dt;

    if (background_x <= -Settings::BACKGROUND_LOOPING_POINT)
    {
        background_x = 0;
    }

    background.setPosition(background_x, 0);

    ground_x += -Settings::MAIN_SCROLL_SPEED * dt;

    if (ground_x <= -Settings::VIRTUAL_WIDTH)
    {
        ground_x = 0;
    }

    ground.setPosition(ground_x, Settings::VIRTUAL_HEIGHT - Settings::GROUND_HEIGHT);

    for (auto it = logs.begin(); it != logs.end(); )
    {
        if ((*it)->is_out_of_game())
        {
            auto log_pair = *it;
            log_factory.remove(log_pair);
            it = logs.erase(it);
            
        }
        else
        {
            (*it)->update(dt);
            ++it;
        }
    }

    if (powerUp) 
    {
        if (powerUp->is_out_of_game() or powerUp_taken) 
        {
            powerUp_factory.remove(powerUp);
            powerUp.reset();
        }
        else 
        {
            powerUp->update(dt);
        }
    }
}

void World::render(sf::RenderTarget& target) const noexcept
{
    target.draw(background);

    for (const auto& log_pair: logs)
    {
        log_pair->render(target);
    }

    target.draw(ground);

    if (powerUp and !powerUp_taken) 
    {
        powerUp->render(target);
    }
}