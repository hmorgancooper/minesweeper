from minesweeper import MinesweeperAI, Sentence

def test_sentence_Sentence_known_mines():
   example = Sentence([(0,0), (0,1)], 2)
   assert(example.known_mines() == {(0,0), (0,1)})


def test_sentence_Sentence_known_safes():
   example = Sentence([(0,0), (0,1)], 0)
   assert(example.known_safes() == {(0,0), (0,1)})

def test_sentence_mark_mine():
    example = Sentence([(0,0), (0,1)], 2)
    example.mark_mine((0,0)) 
    assert(example.cells == {(0,1)})

def test_sentence_mark_safe():
    example = Sentence([(0,0), (0,1)], 2)
    example.mark_safe((0,0)) 
    assert(example.cells == {(0,1)})

def test_add_knowlegde_moves_made():
   ai = MinesweeperAI()
   ai.add_knowledge((0,0), 1)
   assert(ai.moves_made == {(0,0)})

def test_add_knowlegde_safe_cell():
   ai = MinesweeperAI()
   ai.add_knowledge((0,0), 1)
   assert(ai.safes == {(0,0)})


   