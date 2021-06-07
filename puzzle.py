'''
Puzzle class that turns an image into a puzzle!
Puzzle pieces are shuffled in ordered and rotated by 0, 90, 180 or 270
degrees.
The puzzle also includes the solution that includes the original order
(column by row, see helper.py) and the angle by which the piece was
rotated.
'''

from simpleimage import SimpleImage
import random
import helper 

# Finding the right ratio of puzzle pieces is a difficult problem. Therefore this hardcoded solution.
RATIO_PUZZLE_PIECES = {500: (32, 18),
                        1000: (48, 27),
                        2000: (64, 36)}
ANGLES = [0, 90, 180, 270]
TEST_FILE = 'test_images/Okaya_City_Library_1920_1080.jpg'

class Puzzle(SimpleImage):

    def __init__(self, filename, num_pieces = 500):
        if num_pieces not in [500, 1000, 2000]:
            raise ValueError('Number of puzzle pieces not 500, 1000 or 2000.')

        super().__init__(filename)
        if max(self.width, self.height) != 1920 or min(self.width, self.height) != 1080:
            raise ValueError('The input image is not 1920 x 1080 pixels.') 

        if self.width > self.height:
            self.num_pieces_x_axis = max(RATIO_PUZZLE_PIECES[num_pieces])
            self.num_pieces_y_axis = min(RATIO_PUZZLE_PIECES[num_pieces])
        else:
            self.num_pieces_x_axis = min(RATIO_PUZZLE_PIECES[num_pieces])
            self.num_pieces_y_axis = max(RATIO_PUZZLE_PIECES[num_pieces])

        self.actual_num_pieces = self.num_pieces_x_axis * self.num_pieces_y_axis
        print('Your puzzle has', self.actual_num_pieces, 'pieces because no puzzle has the number of pieces it says it has.')

        self.piece_width = int(self.width / self.num_pieces_x_axis)
        self.piece_height = int(self.height / self.num_pieces_y_axis)
        puzzle_pieces_temp = helper.create_blank_pieces(self.actual_num_pieces, 
                                                        self.piece_width, 
                                                        self.piece_height)
        
        # Returns {orignal_position: {'random_position': random_position}}, zero indexed
        self.solution = helper.create_solution(self.actual_num_pieces)

        k = 0
        for j in range(self.num_pieces_y_axis):
            for i in range(self.num_pieces_x_axis):
                puzzle_piece = puzzle_pieces_temp[k]
                angle = random.Random(2000).choice(ANGLES)
                for pixel in puzzle_piece:
                    x = pixel.x
                    y = pixel.y
                    x_rot, y_rot = helper.rotate_coordinates(x, 
                                                             y, 
                                                             angle, 
                                                             self.piece_width, 
                                                             self.piece_height)
                    original_pixel = self.get_pixel(x + self.piece_width * i, 
                                                    y + self.piece_height * j)
                    puzzle_piece.set_pixel(x_rot, y_rot, original_pixel)
                self.solution[k]['angle'] = angle
                k += 1
        
        self.puzzle_pieces = [i for i in range(self.actual_num_pieces)]
        for pos in self.solution:
            random_position = self.solution[pos]['random_position']
            puzzle_piece = puzzle_pieces_temp[pos]
            self.puzzle_pieces[random_position] = puzzle_piece

    def __len__():
        len(self.puzzle_pieces)
    
    def __iter__():
        for piece in self.puzzle_pieces:
            yield piece
    
    def assemble_puzzle_pieces(self):
        self.puzzle_pieces_assembled = SimpleImage.blank(self.width, self.height)
        k = 0
        for j in range(self.num_pieces_y_axis):
            for i in range(self.num_pieces_x_axis):
                puzzle_piece = self.puzzle_pieces[k]
                for pixel in puzzle_piece:
                    x = pixel.x
                    y = pixel.y
                    self.puzzle_pieces_assembled.set_pixel(
                                x + self.piece_width * i,
                                y + self.piece_height * j,
                                pixel)
                k += 1

def main():
    test_puzzle = Puzzle(TEST_FILE)
    test_puzzle.puzzle_pieces[0].show()
    test_puzzle.puzzle_pieces_assembled.show()

if __name__ == '__main__':
    main()

