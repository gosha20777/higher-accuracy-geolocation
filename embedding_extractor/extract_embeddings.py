from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import seaborn as sns
sns.set_style("darkgrid")
from PIL import Image
from torchvision import transforms
import torch

import torchvision
from torch.utils.data.sampler import WeightedRandomSampler
from tensorboardX import SummaryWriter
import seaborn as sns
sns.set_style("darkgrid")

from networks import Loc2Vec
from datasets import GeoTileInferDataset, get_files_from_path, cleanse_files
from config import IMG_SIZE

import psycopg2
from psycopg2 import sql


def load_model(checkpoint_file):
    cuda = torch.cuda.is_available()
    model = Loc2Vec()
    model = torch.load(checkpoint_file)
    model.eval()
    if cuda:
        model.cuda()
    return model

def extract_embedding_from_tile(model, tile)
    return [0.1, 0.1, 0.1, 0.1, 0.1, 0.1]

def load_tile(patch):
    infer_transforms = transforms.Compose([
        transforms.CenterCrop(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                             [0.229, 0.224, 0.225])])

def get_all_embeddings(model, csv_file):
    embeddings = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row['id'], row['patch'])
            tile = load_tile(patch)
            embedding = extract_embedding_from_tile(model, tile)
            lat = row['lat']
            lng = row['lng']
            embedding_pickle_string = pickle.dumps(embedding)
            item = (row['id'], lat, lng, embedding_pickle_string)
            embeddings.append()
    return embeddings

def insert_embeddings_into_db(embeddings, host, port, user, password, database):
    conn = psycopg2.connect(host=host,
                        port=port,
                        user=user,
                        password=password,
                        database=database)
    
    cursor = conn.cursor()
    insert = sql.SQL('INSERT INTO city (code, name, country_name) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, embeddings))
    )
    cursor.execute(insert)
    conn.commit()
    cursor.close()
    conn.close()
    return

def insert_embeddings_into_csv(embeddings, file):
    with open(file, mode='w') as csv_file:
        fieldnames = ['id', 'lat', 'lng', 'embedding']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for (idx, lat, lng, embedding_pickle_string) in embeddings:
            writer.writerow(
                {
                    'id': idx,
                    'lat': lat,
                    'lng': lng,
                    'embedding': embedding
                })
    return



checkpoint_file = ""
csv_file = ""
out_csv = ""
host = ""
port = ""
user = ""
password = ""
database = ""

model = load_model(checkpoint_file)
embeddings = get_all_embeddings(model, csv_file)
#insert_embeddings_into_db(embeddings,
#                        host=host,
#                        port=port,
#                        user=user,
#                        password=password,
#                        database=database))

insert_embeddings_into_csv(embeddings, out_csv)
print('done')

