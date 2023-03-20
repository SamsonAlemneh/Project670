from app import app

from app.api.compute.image_blur_faces import image_blur_faces
from app.api.compute.image_extract_text import image_extract_text
from app.api.compute.neighbors import compute_neighbors
from app.api.compute.pano_util import stitch
from app.api.compute.panoramic import compute_panoramic
from app.api.image_upload import api_get_tour_images, api_set_panoramic_image
from app.api.tour import api_get_tour_by_name
from app.models import Location
from flask import jsonify, redirect, url_for

@app.route('/api/compute-tour/<string:tour_name>', methods=['GET'])
def api_compute_tour(tour_name):
    tour_id = api_get_tour_by_name(tour_name)[0].json['id']

    # For all locations, compute panoramic_images image
    locations = Location.query.filter(Location.tour_id == tour_id).all()
    for location in locations:
        output_path = compute_panoramic(tour_name, location.location_id)
        api_set_panoramic_image(tour_name, location.location_id, output_path)

    # For all locations, compute neighbors
    for location in locations:
        compute_neighbors(tour_name, location.location_id)

    # For all images, blur faces
    for location in locations:
        image_blur_faces(tour_name, location.location_id)

    # For all images, extract text
    for location in locations:
        image_extract_text(tour_name, location.location_id)

    return jsonify({}), 200