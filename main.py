import pickle
from random import randint

import pyglet as pg

from os import getcwd

cur_path = getcwd()

pg.resource.path = [cur_path]
pg.resource.reindex()


class Start_menu(pg.window.Window):
    def __init__(self):
        super(Start_menu, self).__init__(1102, 700, caption='Змейка')

        # add font
        pg.font.add_file("fonts/Segoe Print.ttf")

        self.menu_fon = pg.image.load('images/menu/fon_menu.png')  # Background picture

        # Method for drawing
        self.menu_batch = pg.graphics.Batch()

        # Title inscription
        self.header_img = pg.image.load('images/menu/title.png')
        self.header = pg.sprite.Sprite(img=self.header_img, x=550, y=520, batch=self.menu_batch)

        # play inscription
        self.but_pos_x = 110
        self.butplay_pos_y = 290
        self.button_play_img = [pg.resource.image('images/menu/play_button.png'),  # image for animation
                                pg.resource.image('images/menu/play_button_1.png')]
        self.button_play_an = pg.image.Animation.from_image_sequence(sequence=self.button_play_img,
                                                                     duration=0.25)  # animation
        self.button_play = pg.sprite.Sprite(img=self.button_play_an, x=self.but_pos_x, y=self.butplay_pos_y,
                                            batch=self.menu_batch)

        # leaderboard inscription
        self.butleader_pos_y = 68
        self.leaderboard_img = pg.image.load('images/menu/table_button.png')
        self.button_table = pg.sprite.Sprite(img=self.leaderboard_img, x=self.but_pos_x, y=self.butleader_pos_y,
                                             batch=self.menu_batch)

    # Rendering
    def on_draw(self):
        self.clear()
        self.menu_fon.blit(0, 0)  # image fonts
        self.menu_batch.draw()

    # events press button
    def on_mouse_press(self, x, y, button, modifiers):
        if (button == pg.window.mouse.LEFT and self.but_pos_x + 15 <= x <= self.but_pos_x + 440 and
                self.butplay_pos_y + 30 <= y <= self.butplay_pos_y + 170):
            window = The_game()
            window.set_location(200, 100)
            self.close()
            pg.app.run()

        if (button == pg.window.mouse.LEFT and self.but_pos_x + 15 <= x <= self.but_pos_x + 440 and
                self.butleader_pos_y + 30 <= y <= self.butleader_pos_y + 170):
            window = Leader_board()
            window.set_location(200, 100)
            self.close()
            pg.app.run()

class Leader_board(pg.window.Window):
    def __init__(self):
        super(Leader_board, self).__init__(1102, 700, caption='Змейка')
        self.leaderboard_fon = pg.image.load('images/leaderboard/fon_leaderboard.png')  # background fill

        self.batch_leader = pg.graphics.Batch()  # Method for drawing
        self.batch_leader_text = pg.graphics.Batch()

        # Exit inscription
        self.exit_img_w = pg.image.load('images/exit_white.png')  # white
        self.exit_img_r = pg.image.load('images/exit.png')  # red
        self.exit = pg.sprite.Sprite(img=self.exit_img_w, x=1010, y=605, batch=self.batch_leader)

        # Title inscription
        self.title_text_img = pg.image.load('images/leaderboard/title_leaderboard.png')
        self.title_text = pg.sprite.Sprite(img=self.title_text_img, x=180, y=587, batch=self.batch_leader)

        # Table leaderboard
        self.table_img = pg.image.load('images/leaderboard/table_leaderboard.png')
        self.title = pg.sprite.Sprite(img=self.table_img, x=181, y=60, batch=self.batch_leader)

        # the color of the text that will be used to write labels in the leaderboard
        self.text_color = (255, 250, 255, 255)

        # loading leaderboard from file
        self.f = open('leaderboards.data', 'rb+')
        self.players = pickle.load(self.f)
        self.leaders_and_points(245, 375, self.players['player_1'][0],
                                self.batch_leader_text, self.text_color)  # name player 1
        self.leaders_and_points(245, 305, self.players['player_2'][0],
                                self.batch_leader_text, self.text_color)  # name player 2
        self.leaders_and_points(245, 235, self.players['player_3'][0],
                                self.batch_leader_text, self.text_color)  # name player 3
        self.leaders_and_points(245, 165, self.players['player_4'][0],
                                self.batch_leader_text, self.text_color)  # name player 4
        self.leaders_and_points(245, 105, self.players['player_5'][0],
                                self.batch_leader_text, self.text_color)  # name player 5

        self.leaders_and_points(880, 375, str(self.players['player_1'][1]),
                                self.batch_leader_text, self.text_color, 'right')  # points player 1
        self.leaders_and_points(880, 305, str(self.players['player_2'][1]),
                                self.batch_leader_text, self.text_color, 'right')  # points player 2
        self.leaders_and_points(880, 235, str(self.players['player_3'][1]),
                                self.batch_leader_text, self.text_color, 'right')  # points player 3
        self.leaders_and_points(880, 165, str(self.players['player_4'][1]),
                                self.batch_leader_text, self.text_color, 'right')  # points player 4
        self.leaders_and_points(880, 105, str(self.players['player_5'][1]),
                                self.batch_leader_text, self.text_color, 'right')  # points player 5
        self.f.close()

    def on_draw(self):
        self.clear()
        self.leaderboard_fon.blit(x=0, y=0)
        self.batch_leader.draw()
        self.batch_leader_text.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        if 1017 <= x <= 1086 and 610 <= y <= 670:
            self.exit.image = self.exit_img_r  # red
        else:
            self.exit.image = self.exit_img_w  # white

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pg.window.mouse.LEFT and 1028 <= x <= 1086 and 610 <= y <= 670:
            window = Start_menu()
            window.set_location(200, 100)
            self.close()
            pg.app.run()

    # creates an inscription at the specified coordinates and color
    @staticmethod
    def leaders_and_points(x, y, text, method, color, anchor='left'):
        pg.text.Label(text,
                      font_name='Segoe Print',
                      font_size=30,
                      color=color,
                      x=x, y=y,
                      batch=method,
                      anchor_x=anchor)

