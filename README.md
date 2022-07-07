# minesweeper
An AI to play minesweeper, completed as part of CS50: Introduction to AI.
The AI uses knowledge of the board stored in 'sentences' which contain a set of cells and the number of mines contained within that set.

When a cell is clicked on the following steps take place:
1. The cell is added to the list of moves made and to the list of safe cells
2. A 'sentence' is created to store the new knowledge in the form {set of adjacent cells}: number of mines
3. Any known safe cells and known mines are removed from the sentence and the count adjusted accordingly
4. If none of the cells are mines (i.e.the count is equal to 0) all the cells are added to the list of safe cells
5. If all the cells are mines (i.e. if the count is equal to the length of the set) then the cells are added to the list of known mines 
6. The sentence is added to the knowledge base
7. Each sentence in the knowledge base is compared to every other sentence
8. If sentence A is a subset of sentence B then new knowledge can be created: 
* {B.cells} - {A.cells} = B.count - A.count
9. Then steps 1 - 8 are repeated until there are no new changes\
10. The AI then selects a cell from the list of known safes to play
11. If there are no safes then the AI makes a random move (which is not in moves_made or known_mines)

Code I wrote:
* test_minesweeper.py
* requirements.txt
* In minesweeper.py, (Sentence class) - known_mines, known_safes, mark_mine, mark_safe
* In minesweeper.py (MinesweeperAI class) - mark_mine, mark_safe, add_knowledge, generate_new_knowledge_sentence, 
update_with_inferred_sentences, find_subsets_and_create_new_sentences, check_all_sentences_for_known_safes_and_mines,\
make_safe_move, make_random_move

Code provided:
* runner.py
* In minesweeper.py Minesweeper class
* In minesweeper.py (Sentence class) - __init__, __eq__, __str__
* In minesweeper.py (MinesweeperAI class) - __init__, __eq__, __str__
