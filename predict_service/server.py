import flask
import csv
import pickle
from flask import Flask, jsonify, request, abort
from scipy.interpolate import interp1d

app = flask.Flask(__name__)# define a predict function as an endpoint 

@app.route("/predict", methods=["GET","POST"])
def predict():
    if not request.json or not 'data' in request.json:
        abort(400)
    result = get_predict_point(embeddings,
                            request.json['p0x'], 
                            request.json['p0y'],
                            request.json['p0r'],
                            request.json['p1x'],
                            request.json['p1y'],
                            request.json['p1r'])
    return result, 200

def get_predict_point(embeddings, p0x, p0y, p0r, p1x, p1y, p1r):
    max_p0x, max_p0y, max_p1x, max_p1y = get_corners(p0x, p0y, p0r, p1x, p1y, p1r)
    
    area_embeddings = get_embaddings_of_tiles_in_area(max_p0x, max_p0y, max_p1x, max_p1y)
    
    id0 = get_tile_id_by_geolocation(p0x, p0y)
    id1 = get_tile_id_by_geolocation(p1x, p1y)
    grapf = build_grapf(area_embeddings)
    predict_point = predict_on_tree(id0, id1, grapf)

def predict_point(id0, id1, grapf):
    interpolation_size = 5
    # interpolate from 185175 to 751688
    # These numbers are cherry picked. Once we train for longer, we can remove it
    begin_index = id0 #84212
    end_index = id1
    fst = grapf.get_item_vector(begin_index)
    snd = grapf.get_item_vector(end_index)
    linfit = interp1d([1,interpolation_size], np.vstack([fst, snd]), axis=0)

    item = []
    item = item + [begin_index]
    for i in range(0,interpolation_size):    
        item = item + t.get_nns_by_vector(linfit(i+1),1)

    item = item + [end_index]
    columns = 8
    rows = 1


    w=15
    h=15
    fig=plt.figure(figsize=(20,4))
    plt.title("Interpolation between two locations via embedding")
    plt.subplots_adjust(left=0.32, bottom=0, right=1.0, top=0.7, wspace=0.02, hspace=0.02)
    plt.axis('off')
    for i, index in enumerate(item):
        img = np.random.randint(10, size=(h,w))
        fig.add_subplot(rows, columns, i+1)
        img = Image.open(pd_files.path[index], 'r')
        data = img.convert('RGB')        
        t_img = torch.from_numpy(np.asarray(data))
        t_img_np = t_img.numpy()
        # plt.title(index)
        plt.axis('off')
        plt.imshow(t_img_np)

    plt.show()

def get_corners(p0x, p0y, p0r, p1x, p1y, p1r):
    norm1 = l1(p0x+p0r, p0y+p0r, p1x+p1r, p1y+p1r)
    norm2 = l1(p0x-p0r, p0y-p0r, p1x-p1r, p1y-p1r)
    norm3 = l1(p0x-p0r, p0y-p0r, p1x+p1r, p1y+p1r)
    norm4 = l1(p0x+p0r, p0y+p0r, p1x-p1r, p1y-p1r)
    return min(norm1, norm2, norm3, norm4)

def get_embaddings_of_tiles_in_area(p0x, p0y, p1x, p1y)
    area_embeddings = []
    for x in range(p0x, p1x):
        for y in range(p0y, p1y):
            idx = get_tile_id_by_geolocation(x, y)
            embedding = get_embedding_by_id(idx)
            item = (idx, embedding)
            area_embeddings.append(item)
    return area_embeddings



def l1(p0x, p0y, p1x, p1y):
    return abs(p0x-p1x) + abs(p0y-p1y)

def build_grapf(area_embeddings):
    t = AnnoyIndex(16, metric='euclidean')  # Length of item vector that will be indexed
    for (idx, embedding) in area_embeddings:
        t.add_item(idx, embedding)
    return t

def get_all_embeddings(csv_file):
    embeddings = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            idx = row['id']
            embedding = pickle.loads(row['embedding'])
            lat = row['lat']
            lng = row['lng']
            patch = row['patch']
            item = (idx, lat, lng, patch, embedding)
            embeddings.append(item)
    return embeddings

def load_embeddings(args):
    embeddings_path = args.patch
    
    global _embeddings
    _embeddings = get_all_embeddings(embeddings_path)

    return _embeddings

def main(args=None):
    app.run(debug=True, host='0.0.0.0', port=5000)    

if __name__ == '__main__':
    main()