class Snake():
    def spawn_head(self, x, y, batch, side=40):
        # load head image and create sprite
        self.head_snake_img = pg.image.load('images/the_game/head_snake_1.png')
        self.head_snake_img.anchor_x = side // 2  # center snap to rotate the sprite correctly
        self.head_snake_img.anchor_y = side // 2
        self.head_snake = pg.sprite.Sprite(img=self.head_snake_img, x=x, y=y, batch=batch)
        self.head_snake.update(rotation=180)  # 180 degree turn
        return self.head_snake

    def spawn_part(self, x, y, batch, side=40):
        # two parts the snake
        self.section_snake_img = pg.image.load('images/the_game/snake_section_1.png')
        self.section_snake_img.anchor_x = side // 2  # center snap to rotate the sprite correctly
        self.section_snake_img.anchor_y = side // 2
        return pg.sprite.Sprite(img=self.section_snake_img, x=x, y=y , batch=batch)

    def motion(self, head, snake, change_x, change_y):
        for i in range(len(snake) - 1, 0, -1):  # loop iterates sections of the snake from the tail
            # move the section to the place of the previous section
            snake[i].x = snake[i - 1].x
            snake[i].y = snake[i - 1].y

        # moving snake hed
        head.x += change_x
        head.y += change_y

        # if the snake goes out of bounds, then it crawls out on the other side
        if head.x > 1102:
            head.x = 19
        elif head.x < 0:
            head.x = 1083
        elif head.y > 608:
            head.y = 19
        elif head.y < 0:
            head.y = 589

