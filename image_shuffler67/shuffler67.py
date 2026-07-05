import random
import warnings
import pathlib
import cv2 as cv
import numpy as np
# modified
from PIL import Image
# modified
class Shuffler67:
    def __init__(self, image: str) -> None:
        self.path = pathlib.Path(image)
        self.original = cv.imread(str(self.path.resolve()))

        if self.original is None:
            raise ValueError('image is None')
        
        self.shuffled = self.original.copy()
        self.x = self.original.shape[1]
        self.y = self.original.shape[0]

        self._pieces = []

    def _check_argument(self, matrix: tuple) -> None:
        if len(matrix) != 2 or not all(isinstance(x, int) for x in matrix):
            raise ValueError(
                'matrix must be 2-dimensional containing only integer numbers'
            )
        elif min(matrix) <= 0:
            raise ValueError('matrix values must be greater than 0')
        elif matrix > (self.x, self.y):
            raise ValueError('number of splits greater than pixels') 

    def _check_pixel_loss(self, x_missing: int, y_missing: int) -> None:
        new_x = self.x - x_missing
        new_y = self.y - y_missing

        if (x_missing + y_missing) > 0:
            warnings.warn(
                'Splitting images into non-integer intervals causes pixel '
                f'loss. Original Shape: ({self.x}, {self.y}) New Shape: '
                f'({new_x}, {new_y})',
                stacklevel=2,
            )

    def _split(self, x: int, y: int, x_list: list, y_list: list) -> None:
        if len(self._pieces) > 0:
            self._pieces.clear()

        for x_n, x_piece in enumerate(x_list):
            for y_n, y_piece in enumerate(y_list):
                self._pieces.append(
                    self.original[y_n * y:y_piece, x_n * x:x_piece]
                )

    def _generate_image(self, cols: int) -> None:
        chunks = [
            np.vstack(chunk) for chunk in zip(*[iter(self._pieces)] * cols)
        ]
        self.shuffled = np.hstack(np.array(chunks, dtype=np.uint8))

    def shuffle(self, keyhash, matrix: tuple) -> None:
        # modified
        self._check_argument(matrix)

        x = int(self.x / matrix[0])
        x_missing = self.x - (x * matrix[0])
        x_list = list(range(x, self.x + 1, x))

        y = int(self.y / matrix[1])
        y_missing = self.y - (y * matrix[1])
        y_list = list(range(y, self.y + 1, y))

        self._check_pixel_loss(x_missing, y_missing)
        self._split(x, y, x_list, y_list)
        
        # prefix random seed with keyhash, start of modification
        rng = random.Random(int.from_bytes(keyhash, byteorder='big'))
        rng.shuffle(self._pieces)
        # end shuffling
        
        # flip image based on seed
        # first go block by block
        for ctri in range(len(self._pieces)):
            fliptype = rng.randint(0,1)
            
            # numpy blocks are:
            # [ per row, up2bottom -> [ per pixel in row, left2right [rgb],[rgb]..], [[rgb]..], .. ]
            
            if fliptype == 1:
                # flips rows up to down
                self._pieces[ctri] = self._pieces[ctri][::-1]
            else:
                # select one row
                ctri_row = 0
                for onerow in self._pieces[ctri]:
                    # flip row left to right
                    self._pieces[ctri][ctri_row] = onerow[::-1]
                    ctri_row = ctri_row + 1
        # end image flipping

        self._generate_image(matrix[1])
        # end function
    
    
    def unshuffle(self, keyhash, matrix: tuple) -> None:
        # modified
        self._check_argument(matrix)

        x = int(self.x / matrix[0])
        x_missing = self.x - (x * matrix[0])
        x_list = list(range(x, self.x + 1, x))

        y = int(self.y / matrix[1])
        y_missing = self.y - (y * matrix[1])
        y_list = list(range(y, self.y + 1, y))

        self._check_pixel_loss(x_missing, y_missing)
        self._split(x, y, x_list, y_list)
        
        # prefix random seed with keyhash, start of modification
        rng = random.Random(int.from_bytes(keyhash, byteorder='big'))
        
        # use a copy to waste the seed_nums for the shuffle
        useless_matrix = self._pieces.copy()
        rng.shuffle(useless_matrix)
        
        # flip image based on seed
        # first go block by block
        for ctri in range(len(self._pieces)):
            fliptype = rng.randint(0,1)
            
            # numpy blocks are:
            # [ per row, up2bottom -> [ per pixel in row, left2right [rgb],[rgb]..], [[rgb]..], .. ]
            
            if fliptype == 1:
                # flips rows up to down
                self._pieces[ctri] = self._pieces[ctri][::-1]
            else:
                # select one row
                ctri_row = 0
                for onerow in self._pieces[ctri]:
                    # flip row left to right
                    self._pieces[ctri][ctri_row] = onerow[::-1]
                    ctri_row = ctri_row + 1
        # flipping ends
        
        # regenerate seeds again
        rng = random.Random(int.from_bytes(keyhash, byteorder='big'))
        # unshuffling begins
        block_number = len(self._pieces)
        positions = list(range(block_number)) # ie: [0 1 2 3 4 5]
        rng.shuffle(positions) # gives us the shuffled image in array index context
        # ie: [5 4 3 2 1 0]
        
        # restore & save seperately original index of unshuffled image
        temp_blocks = [None] * block_number
        for current_index, shuffled_index in enumerate(positions):
            # temp_blocks[4] = self._pieces[1]
            temp_blocks[shuffled_index] = self._pieces[current_index]
            
        #restore original image
        for ctri_restore in range(block_number):
            self._pieces[ctri_restore] = temp_blocks[ctri_restore]
        # unshuffling ends

        self._generate_image(matrix[1])
        # end function
    

    def show(self) -> None:
        cv.imshow('Image', self.shuffled)
        cv.waitKey(0)
        cv.destroyAllWindows()

    def save(self) -> None:
        cv.imwrite(
            str(self.path.parent.resolve() / f'shuffled_{self.path.name}'),
            self.shuffled,
        )
    
    def save_unshuffle(self) -> None:
        cv.imwrite(
            str(self.path.parent.resolve() / f'unshuffle_{self.path.name}'),
            self.shuffled,
        )
