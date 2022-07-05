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

def test_add_knowledge_1():
   ai = MinesweeperAI()
   ai.add_knowledge((7,7), 1)
   assert(ai.knowledge[0] == Sentence([(6, 6), (6, 7), (7, 6)], 1))

def test_add_knowledge_removing_mines():
   ai = MinesweeperAI()
   ai.mines.add((6,6))
   ai.add_knowledge((7,7), 2)
   assert(ai.knowledge[0] == Sentence([(6, 7), (7, 6)], 1))

def test_add_knowledge_removing_safes():
   ai = MinesweeperAI()
   ai.safes.add((6,6))
   ai.add_knowledge((7,7), 1)
   assert(ai.knowledge[0] == Sentence([(6, 7), (7, 6)], 1))

# def test_add_knowledge_removing_safes_in_existing_knowledge():
#    ai = MinesweeperAI()
#    ai.safes.add((6,6))
#    ai.add_knowledge((7,7), 1)
#    ...
#    assert(ai.knowledge[0] == Sentence([(6, 7), (7, 6)], 1))
   
def test_count_0_sets_all_to_safe():
   ai = MinesweeperAI()
   ai.add_knowledge((6,6), 0)
   assert(ai.safes == {(6,6), (5, 5), (6, 5), (5, 7), (6, 7), (7, 6), (5, 6), (7, 5), (7,7)})

# test count = number adjacent sets all to mines
def test_count_is_len_cells_sets_all_to_mines():
   ai = MinesweeperAI()
   ai.add_knowledge((6,6), 8)
   assert(ai.mines == {(5, 5), (6, 5), (5, 7), (6, 7), (7, 6), (5, 6), (7, 5), (7,7)})

def test_add_knowledge_removing_mines_retrospectively():
   ai = MinesweeperAI()
   ai.add_knowledge((7,7), 2)
   ai.mark_mine((6,6))
   assert(ai.knowledge[0] == Sentence([(6, 7), (7, 6)], 1))

def test_add_knowledge_updates_knowledge():
   ai = MinesweeperAI()
   ai.add_knowledge((6,6), 3)
   ai.add_knowledge((7,7), 2)
   assert(ai.knowledge[0] == Sentence([(5, 5), (6, 5), (5, 7), (5, 6), (7, 5)], 1))

def test_overlapping_cells_create_new_knowledge():
   ai = MinesweeperAI()
   ai.add_knowledge((6,6), 3)
   ai.add_knowledge((7,7), 1)
   assert(ai.knowledge[2] == Sentence([(5, 5), (6, 5), (5, 7), (5, 6), (7, 5)], 2))

# test that no matching cells does not create new knowledge
# test that add knowledge cycles through until no more changes to knowledge


