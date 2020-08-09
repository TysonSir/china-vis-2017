import os

class MatchAlgo:
    def isImageSame(self, img1, img2):
        return os.path.abspath(img1) == os.path.abspath(img2)