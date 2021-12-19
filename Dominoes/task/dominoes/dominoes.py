# Write your code here
import random

NUM_STOCK = 14
NUM_COMPUTER = 7
NUM_PLAYER = 7

stock_pieces = []
computer_pieces = []
player_pieces = []
domino_snake = []
status = ''

STATUS_PLAYER_TURN = 'player'
STATUS_COMPUTER_TURN = 'computer'
STATUS_COMPUTER_WIN = 'computer_win'
STATUS_PLAYER_WIN = 'player_win'
STATUS_DRAW = 'draw'


def init_domino():
    domino_set = []
    for x in range(0, 7):
        for y in range(x, 7):
            domino_set.append([x, y])
    return domino_set


def distribute_domino():
    domino_full_set = init_domino()
    domino_full_set_dup = domino_full_set

    domino_full_set_dup, set1 = \
        random_choice_of_domino(domino_full_set_dup, NUM_STOCK)
    domino_full_set_dup, set2 = \
        random_choice_of_domino(domino_full_set_dup, NUM_COMPUTER)
    _, set3 = \
        random_choice_of_domino(domino_full_set_dup, NUM_PLAYER)
    return set1, set2, set3


def random_choice_of_domino(full_set, num_of_domino):
    new_set = []
    for _ in range(0, num_of_domino):
        domino = random.choice(full_set)
        new_set.append(domino)
        full_set.remove(domino)
    return full_set, new_set


def find_double_domino(domino_set):
    new_set = []
    for domino in domino_set:
        if domino[0] == domino[1]:
            new_set.append(domino)
    return new_set if len(new_set) > 0 else None


def find_max_double(domino_set):
    double_domino = find_double_domino(domino_set)
    max = -1
    max_domino = None
    if double_domino is not None:
        for domino in double_domino:
            sum = domino[0] + domino[1]
            if sum > max:
                max = sum
                max_domino = domino
    return max_domino, max


def check_status_draw():
    result = False

    if len(domino_snake) >= 7:
        first_domino = domino_snake[0]
        last_domino = domino_snake[-1]
        if first_domino[0] == last_domino[1]:
            cnt = 0
            for domino in domino_snake:
                if domino[0] == first_domino[0]:
                    cnt = cnt + 1
                if domino[1] == first_domino[1]:
                    cnt = cnt + 1
            if cnt == 8:
                result = True
    return result


def print_status():
    global status

    print('=' * 70)
    print('Stock size: {}'.format(len(stock_pieces)))
    print('Computer pieces: {}'.format(len(computer_pieces)))
    domino_snake_str = ''
    if len(domino_snake) <= 6:
        for domino in domino_snake:
            domino_snake_str = domino_snake_str + str(domino)
    else:
        for i in range(3):
            domino_snake_str = domino_snake_str + str(domino_snake[i])
        domino_snake_str = domino_snake_str + '...'
        for i in range(-3, 0, 1):
            domino_snake_str = domino_snake_str + str(domino_snake[i])
    print()
    print(domino_snake_str)
    print()
    print('Your pieces:')
    for i, domino in enumerate(player_pieces, start=1):
        print('{}:{}'.format(i, domino))
    print()

    if len(computer_pieces) == 0:
        status = STATUS_COMPUTER_WIN
    if len(player_pieces) == 0:
        status = STATUS_PLAYER_WIN
    if check_status_draw():
        status = STATUS_DRAW

    if status == STATUS_PLAYER_TURN:
        print("Status: It's your turn to make a move. Enter your command.")
    elif status == STATUS_COMPUTER_TURN:
        print("Status: Computer is about to make a move. Press Enter to continue...")
    elif status == STATUS_PLAYER_WIN:
        print('Status: The game is over. You won!')
    elif status == STATUS_COMPUTER_WIN:
        print('Status: The game is over. The computer won!')
    elif status == STATUS_DRAW:
        print("Status: The game is over. It's a draw!")


def player_request_turn():
    global player_pieces
    global stock_pieces
    global status

    result = False
    turn = 0
    success = False

    while not success:
        command = input('')
        try:
            turn = int(command)
            success = True
        except Exception as e:
            success = False
        if success:
            if not (-len(player_pieces) <= turn <= len(player_pieces)):
                success = False
        if not success:
            print("Invalid input. Please try again.")

    status = STATUS_COMPUTER_TURN
    if turn == 0:
        if len(stock_pieces) > 0:
            domino = stock_pieces.pop()
            player_pieces.append(domino)
        else:
            result = False
    elif 0 < turn <= len(player_pieces):
        domino = player_pieces[turn-1]
        player_pieces.remove(domino)
        domino_snake.append(domino)
    elif -len(player_pieces) <= turn < 0:
        domino = player_pieces[abs(turn)-1]
        player_pieces.remove(domino)
        domino_snake.insert(0, domino)
    else:
        pass

    return result


def computer_request_turn():
    global computer_pieces
    global stock_pieces
    global status

    input('')
    command = random.randint(-len(computer_pieces), len(computer_pieces))
    turn = int(command)
    status = STATUS_PLAYER_TURN
    if turn == 0:
        if len(stock_pieces) > 0:
            domino = stock_pieces.pop()
            computer_pieces.append(domino)
        else:
            status = STATUS_COMPUTER_TURN
    elif 0 < turn <= len(computer_pieces):
        domino = computer_pieces[turn-1]
        computer_pieces.remove(domino)
        domino_snake.append(domino)
    elif -len(computer_pieces) <= turn < 0:
        domino = computer_pieces[abs(turn)-1]
        computer_pieces.remove(domino)
        domino_snake.insert(0, domino)
    else:
        pass


if __name__ == '__main__':
    success_start = False
    while not success_start:
        stock_pieces, computer_pieces, player_pieces = distribute_domino()

        computer_max_domino, max_computer = find_max_double(computer_pieces)
        player_max_domino, max_player = find_max_double(player_pieces)
        domino_snake=[]

        if max_player > max_computer:
            domino_snake.append(player_max_domino)
            player_pieces.remove(player_max_domino)
            status = 'computer'
            score = max_player
        else:
            domino_snake.append(computer_max_domino)
            computer_pieces.remove(computer_max_domino)
            status = STATUS_PLAYER_TURN
            score = max_computer

        if score > 0:
            success_start = True

    while True:
        print_status()
        if status == STATUS_PLAYER_TURN:
            player_request_turn()
        elif status == STATUS_COMPUTER_TURN:
            computer_request_turn()
        else:
            break







