from settings import *
from game import *

g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()