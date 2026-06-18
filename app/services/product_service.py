from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import CategoryNotFound, SizesNotFound, SlugAlreadyExists, ProductNotFound, SizeNotFound, \
    ImageNotFound, BrandNotFound
from app.repositories.product_repo import ProductRepository
from app.schemas.product import CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate, ProductSizeCreate, \
    ProductSizeUpdate, ProductImageCreate, ProductImageUpdate, BrandCreate, BrandUpdate, ProductFilters


class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def create_category(self, data: CategoryCreate):
        return await self.product_repo.create_category(data)

    async def get_categories(self):
        return await self.product_repo.get_categories()

    async def get_category(self, category_id: int):
        try:
            return await self.product_repo.get_category(category_id)
        except CategoryNotFound:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")

    async def update_category(self, category_id: int, data: CategoryUpdate):
        try:
            return await self.product_repo.update_category(category_id, data)
        except CategoryNotFound:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")

    async def delete_category(self, category_id: int):
        try:
            return await self.product_repo.delete_category(category_id)
        except CategoryNotFound:
            raise HTTPException(status_code=404, detail=f"Category {category_id} not found")

    async def create_product(self, data: ProductCreate):
        try:
            return await self.product_repo.create_product(data)
        except CategoryNotFound as e:
            raise HTTPException(status_code=404, detail=f"Category {e.category_id} not found")
        except BrandNotFound as e:
            raise HTTPException(status_code=404, detail=f"Brand {e.brand_id} not found")
        except SizesNotFound as e:
            raise HTTPException(status_code=422, detail=f"Size IDs not found: {sorted(e.missing_ids)}")
        except SlugAlreadyExists as e:
            raise HTTPException(status_code=409, detail=f"Slug '{e.slug}' already exists")
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Data integrity error")

    async def get_product(self, product_id: int):
        try:
            return await self.product_repo.get_product(product_id)
        except ProductNotFound:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    async def get_products(self, page: int, page_size: int, filters: ProductFilters | None = None):
        return await self.product_repo.get_products(page, page_size, filters)

    async def get_stats(self):
        return await self.product_repo.get_stats()

    async def update_product(self, product_id: int, data: ProductUpdate):
        try:
            return await self.product_repo.update_product(product_id, data)
        except ProductNotFound:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        except CategoryNotFound as e:
            raise HTTPException(status_code=404, detail=f"Category {e.category_id} not found")
        except BrandNotFound as e:
            raise HTTPException(status_code=404, detail=f"Brand {e.brand_id} not found")
        except SizesNotFound as e:
            raise HTTPException(status_code=422, detail=f"Size IDs not found: {sorted(e.missing_ids)}")
        except SlugAlreadyExists as e:
            raise HTTPException(status_code=409, detail=f"Slug '{e.slug}' already exists")
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Data integrity error")

    async def delete_product(self, product_id: int):
        try:
            return await self.product_repo.delete_product(product_id)
        except ProductNotFound:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")

    async def get_sizes(self):
        return await self.product_repo.get_sizes()

    async def get_size(self, size_id: int):
        try:
            return await self.product_repo.get_size(size_id)
        except SizeNotFound:
            raise HTTPException(status_code=404, detail=f"Size {size_id} not found")

    async def create_size(self, data: ProductSizeCreate):
        return await self.product_repo.create_size(data)

    async def update_size(self, size_id: int, data: ProductSizeUpdate):
        try:
            return await self.product_repo.update_size(size_id, data)
        except SizeNotFound:
            raise HTTPException(status_code=404, detail=f"Size {size_id} not found")

    async def delete_size(self, size_id: int):
        try:
            return await self.product_repo.delete_size(size_id)
        except SizeNotFound:
            raise HTTPException(status_code=404, detail=f"Size {size_id} not found")

    async def get_images_by_product(self, product_id: int):
        return await self.product_repo.get_images_by_product(product_id)

    async def get_image(self, image_id: int):
        try:
            return await self.product_repo.get_image(image_id)
        except ImageNotFound:
            raise HTTPException(status_code=404, detail=f"Image {image_id} not found")

    async def create_image(self, data: ProductImageCreate):
        try:
            return await self.product_repo.create_image(data)
        except ProductNotFound:
            raise HTTPException(status_code=404, detail=f"Product {data.product_id} not found")

    async def update_image(self, image_id: int, data: ProductImageUpdate):
        try:
            return await self.product_repo.update_image(image_id, data)
        except ImageNotFound:
            raise HTTPException(status_code=404, detail=f"Image {image_id} not found")

    async def delete_image(self, image_id: int):
        try:
            return await self.product_repo.delete_image(image_id)
        except ImageNotFound:
            raise HTTPException(status_code=404, detail=f"Image {image_id} not found")

    async def create_brand(self, data: BrandCreate):
        try:
            return await self.product_repo.create_brand(data)
        except SlugAlreadyExists as e:
            raise HTTPException(status_code=409, detail=f"Slug '{e.slug}' already exists")

    async def get_brands(self):
        return await self.product_repo.get_brands()

    async def get_brand(self, brand_id: int):
        try:
            return await self.product_repo.get_brand(brand_id)
        except BrandNotFound:
            raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")

    async def update_brand(self, brand_id: int, data: BrandUpdate):
        try:
            return await self.product_repo.update_brand(brand_id, data)
        except BrandNotFound:
            raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")
        except SlugAlreadyExists as e:
            raise HTTPException(status_code=409, detail=f"Slug '{e.slug}' already exists")

    async def delete_brand(self, brand_id: int):
        try:
            return await self.product_repo.delete_brand(brand_id)
        except BrandNotFound:
            raise HTTPException(status_code=404, detail=f"Brand {brand_id} not found")