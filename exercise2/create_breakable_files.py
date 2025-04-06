import os


def create_invalid_utf8_file():
    with open("exercise2/invalid_utf8.txt", "wb") as f:
        f.write(b"Valid line 1\n")
        f.write(b"Valid line 2\n")
        f.write(b"\xf0\x9f")


def create_binary_file():
    with open("exercise2/binary_file.txt", "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR")
