import json
import hashlib
from base64 import b64encode,b64decode
from Crypto.Cipher import AES
from image_shuffler67 import Shuffler67

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
    print("# 9 == quit                       #")
    print("###################################")
    i = int(input("Enter num: "))
    if ( i == 9 ):
        print("\n quitting... \n")
    elif ( i == 1 ):
        encrypt_text()
    elif ( i == 2 ):
        decrypt_text()
    else:
        print("\n Invalid No: \n")
