import hashlib
import random
from base64 import b64decode, b64encode
from binascii import hexlify
from typing import List

import numpy as np
from Crypto.Cipher import Salsa20


def extract_keys(key: bytes) -> str:
    """Derive a key1,key2, key3 from a password str and returns a hex tuple (key1, key2, key3) """
    digest = hashlib.sha256(key).digest()
    key1 = hexlify(digest)
    key2 = hashlib.sha256(digest).hexdigest()
    key3 = hashlib.sha256(hashlib.sha256(digest).digest()).hexdigest()
    return key1, key2, key3

def encrypt(msg: bytes, key: bytes) -> bytes:
    """Encrypt a plaintext message with key using Salsa20"""
    cipher = Salsa20.new(key=key)
    encrypted_message = cipher.encrypt(msg)
    return encrypted_message

def decrypt(msg: bytes, key: bytes) -> bytes:
    """Decrypt a plaintext message with key using Salsa20"""
    cipher = Salsa20.new(key=key)
    decrypted_message = cipher.decrypt(msg)
    return decrypted_message

def prng(length_message: int, seed: int, cover_image_size: int) -> List[int]:
    """Generates an array of random locations with pseudo-random sequence based on seed"""
    random.seed(seed)
    random_location_array = random.sample(range(0, cover_image_size), length_message)
    return random_location_array

def modulation(pseudo_rand_array: List[int], message: str, cover_img: np.ndarray) -> np.ndarray:
    """Modulates a message into an image with a pseudo random sequence array """
    img = cover_img.copy()
    blue_plane = extract_planes(img)
    for i, char in zip(pseudo_rand_array, message):
        blue_plane[i] = ord(char)
    img[...,-1] = blue_plane.reshape(img[...,-1].shape).copy()
    return img

def demodulation(pseudo_rand_array: List[int], cover_img: np.ndarray, img: np.ndarray) -> str:
    """demodulates a message from an image with a pseudo random sequence array """
    message = ''
    blue_plane = extract_planes(img)
    blue_cover_plane = extract_planes(cover_img)
    for i in pseudo_rand_array:
        message += chr(blue_cover_plane[i])
    return message

def interleaver(pseudo_rand_array: List[int], array: np.ndarray):
    """Random permutations for interleaving an array according to a pseudo random sequence"""
    dims = array.shape
    flat_array = array.flatten()
    matrix = np.zeros(array.size, int)
    for index, position in enumerate(pseudo_rand_array):
        matrix[index] = flat_array[position]
    matrix = matrix.reshape(dims)
    return matrix

def deinterleaver(pseudo_rand_array: List[int], array: np.ndarray):
    """Random permutations for deinterleaving an array according to a pseudo random sequence"""
    dims = array.shape
    flat_array = array.flatten()
    matrix = np.zeros(array.size, int)
    for index, position in enumerate(pseudo_rand_array):
        matrix[position] = flat_array[index]
    matrix = matrix.reshape(dims)
    return matrix

def oniichan(path: str) -> str :
    """Encode a file to base64"""
    with open(path, "rb") as f:
        img = f.read()
    b64_img = b64encode(img)
    return b64_img.decode()

def imouto(base64_img: str, path: str) -> None :
    """Decode a base64 encoded file"""
    img = b64decode(base64_img)
    with open(path, "wb") as f:
        f.write(img)

def extract_planes(planes: np.ndarray) -> np.ndarray:
    """Return a n x m array, Blue channel if jpeg, alpha channel 
    if PNG since the last array is either the Blue or the alpha"""
    blue__or_alpha_plane = planes[..., -1]
    return blue__or_alpha_plane.flatten()
