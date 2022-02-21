# Basic arcade shooter

# Imports
import arcade
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Arcade Space Shooter"
SCALING = 2.0























class SpaceShooter(arcade.Window):
    """Space Shooter side scroller game
    Player starts on the left, enemies appear on the right
    Player can move anywhere, but not off screen
    Enemies fly to the left at variable speed
    Collisions end the game
    """

    def __init__(self, width, height, title):
        """Initialize the game
        """
        super().__init__(width, height, title)

        # Set up the empty sprite lists
        self.enemies_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

def setup(self):
    """Get the game ready to play
    """

    # Set the background color
    arcade.set_background_color(arcade.color.SKY_BLUE)

    # Set up the player
    self.player = arcade.Sprite("images/jet.png", SCALING)
    self.player.center_y = self.height / 2
    self.player.left = 10
    self.all_sprites.append(self.player)