class Obstacles():
    position = []  # here are the coordinates of all the stones and apples

    def __init__(self):
        The_game.__init__(self)

    def spawn(self, change, img, place):
        # a place is selected where there are no stones or apples yet and on the trajectory of the snake
        self.pos_x = randint(0, 28) * change
        self.pos_y = randint(0, 14) * change
        while (self.pos_x, self.pos_y) in Obstacles.position:
            self.pos_x = randint(0, 28) * change
            self.pos_y = randint(0, 14) * change
        # adding a position to the list
        Obstacles.position.insert(place, (self.pos_x + change // 2, self.pos_y + change // 2))
        return pg.sprite.Sprite(img, x=self.pos_x, y=self.pos_y, batch=self.batch_obstacles)

class Apple(Obstacles):
    # uploading an apple image
    apple_img = pg.image.load('images/the_game/apple.png')
    apple_img.anchor_x = 1

    def __init__(self):
        Obstacles.__init__(self)

    # we use the method to spawn obstacles
    def spawn(self):
        return Obstacles.spawn(self, self.change, Apple.apple_img, 0)

class Stone(Obstacles):
    # uploading a stone image
    stone_img = pg.image.load('images/the_game/stone.png')

    def __init__(self):
        Obstacles.__init__(self)

    # we use the method to spawn obstacles
    def spawn(self):
        return Obstacles.spawn(self, self.change, Stone.stone_img, 1)

class The_game(pg.window.Window):
    def __init__(self):
        super(The_game, self).__init__(1102, 700, caption='Змейка')

        self.the_game_fon = pg.image.load('images/the_game/fon_the_game.png')  # background fill
        self.the_game_hat = pg.image.load('images/the_game/hat_game.png')

        self.side = 40  # size snake

        self.batch_snake = pg.graphics.Batch()  # Method for drawing
        self.batch_text = pg.graphics.Batch()
        self.batch_obstacles = pg.graphics.Batch()
        self.batch_game_end = pg.graphics.Batch()
        self.batch_game_end_enter = pg.graphics.Batch()
        self.batch_stars = pg.graphics.Batch()

        # Score inscription
        self.points = pg.text.Label('Очки:',
                                    font_name='Segoe Print',
                                    font_size=63,
                                    color=(140, 249, 199, 255),
                                    x=8, y=625,
                                    batch=self.batch_text)

        # Exit inscription
        self.exit_img_w = pg.image.load('images/exit_white.png')  # white
        self.exit_img_r = pg.image.load('images/exit.png')  # red
        self.exit = pg.sprite.Sprite(img=self.exit_img_w, x=980, y=612, batch=self.batch_text)

        # leaderboard inscription
        self.text_leaderboard_img = pg.image.load('images/the_game/leaderboard_insc.png')
        self.text_leaderboard = pg.sprite.Sprite(img=self.text_leaderboard_img, x=465, y=605, batch=self.batch_text)

        self.points_counters = 0  # counts how many apples the snake ate
        # derivation of points
        self.text_points_counters = pg.text.Label(str(self.points_counters),
                                                  font_name='Segoe Print',
                                                  font_size=45,
                                                  color=(255, 255, 255, 255),
                                                  x=280, y=627)

        # snake locomotion
        self.change = 38
        self.change_x = 0
        self.change_y = -self.change

        # snake
        self.start_pos_x, self.start_pos_y = 589, 285
        self.head_snake = Snake.spawn_head(self, self.start_pos_x, self.start_pos_y, self.batch_snake)
        self.the_snake = [self.head_snake] # list with all parts of the snake
        self.the_snake.append(Snake.spawn_part(self, self.start_pos_x, self.start_pos_y + self.side - 2, self.batch_snake))
        self.the_snake.append(Snake.spawn_part(self, self.start_pos_x, self.start_pos_y + (self.side - 2) * 2, self.batch_snake))

        # a list with all the stones
        self.stones = []

        # the indicator of cutting into the stone
        self.crash = False

        # to end the game
        self.game_end_fon_img = pg.image.load('images/the_game/game_end_fon.png')
        self.entering_name_img = pg.image.load('images/the_game/entering_name.png')
        self.snake_end_img = pg.image.load('images/the_game/snake_the_end.png')
        self.stars_ani = pg.resource.animation('images/the_game/stars.gif')

        # sounds
        self.sound_eat = pg.media.load('sounds/eat.wav', streaming=False)
        self.sound_crash = pg.media.load('sounds/crash.wav', streaming=False)

        # loading leaderboard from file
        with open('leaderboards.data', 'rb+') as self.f:
            self.players = pickle.load(self.f)

        # name in case of winning
        self.name_text = ''

        self.bool_input = False  # check if name entry is enabled

        self.game_over = False  # checking if the snake has crashed

        self.apple_counter = 0  # checks if there are apples in the field

        pg.clock.schedule_interval(self.update, .25)  # update window

    def on_draw(self):
        self.clear()
        self.the_game_fon.blit(0, 0)
        self.batch_obstacles.draw()  # so that the snake is on top of the apple
        self.batch_snake.draw()
        self.the_game_hat.blit(0, 600)
        self.batch_game_end.draw()
        self.batch_game_end_enter.draw()
        self.text_points_counters.draw()
        self.batch_text.draw()
        self.batch_stars.draw()

    # a function that updates the values in the leaderboard
    @staticmethod
    def update_leaderboard(player, name, points):
        f = open('leaderboards.data', 'rb')
        players = pickle.load(f)  # download initial values
        f.close()

        # change table values
        players[player][0] = name
        players[player][1] = points

        # upload back to file
        f = open('leaderboards.data', 'wb')
        pickle.dump(players, f)
        f.close()

    # decorations
    def on_mouse_motion(self, x, y, dx, dy):
        if 985 <= x <= 1050 and 620 <= y <= 680:
            self.exit.image = self.exit_img_r
            window.set_mouse_cursor(window.get_system_mouse_cursor(window.CURSOR_HAND))
        else:
            self.exit.image = self.exit_img_w
            window.set_mouse_cursor()

        if 465 <= x <= 883 and 633 <= y <= 676:
            window.set_mouse_cursor(window.get_system_mouse_cursor(window.CURSOR_HAND))
        else:
            window.set_mouse_cursor()

    def on_mouse_press(self, x, y, button, modifiers):
        # exit from the game
        if button == pg.window.mouse.LEFT and 985 <= x <= 1050 and 620 <= y <= 680:
            window = Start_menu()
            window.set_location(200, 100)
            self.close()
            pg.app.run()

        # see leaderboard
        if button == pg.window.mouse.LEFT and 465 <= x <= 883 and 633 <= y <= 676:
            window = Leader_board()
            window.set_location(200, 100)
            self.close()
            pg.app.run()

    # change the movement of the snake through the keyboard
    def on_key_press(self, symbol, modifiers):
        if symbol == pg.window.key.LEFT and self.change_x == 0:
            self.change_x = -self.change
            self.change_y = 0
            self.head_snake.update(rotation=270)  # turn in the right direction, left
        elif symbol == pg.window.key.RIGHT and self.change_x == 0:
            self.change_x = self.change
            self.change_y = 0
            self.head_snake.update(rotation=90)  # turn in the right direction, right
        elif symbol == pg.window.key.DOWN and self.change_y == 0:
            self.change_x = 0
            self.change_y = -self.change
            self.head_snake.update(rotation=180)  # turn in the right direction, down
        elif symbol == pg.window.key.UP and self.change_y == 0:
            self.change_x = 0
            self.change_y = self.change
            self.head_snake.update(rotation=0)  # turn in the right direction, up

        # restart game
        if self.game_over and symbol == pg.window.key.SPACE and not self.bool_input:

            Obstacles.position.clear()  # clear the stones
            self.stones.clear()
            del self.apple

            self.the_snake = self.the_snake[:2] + [self.the_snake[-1]]  # return the initial snake

            # return the snake to its starting position
            self.head_snake.x, self.head_snake.y = self.start_pos_x, self.start_pos_y
            self.head_snake.update(rotation=180)
            for i in range(1, len(self.the_snake)):  # loop iterates sections of the snake from the tail
                self.the_snake[i].x = self.the_snake[i - 1].x
                self.the_snake[i].y = self.the_snake[i - 1].y + 40

            self.game_end_fon.delete()  # clears the inscription about the loss
            self.text_hint_s.delete()
            self.stars.delete()
            self.snake_end.delete()

            self.points_counters = 0  # return zero points
            self.text_points_counters = pg.text.Label(str(self.points_counters),
                                                      font_name='Segoe Print',
                                                      font_size=45,
                                                      color=(255, 255, 255, 255),
                                                      x=300, y=627)

            # set initial values
            self.change_x = 0
            self.change_y = -self.change

            # name in case of winning
            self.name_text = ''

            self.crash = False
            self.game_over = False

        # the ability to delete the entered name
        if self.bool_input and symbol == pg.window.key.BACKSPACE:
            self.name_text = self.name_text[:-1]

        # if the player presses "enter" then the entered name is saved and can no longer be changed
        if self.bool_input and symbol == pg.window.key.ENTER:
            self.name.delete()
            self.text_hint_e.delete()

            self.window.delete()
            del self.window
            self.bool_input = False

    def on_text(self, text):
        # if an input window is open, then add to the name any text entered from the keyboard,
        # not exceeding the maximum length of the name
        if self.bool_input and len(self.name_text) <= 20:
            self.name_text += text

    def update(self, dt):  # updates the playing field
        if not self.game_over:
            Snake.motion(self, self.head_snake, self.the_snake, self.change_x, self.change_y)

            # spawn an apple if necessary
            if self.apple_counter == 0:

                # spawn a stone if necessary
                if self.points_counters % 5 == 0 and self.points_counters > 0:
                    self.stones.append(Stone.spawn(self))

                # spawn an apple
                self.apple = Apple.spawn(self)
                self.apple_counter += 1  # informs that there is an apple on the field

            # checking if the snake has eaten the apple
            if (self.apple.x <= self.head_snake.x <= self.apple.x + self.side and
                    self.apple.y <= self.head_snake.y <= self.apple.y + self.side):
                # the sound of eating
                self.sound_eat.play()

                # if the snake ate an apple, then a new apple is generated, because apple counter becomes 0
                self.apple_counter -= 1
                Obstacles.position = Obstacles.position[1:]
                del self.apple

                # add snake section
                # adds 1 snake section in front of the tail
                self.the_snake.insert(-1, Snake.spawn_part(self, self.the_snake[-2].x, self.the_snake[-2].y, self.batch_snake))
                # center snap to move properly behind the head
                self.the_snake[-2].anchor_x = self.side // 2
                self.the_snake[-2].anchor_y = self.side // 2

                # add point
                self.points_counters += 1
                # derivation of points
                self.text_points_counters = pg.text.Label(str(self.points_counters),
                                                          font_name='Segoe Print',
                                                          font_size=45,
                                                          color=(255, 255, 255, 255),
                                                          x=300, y=627)

            for (x, y) in Obstacles.position:
                if x == self.head_snake.x and y == self.head_snake.y:
                    self.crash = True
                    break

            for section in self.the_snake[1:]:  # iterate over the sections of the snake
                # if the snake collides with some part of itself, then the game ends
                if self.crash or section.x == self.head_snake.x and section.y == self.head_snake.y:
                    # the sound of crash
                    self.sound_crash.play()

                    # updating the apple counter
                    self.apple_counter = 0

                    # area for an inscription about the loss
                    self.game_end_fon = pg.sprite.Sprite(img=self.game_end_fon_img, x=221, y=110,
                                                         batch=self.batch_game_end)

                    self.game_over = True
                    break
        else:
            # check if the player has overtaken someone from the leaderboard
            # we go in ascending order and if the chain is interrupted,
            # then we update the player who was overtaken last
            if self.points_counters > self.players['player_5'][1]:
                if self.name_text == '':
                    self.bool_input = True  # check if name entry is enabled

                if self.bool_input:

                    # field for entering a name player and name suggestion
                    self.window = pg.sprite.Sprite(img=self.entering_name_img, x=347, y=230,
                                                   batch=self.batch_game_end_enter)

                    # check if the name is entered, then clear it to make changes
                    try:
                        self.text_hint_e.delete()
                        self.name.delete()
                    except AttributeError:
                        pass

                    self.text_hint_e = pg.text.Label('<ENTER>',
                                                     font_size=15,
                                                     color=(255, 255, 255, 120),
                                                     x=551, y=130, anchor_x='center',
                                                     batch=self.batch_text)

                    # entered name
                    self.name = pg.text.Label(self.name_text,
                                              font_name='Typometry_Regular',
                                              font_size=25,
                                              color=(0, 0, 0, 255),
                                              x=551, y=246, anchor_x='center',
                                              batch=self.batch_text)
                else:
                    # update leaderboard
                    self.name_player = 'player_'
                    self.player_number = 5
                    while self.points_counters > self.players[self.name_player + str(self.player_number)][1] and self.player_number > 0:
                        self.player_number -= 1
                    else:
                        self.player_number += 1
                        self.update_leaderboard(self.name_player + str(self.player_number), self.name_text, self.points_counters)

            if not self.bool_input:
                # clear window
                try:
                    self.snake_end.delete()
                    self.stars.delete()
                    self.text_hint_s.delete()
                except AttributeError:
                    pass

                self.text_hint_s = pg.text.Label('<SPACE>',
                                                 font_size=15,
                                                 color=(255, 255, 255, 120),
                                                 x=551, y=130, anchor_x='center',
                                                 batch=self.batch_text)
                self.snake_end = pg.sprite.Sprite(img=self.snake_end_img, x=473, y=183, batch=self.batch_text)
                self.stars = pg.sprite.Sprite(img=self.stars_ani, x=473, y=270, batch=self.batch_stars)


if __name__ == '__main__':
    window = Start_menu()
    window.set_location(200, 100)
    pg.app.run()
