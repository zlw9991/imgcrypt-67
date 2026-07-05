# imgcrypt-67
Don't want your images scraped for an LLM training set? <br>
Don't have a GPU for nightshade or glaze? <br>
Only have a centrino?

This script cuts your art into 6x7 pieces.  <br>
Then takes 6-7 seconds turning ur passphrase 2 a decrypting SHA512 key. <br>

Grid & Hashtime is configurable via changing the instances of '6x7' & '6700000' to higher values.

# Installation & Startup

Installation:
```
python3 -m venv .venv
source .venv/bin/activate
pip install pycryptodome
pip install numpy
pip install opencv-python
pip install Pillow
deactivate
```

Do not forget to copy the ```image_shuffler67``` folder into the directory where the above python venv exists.

Operation:
```
source .venv/bin/activate
python3 img67hashcrypt.py
deactivate
```

# Try decrypting this image!

![what_a_funky](shuffled_IOSYS_ska.jpg)

- passphrase: flandre
