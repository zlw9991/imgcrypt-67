# imgcrypt-67
Don't want your images scraped for an LLM training set? <br>
Don't have a GPU for nightshade or glaze? <br>
Only have a centrino?

This script cuts your art into 6x7 pieces.  <br>
Then takes 6-7 seconds turning ur passphrase 2 a decrypting SHA512 key. <br>

This forces all scrapers to spend 6-7 seconds hashing in order to unshuffle the image.

Grid & Hashtime is configurable via changing the instances of '6x7' & '6700000' to higher values.

Shuffler67 code modified from [@gabrielstork's](https://github.com/gabrielstork) work.

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

## Credits

* Thanks to [Gabriel Stork's](https://github.com/gabrielstork)'s library [Image_Shuffler](https://github.com/gabrielstork/image-shuffler)

### ZOMG WATCH THIS

[![WAOW](https://i.ytimg.com/vi/KxN5V1IzjnU/maxresdefault.jpg)](https://www.youtube.com/watch?v=KxN5V1IzjnU&list=PLbyhCGqsFkvu13i-qlNXXh1ucw8bJHjnx)
