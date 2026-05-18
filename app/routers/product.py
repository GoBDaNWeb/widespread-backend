import math

from fastapi import APIRouter, Depends, Query

from app.dependencies.services import get_product_service
from app.schemas.product import CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate, ProductSizeCreate, \
    ProductSizeUpdate, ProductImageCreate, ProductImageUpdate, ProductListOut, BrandCreate, BrandUpdate

category_router = APIRouter(prefix="/categories", tags=["Product/Category"])

@category_router.post("/create_category")
async def create_category(data: CategoryCreate, service=Depends(get_product_service)):
    return await service.create_category(data)

@category_router.get("/get_categories")
async def get_categories(service=Depends(get_product_service)):
    return await service.get_categories()

@category_router.get("/get_category/{category_id}")
async def get_category(category_id: int, service=Depends(get_product_service)):
    return await service.get_category(category_id)

@category_router.patch("/update_category/{category_id}")
async def update_category(category_id: int, data: CategoryUpdate, service=Depends(get_product_service)):
    return await service.update_category(category_id, data)

@category_router.delete("/delete_category/{category_id}")
async def delete_category(category_id: int, service=Depends(get_product_service)):
    return await service.delete_category(category_id)


product_router = APIRouter(prefix="/products", tags=["Product"])

@product_router.post("/create_product")
async def create_product(data: ProductCreate, service=Depends(get_product_service)):
    return await service.create_product(data)

@product_router.get("/get_product/{product_id}")
async def get_product(product_id: int, service=Depends(get_product_service)):
    return await service.get_product(product_id)

@product_router.get("/get_products", response_model=ProductListOut)
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service=Depends(get_product_service),
):
    items, total = await service.get_products(page, page_size)
    return ProductListOut(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total else 0,
    )

@product_router.patch("/update_product/{product_id}")
async def update_product(product_id: int, data: ProductUpdate, service=Depends(get_product_service)):
    return await service.update_product(product_id, data)

@product_router.delete("/delete_product/{product_id}")
async def delete_product(product_id: int, service=Depends(get_product_service)):
    print(product_id)
    return await service.delete_product(product_id)


sizes_router = APIRouter(prefix="/sizes", tags=["Product/Size"])

@sizes_router.get("/get_sizes")
async def get_sizes(service=Depends(get_product_service)):
    return await service.get_sizes()

@sizes_router.get("/get_size/{size_id}")
async def get_size(size_id: int, service=Depends(get_product_service)):
    return await service.get_size(size_id)

@sizes_router.post("/create_size")
async def create_size(data: ProductSizeCreate, service=Depends(get_product_service)):
    return await service.create_size(data)

@sizes_router.patch("/update_size/{size_id}")
async def update_size(size_id: int, data: ProductSizeUpdate, service=Depends(get_product_service)):
    return await service.update_size(size_id,data)

@sizes_router.delete("/delete_size/{size_id}")
async def delete_size(size_id: int, service=Depends(get_product_service)):
    return await service.delete_size(size_id)

brand_router = APIRouter(prefix="/brands", tags=["Product/Brand"])

@brand_router.post("/create_brand")
async def create_brand(data: BrandCreate, service=Depends(get_product_service)):
    return await service.create_brand(data)

@brand_router.get("/get_brands")
async def get_brands(service=Depends(get_product_service)):
    return await service.get_brands()

@brand_router.get("/get_brand/{brand_id}")
async def get_brand(brand_id: int, service=Depends(get_product_service)):
    return await service.get_brand(brand_id)

@brand_router.patch("/update_brand/{brand_id}")
async def update_brand(brand_id: int, data: BrandUpdate, service=Depends(get_product_service)):
    return await service.update_brand(brand_id, data)

@brand_router.delete("/delete_brand/{brand_id}")
async def delete_brand(brand_id: int, service=Depends(get_product_service)):
    return await service.delete_brand(brand_id)


image_router = APIRouter(prefix="/images", tags=["Image"])

@image_router.get("/get_images_by_product/{product_id}")
async def get_images_by_product(product_id: int, service=Depends(get_product_service)):
    return await service.get_images_by_product(product_id)

@image_router.get("/get_image/{image_id}")
async def get_image(image_id: int, service=Depends(get_product_service)):
    return await service.get_image(image_id)

@image_router.post("/create_image")
async def create_image(data: ProductImageCreate, service=Depends(get_product_service)):
    return await service.create_image(data)

@image_router.patch("/update_image/{image_id}")
async def update_image(image_id: int, data: ProductImageUpdate, service=Depends(get_product_service)):
    return await service.update_image(image_id, data)

@image_router.delete("/delete_image/{image_id}")
async def delete_image(image_id: int, service=Depends(get_product_service)):
    return await service.delete_image(image_id)