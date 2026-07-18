import json
import hashlib
from base64 import b64encode,b64decode
from Crypto.Cipher import AES
from image_shuffler67 import Shuffler67
import imageio.v3 as iio # Added 16/7/2026
gif_img_array = [None] * 30 # Added 16/7/2026

def encrypt_text():
    print("\n SHUFFLING IMG \n")
    passphrase = str(input("enter your passphrase: "))
    print("\n")
    unshuffledimg = str(input("enter your image filename: "))
    
    repeathash = hashlib.sha512(passphrase.encode()).digest() # create first hash by turning passphrase into bytes, hashing, then give hash a byte format
    
    hctr = 0
    while ( hctr <= 6700000 ):
        repeathash = hashlib.sha512(repeathash).digest()
        hctr = hctr + 1
        # repeat for 6.7 million times
    
    # shuffles & flips img w keyhash
    image = Shuffler67(unshuffledimg)
    image.shuffle(repeathash, matrix=(6,7))
    image.save()

def pixelate_img_2_gif(): # added 8/7/2026, modified 16/7/2026
    print("\n PIXELATING 2 GIF \n")
    unpixelimg = str(input("enter your unpixellated image filename: "))
    print("\n")
    passphrase_sentence = str(input("enter a sentence longer than 31 words: ")).split()
    
    for ctri in range(0, 30, 1): # generating gif frames
        passphrase = passphrase_sentence[ctri]
    
        repeathash = hashlib.sha512(passphrase.encode()).digest() # create first hash by turning passphrase into bytes, hashing, then give hash a byte format
    
        hctr = 0
        while ( hctr <= 30 ):
            repeathash = hashlib.sha512(repeathash).digest()
            hctr = hctr + 1
            # repeat for 67 times
    
        # flip again to unflip, then do unshuffling
        image = Shuffler67(unpixelimg)
        image.pixelate(repeathash, matrix=(6,7))
        gif_img_array[ctri] = image
    
    # merging frames
    
    legit_frames = [frame.shuffled[..., ::-1] for frame in gif_img_array if frame is not None] 
    # ^ clear out empty frames, invert colour for iio
    if len(legit_frames) == 30: # check frames count is 67 and generate webm.
        iio.imwrite( # save webm at 67fps with compression
            "protected-" +str(unpixelimg) + ".webm",
            legit_frames,
            plugin="pyav",
            fps=67,
            codec="libvpx-vp9",
            out_pixel_format="yuv420p"
        )
    if len(legit_frames) == 30: # check frames count is 67 and generate mp4.
        iio.imwrite( # save webm at 67fps with compression
            "protected-" +str(unpixelimg) + ".mp4",
            legit_frames,
            plugin="pyav",
            fps=67,
            codec="libx264",
            out_pixel_format="yuv420p"
        )

def decrypt_text():
    print("\n UNSHUFFLING \n")
    passphrase = str(input("enter your passphrase: "))
    print("\n")
    shuffledimg = str(input("enter your shuffled image filename: "))
    
    repeathash = hashlib.sha512(passphrase.encode()).digest() # create first hash by turning passphrase into bytes, hashing, then give hash a byte format
    
    hctr = 0
    while ( hctr <= 6700000 ):
        repeathash = hashlib.sha512(repeathash).digest()
        hctr = hctr + 1
        # repeat for 6.7 million times
    
    # flip again to unflip, then do unshuffling
    image = Shuffler67(shuffledimg)
    image.unshuffle(repeathash, matrix=(6,7))
    image.save_unshuffle()

i = 0
while ( i != 9 ):
    print("###################################")
    print("# IMG67HASHCRYPT MENU, ENTER A NO:#")
    print("# 1 == shuffle img                #")
    print("# 2 == unshuffle img              #")
    print("# 3 == pixellate img 2 webm + mp4 #")  # added 8/7/2026, modified 16/7/2026
    print("# 9 == quit                       #")
    print("###################################")
    i = int(input("Enter num: "))
    if ( i == 9 ):
        print("\n quitting... \n")
    elif ( i == 1 ):
        encrypt_text()
    elif ( i == 2 ):
        decrypt_text()
    elif ( i == 3 ): # added 8/7/2026, modified 16/7/2026
        pixelate_img_2_gif()
    else:
        print("\n Invalid No: \n")
