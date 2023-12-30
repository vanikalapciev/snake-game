from tkinter import *
import random

BOARD_SIZE = 20
PIXEL_SIZE = 20
SNAKE_SIZE = 3
BOARD_COLOR = "#000000"
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
SPEED = 200

score = 0
direction = "down"


def draw_square(x, y) -> None:
    x = x * PIXEL_SIZE
    y = y * PIXEL_SIZE
    board.create_rectangle(x, y, x + PIXEL_SIZE, y + PIXEL_SIZE, fill=SNAKE_COLOR, tags="snake")


def delete_square(x, y) -> None:
    x = x * PIXEL_SIZE
    y = y * PIXEL_SIZE
    item_id = board.find_closest(x + PIXEL_SIZE // 2, y + PIXEL_SIZE // 2)
    board.delete(item_id)


def draw_food(x, y) -> None:
    x = x * PIXEL_SIZE
    y = y * PIXEL_SIZE
    board.create_oval(x, y, x + PIXEL_SIZE, y + PIXEL_SIZE, fill=FOOD_COLOR, tags="food")


def check_collision(snake_coordinates):
    seen_pairs = set()
    for coord in snake_coordinates:
        pair = tuple(coord)
        if pair in seen_pairs or any(coord < 0 or coord >= BOARD_SIZE for coord in coord):
            return True
        seen_pairs.add(pair)
    return False


class Snake:

    def __init__(self):
        self.coordinates = []

        for i in range(0, SNAKE_SIZE):
            self.coordinates.append([0, i])
            draw_square(0, i)


class Food:
    coordinates = []

    def __init__(self, snake_coordinates):
        while True:
            x = random.randint(1, (BOARD_SIZE - 2))
            y = random.randint(1, (BOARD_SIZE - 2))
            if [x, y] not in snake_coordinates:
                break

        self.coordinates.append([x, y])
        draw_food(x, y)


def next_step(snake, food):
    if check_collision(snake.coordinates):
        game_over()
    else:
        x, y = snake.coordinates[-1]

        if direction == "up":
            y -= 1
        elif direction == "down":
            y += 1
        elif direction == "right":
            x += 1
        elif direction == "left":
            x -= 1

        snake.coordinates.append([x, y])

        if food.coordinates[-1] == snake.coordinates[-1]:
            delete_square(food.coordinates[-1][0], food.coordinates[-1][1])
            Food(snake.coordinates)
            update_score()
        else:
            delete_square(snake.coordinates[0][0], snake.coordinates[0][1])
            del snake.coordinates[0]

        draw_square(x, y)
        window.after(SPEED, next_step, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction


def update_score():
    global score
    global SPEED
    score += 1
    if score % 10 == 0:
        SPEED = int(SPEED * 0.9)
    label.config(text="Score: {}".format(score))


def game_over():
    board.delete(ALL)
    board.create_text(
        board.winfo_width() / 2, board.winfo_height() / 2, font=('consolas', 70),
        text=f"Game Over\nScore: {score}", fill="red",
    )


if __name__ == '__main__':
    window = Tk()
    window.resizable(False, False)

    label = Label(window, text="Score: {}".format(score), font=('consolas', 42))
    label.pack()

    board = Canvas(window, background=BOARD_COLOR, width=BOARD_SIZE * PIXEL_SIZE, height=BOARD_SIZE * PIXEL_SIZE)
    board.pack()

    window.bind('<Left>', lambda event: change_direction("left"))
    window.bind('<Right>', lambda event: change_direction("right"))
    window.bind('<Up>', lambda event: change_direction("up"))
    window.bind('<Down>', lambda event: change_direction("down"))

    snake = Snake()
    food = Food(snake.coordinates)
    next_step(snake, food)

    window.mainloop()
