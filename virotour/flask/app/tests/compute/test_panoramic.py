from PIL import Image
from app.api.compute.compute import compute_panoramic
from app.tests.images.test_add_images import get_image_paths
from app.tests.common_utils import add_tour, upload_images, get_panoramic_image


def test_compute_panoramic(client):
    tour_name = "Tour 1"
    add_tour(client, tour_name, "Tour Description Example")
    image_paths = get_image_paths('input_images/location1')
    upload_images(client, tour_name, image_paths)

    data = compute_panoramic(tour_name, 1)
