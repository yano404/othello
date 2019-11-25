import othello

def main():
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
                pos, score = game.alphabeta()
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
    print(game.getlog())

if __name__ == '__main__':
    main()
