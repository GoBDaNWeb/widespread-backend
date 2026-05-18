class CategoryNotFound(Exception):
    def __init__(self, category_id: int):
        self.category_id = category_id

class SizesNotFound(Exception):
    def __init__(self, missing_ids: set[int]):
        self.missing_ids = missing_ids

class ProductNotFound(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id

class SizeNotFound(Exception):
    def __init__(self, size_id: int):
        self.size_id = size_id

class ImageNotFound(Exception):
    def __init__(self, image_id: int):
        self.image_id = image_id

class SlugAlreadyExists(Exception):
    def __init__(self, slug: str):
        self.slug = slug

class BrandNotFound(Exception):
    def __init__(self, brand_id: int):
        self.brand_id = brand_id