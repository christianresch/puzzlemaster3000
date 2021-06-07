'''
Try out the PuzzleMaster3000!
'''

from puzzle import Puzzle

TEST_FILE = 'test_images/Okaya_City_Library_1920_1080.jpg'

def main():
    test_puzzle = Puzzle(TEST_FILE, num_pieces = 500)
    test_puzzle.show()
    test_puzzle.puzzle_pieces[0].show()
    test_puzzle.assemble_puzzle_pieces()
    test_puzzle.puzzle_pieces_assembled.show()

if __name__ == '__main__':
    main()

