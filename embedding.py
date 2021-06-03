import hashlib
import random
from typing import List
import numpy as np
from Crypto.Cipher import Salsa20
from Crypto.Util.number import bytes_to_long

def extract_key(key: str):
    """Derive a key1 and key2 from a password str and returns a hex tuple (key1, key2) """
    digest = hashlib.sha256(key).digest()
    key1 = hex(bytes_to_long(digest))
    key2 = hashlib.sha256(digest).hexdigest()

    return key1, key2 

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

def prng(message: bytes, seed: int, image: np.ndarray) -> List[int]:
    """Generates an array of random locations with pseudo-random sequence based on seed"""
    random.seed(seed)
    random_location_array = random.sample(range(0, image.size), len(message))
    return random_location_array

def modulation(pseudo_rand_array: List[int], message: bytes, img: np.ndarray) -> np.ndarray:
    """Modulates a message into an image with a pseudo random sequence array """
    lines, columns = img.shape
    for i,char in zip(pseudo_rand_array, message):
        img[i//columns][i%columns] = img[i//columns][i%columns]*char
    return img

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
