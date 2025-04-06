from typing import Iterator
import io
from create_breakable_files import create_binary_file, create_invalid_utf8_file


def _read_chunks_reversed(file: io.BufferedReader, buffer_size: int) -> Iterator[bytes]:
    """
    NOTE(lfacciolo)
    Given a file opened in binary mode and a buffer size,
    yields chunks of bytes starting from the end of the file and moving backwards.
    """
    file.seek(0, io.SEEK_END)
    position = file.tell()
    while position > 0:
        read_size = min(buffer_size, position)
        position -= read_size
        file.seek(position)
        yield file.read(read_size)


def is_safe_to_utf8_decode(chunk: bytes, leftover: bytes = b"") -> tuple[str, bytes]:
    """
    NOTE(lfacciolo)
    Given a chunk of bytes and any leftover from a previous read,
    tries to decode the bytes into UTF-8.

    It attempts up to 4 times because UTF-8 characters can be up to 4 bytes long.
    If decoding fails, it removes 1 byte at a time from the end and saves it as leftover.

    Returns:
        A tuple containing:
        - The decoded text
        - Any remaining bytes that could not be decoded (leftover for the next chunk)
    """
    chunk += leftover
    max_utf8_char_size = 4

    for bytes_removed in range(max_utf8_char_size):
        try:
            decoded_text = chunk.decode("utf-8")
            return decoded_text, b""
        except UnicodeDecodeError:
            split_point = len(chunk) - (bytes_removed + 1)
            leftover = chunk[split_point:]
            chunk = chunk[:split_point]

    raise ValueError("Failed to decode UTF-8.")


def last_lines(
    filename: str, buffer_size: int = io.DEFAULT_BUFFER_SIZE
) -> Iterator[str]:

    with open(filename, "rb") as f:
        leftover = b""
        for chunk in _read_chunks_reversed(f, buffer_size):
            text, leftover = is_safe_to_utf8_decode(chunk, leftover)
            lines = text.splitlines(keepends=True)
            for line in reversed(lines):
                yield line


if __name__ == "__main__":
    try:
        create_invalid_utf8_file()
        create_binary_file()
        root = "exercise2"
        file = "binary_file.txt"
        file_full_path = f"{root}/{file}"
        for line in last_lines(file_full_path, 20):
            print(line, end="")
    except Exception as e:
        raise Exception(f"error reading parser {e}")
