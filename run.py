import othello

def main(method="alphabeta"):
    game = othello.game()
    print("Your stone is Black(B)")
    while game.goeson():
        if game.turn() == 1:
            # user
            game.show()
            while True:
                try:
                    if len(game.findavailable()) == 0:
                        print("You cannot put the stone...pass")
                        game.upass()
                        break
                    print("Enter the position you want to put the stone.")
                    row = int(input("row >"))
                    col = int(input("col >"))
                    game.put(row, col)
                    game.show()
                    break
                except ValueError:
                    print("Enter 1~8")
                except othello.CanNotPutStoneError:
                    print("You cannot put the stone there.")
        else:
            # computer
            if len(game.findavailable()) == 0:
                game.upass()
            else:
                if method == "alphabeta":
                    pos, score = game.alphabeta()
                else:
                    pos, score = game.minmax()
                print("score:", score)
                game.put(pos[0], pos[1])

    game.show()
    winner = game.winner()
    if winner == 1:
        print("You Win!")
        print("Black: ", game.numblack())
        print("White: ", game.numwhite())
    elif winner == -1:
        print("You Lose...")
        print("Black: ", game.numblack())
        print("White: ", game.numwhite())
    else:
        print("Draw")
    print("log: (stone, row, col)")
    print(game.getlog())

if __name__ == '__main__':
    methods = ["minmax", "alphabeta"]
    while True:
        print("Select method:")
        for i, method in enumerate(methods):
            print(f"{i+1}) {method}")
        try:
            sel = methods[int(input(">")) - 1]
            break
        except (ValueError, IndexError):
            print("Enter a valid number.")

    main(sel)
