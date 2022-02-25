# Basic arcade shooter

# Imports
from pickle import FALSE
from turtle import right
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Space Shooter"
SCALING = 1.0

class FlyingSprite(arcade.Sprite):
    """Base class for all flying sprites
    Flying sprites include enemies and clouds"""

    def update(self):
        """Update the position of the sprite
        When it moves off screen to the left, remove it"""

        # Move the sprite
        super().update()

        # Remove if off the screen
        if self.right < 0:
            self.remove_from_sprite_lists()


class SpaceShooter(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game"""

    def __init__(self, width, height, title):
        """Initialize the game"""
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        """Get the game ready to play"""

        # Set the background color
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Set up the player
        self.player = arcade.Sprite("images/jet.png", SCALING)
        self.player.center_y = self.height / 2
        self.player.left = 10
        self.all_sprites.append(self.player)
        self.player_speed = 250
        self.right = False
        self.left = False
        self.up = False
        self.down = False

        # Spawn a new enemy every 0.25 seconds
        arcade.schedule(self.add_enemy, 0.25)

        # Spawn a new cloud every second
        arcade.schedule(self.add_cloud, 1.0)

        # Load your background music
        # Sound source: http://ccmixter.org/files/Apoxode/59262
        # License: https://creativecommons.org/licenses/by/3.0/
        self.background_music = arcade.load_sound(
            "sounds/Apoxode_-_Electric_1.wav"
        )

        # Load your sounds
        # Sound sources: Jon Fincher
        self.collision_sound = arcade.load_sound("sounds/Collision.wav")
        self.move_up_sound = arcade.load_sound("sounds/Rising_putter.wav")
        self.move_down_sound = arcade.load_sound("sounds/Falling_putter.wav")

        self.paused = False

    def add_enemy(self, delta_time: float):
        """Adds a new enemy to the screen
        
        Arguments:
            delta_time {float} -- How much time has pass since the last call"""

        # First, create the new enemy sprite
        enemy = FlyingSprite("images/missile.png", SCALING)

        # Set its position to a random height and off screen right
        enemy.left = random.randint(self.width, self.width + 80)
        enemy.top = random.randint(10, self.height - 10)

        # Set its speed to a random speed heading left
        enemy.velocity = (random.randint(-100, -50), 0)

        # Add it to the enemies list
        self.enemies_list.append(enemy)
        self.all_sprites.append(enemy)

    def add_cloud(self, delta_time: float):
        """Adds a new cloud to the screen
        
        Arguments:
            delta_time {float} -- How much time has passed since the last call"""
        # First, create the new cloud sprite
        cloud = FlyingSprite("images/cloud.png", SCALING)

        # Set its position to a random height and off screen right
        cloud.left = random.randint(self.width, self.width + 80)
        cloud.top = random.randint(10, self.height - 10)

        # Set its speed to a random speed heading left
        cloud.velocity = (random.randint(-100, -20), 0)

        # Add it to the enemies list
        self.clouds_list.append(cloud)
        self.all_sprites.append(cloud)

    def on_key_press(self, symbol, modifiers):
        """Handle user keyboard input
        Esc: Quit the game
        Space: Pause/Unpause the game
        W/A/S/D: Move up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right
        
        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed"""
        if symbol == arcade.key.ESCAPE:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.SPACE:
            self.paused = not self.paused
        
        if (symbol == arcade.key.W or symbol == arcade.key.UP):
            self.up = True
            arcade.play_sound(self.move_up_sound)

        if (symbol == arcade.key.S or symbol == arcade.key.DOWN):
            self.down = True
            arcade.play_sound(self.move_down_sound)

        if (symbol == arcade.key.A or symbol == arcade.key.LEFT):
            self.left = True

        if (symbol == arcade.key.D or symbol == arcade.key.RIGHT):
            self.right = True

        # if symbol == arcade.key.W or symbol == arcade.key.UP:
        #     self.player.change_y = 100
        #     arcade.play_sound(self.move_up_sound)
        
        # if symbol == arcade.key.S or symbol == arcade.key.DOWN:
        #     self.player.change_y = -50  
        #     arcade.play_sound(self.move_down_sound)

        # if symbol == arcade.key.A or symbol == arcade.key.LEFT:
        #     self.player.change_x = -50
        
        # if symbol == arcade.key.D or symbol == arcade.key.RIGHT:
        #     self.player.change_x = 100

    def on_key_release(self, symbol: int, modifiers: int):
        """"Undo movement vectors when movement keys are released
        
        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed"""

        if (symbol == arcade.key.W or arcade.key.UP):
            self.up = False

        if (symbol == arcade.key.S or arcade.key.DOWN):
            self.down = False

        if (symbol == arcade.key.A or arcade.key.LEFT) and self.right == True:
            self.right = True

        elif (symbol == arcade.key.A or arcade.key.LEFT):
            self.left = False

        if (symbol == arcade.key.D or arcade.key.RIGHT) and self.left == True:
            self.left = True

        elif (symbol == arcade.key.D or arcade.key.RIGHT) and self.left == False:
            self.right = False

        # if (symbol == arcade.key.W or
        #     symbol == arcade.key.UP or
        #     symbol == arcade.key.S or
        #     symbol == arcade.key.DOWN
        # ):
        #     self.player.change_y = 0

        # if (symbol == arcade.key.A or
        #     symbol == arcade.key.LEFT or
        #     symbol == arcade.key.D or
        #     symbol == arcade.key.RIGHT
        # ):
        #     self.player.change_x = 0

    def on_update(self, delta_time: float):
        """Update the positions and statuses of all game objects
        If paused, do nothing

        Arguments:
            delta_time {float} -- Time since the last update"""

        # If paused don't update anything
        if self.paused:
            return
        # Did you hit anything? If so, end the game
        if len(self.player.collides_with_list(self.enemies_list)) > 0:
            arcade.play_sound(self.collision_sound)
            arcade.close_window()

        if self.right == True or self.left == False:
            self.player.change_x += self.player_speed * delta_time

        if self.left == True or self.right == False:
            self.player.change_x -= self.player_speed * delta_time
        
        if self.up == True or self.down == False:
            self.player.change_y += self.player_speed * delta_time

        if self.down == True or self.up == False:
            self.player.change_y -= self.player_speed * delta_time

        if self.left == False and self.right == False:
            self.player.change_x = 0
        
        if self.up == False and self.down == False:
            self.player.change_y = 0

        if self.left == True and self.right == True:
            self.player.change_x = 0
        
        if self.up == True and self.down == True:
            self.player.change_y = 0

        # Update everything
        for sprite in self.all_sprites:
            sprite.center_x = int(
                sprite.center_x + sprite.change_x * delta_time)
            sprite.center_y = int(
                sprite.center_y + sprite.change_y * delta_time
            )

        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_draw(self):
        """Draw all game objects"""
        arcade.start_render()
        self.all_sprites.draw()

if __name__ == "__main__":
    # Create a new Space Shooter window
    space_game = SpaceShooter(
        int(SCREEN_WIDTH * SCALING), int(SCREEN_HEIGHT * SCALING), SCREEN_TITLE
    )
    # Setup to play
    space_game.setup()
    # Run the game
    arcade.run()