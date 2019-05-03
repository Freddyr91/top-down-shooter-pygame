import game

g = game.Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
