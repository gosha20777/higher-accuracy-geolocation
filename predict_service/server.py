import flask
import csv
import pickle
from flask import Flask, jsonify, request, abort

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
                            request.json['p0r'])
    return result, 200

def get_predict_point(embeddings, p0x, p0y, p0r, p1x, p1y, p1r):
    p0x, p0y, p1x, p1y = get_corners(p0x+p0r, p0y+p0r, p1x+p1r, p1y+p1r)
    SOME_VARS = get_embaddings_of_tiles_in_area(p0x, p0y, p1x, p1y)
    
    id0 = get_tile_id_by_geolocation(p0x, p0y)
    id1 = get_tile_id_by_geolocation(p1x, p1y)
    tree = build_tree(SOME_VARS)
    predict_point = predict_on_tree(id0, id1, tree)


def get_all_embeddings(csv_file):
    embeddings = []
    with open(csv_file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            idx = row['id']
            embedding = pickle.loads(row['embedding'])
            lat = row['lat']
            lng = row['lng']
            item = (idx, lat, lng, embedding)
            embeddings.append(item)
    return embeddings

def load_embeddings(args):
    embeddings_path = args.patch
    
    global embeddings
    embeddings = get_all_embeddings(embeddings_path)

    return embeddings

def main(args=None):
    app.run(debug=True, host='0.0.0.0', port=5000)    

if __name__ == '__main__':
    main()