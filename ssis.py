import argparse
from base64 import b64decode, b64encode
from binascii import hexlify, unhexlify

import numpy as np
from Crypto.Util.number import bytes_to_long, long_to_bytes
from PIL import Image

from embedding import (decrypt, deinterleaver, demodulation, encrypt,
                       extract_keys, imouto, interleaver, modulation, oniichan,
                       prng)

parser = argparse.ArgumentParser(description="Cacher une image dans une image par stéganographie à étalement de spectre")
subparser = parser.add_subparsers(title="Commandes:", description="Commandes à utiliser pour extraire/cacher une image", dest="steg")

embed = subparser.add_parser("embed", description="Commande pour cacher une image")
extract = subparser.add_parser("extract", description="Commande pour extraire une imge")


embed.add_argument("-k", "--key", help="La clef ou le mot de passe pour cacher l'image", required=True)
embed.add_argument("-s", "--source", help="Le chemin du fichier image à cacher", required=True)
embed.add_argument("-c", "--cover", help="Le chemin du fichier image couverture", required=True)
embed.add_argument("-o", "--output", help="Le chemin du fichier image de l'image stéganographique", required=True)


extract.add_argument("-k", "--key", help="La clef ou le mot de passe pour extraire l'image", required=True)
extract.add_argument("-s", "--stego", help="Le chemin du fichier image stéganographique", required=True)
extract.add_argument("-o", "--output", help="Le chemin du fichier image de l'image extraite", required=True)

args = parser.parse_args()

def extract_image(src: str, passwd: str):
    decryption_key, seed_prng_key, deinterleaver_seed_key = extract_keys(passwd)
    img = oniichan(src)
    #steps: deinterleave, demodulate, decrypt
    rand_seq_interleaver = prng()
    deinterleaver()

def embed_image(src: str, cover: str, passwd: str, output: str) -> None:
    encryption_key, seed_prng_key, interleaver_seed_key = extract_keys(passwd.encode())
    source_img = oniichan(src).encode()

    cover_img = np.array(Image.open(cover))
    cover_img_size = cover_img.size // cover_img.shape[-1]
    # encrypt, modulate, interleave
    encryption_key = unhexlify(encryption_key)
    encrypted_message = b64encode(encrypt(source_img, encryption_key))

    seed_prng_key = bytes_to_long(unhexlify(seed_prng_key))
    rnd_loc_array = prng(len(encrypted_message), seed_prng_key, cover_img_size)
    modulated = modulation(rnd_loc_array, encrypted_message.decode(), cover_img)

    interleaver_seed_key = bytes_to_long(unhexlify(interleaver_seed_key))
    rnd_intrlvr_array = prng(modulated[..., -1].size, interleaver_seed_key, cover_img_size)
    interleaved = interleaver(rnd_intrlvr_array, modulated[..., -1])

    cover_img[..., -1] = interleaved

    stego_img = Image.fromarray(cover_img)
    stego_img.save(output)


if __name__ == "__main__":
    if args.steg == "embed":
        embed_image(args.source, args.cover, args.key, args.output)

        
    elif args.extract:
        pass

    
    


    
