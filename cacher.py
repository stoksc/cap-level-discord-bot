import pickle
import os
import glob
import data

def cache_embed(discord_em, query_type, query_str):
    query_dir = os.path.join(os.getcwd(), query_type)
    query_file = os.path.join(query_dir, query_str)
    with open(query_file, 'wb') as f:
        pickle.dump(discord_em, f)
    if sum([os.stat(query_file).st_size for f in os.listdir(query_dir)]) > data.MAX_SIZE:
        lru_file = min([(os.stat(query_file).st_atime, f) for f in os.listdir(query_dir)])
        os.remove(os.path.join(query_dir, lru_file[1]))

def uncache_embed(query_type, query_str):
    try:
        with open(os.path.join(os.getcwd(), query_type, query_str), 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None
