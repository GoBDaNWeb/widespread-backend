import math
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.dependencies.i18n import get_language
from app.dependencies.services import get_product_service
from app.schemas.product import CategoryCreate, CategoryOut, CategoryUpdate, ProductCreate, ProductOut, ProductUpdate, \
    ProductSizeCreate, ProductSizeUpdate, ProductImageCreate, ProductImageUpdate, ProductListOut, BrandCreate, \
    BrandUpdate, ProductFilters, Gender, ProductSortField, SortOrder, ProductStats


category_router = APIRouter(prefix="/categories", tags=["Product/Category"])

@category_router.post("/create_category", response_model=CategoryOut)
async def create_category(data: CategoryCreate, service=Depends(get_product_service), lang: str = Depends(get_language)):
    return await service.create_category(data, lang)

@category_router.get("/get_categories", response_model=list[CategoryOut])
async def get_categories(service=Depends(get_product_service), lang: str = Depends(get_language)):
    return await service.get_categories(lang)

@category_router.get("/get_category/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int, service=Depends(get_product_service), lang: str = Depends(get_language)):
    return await service.get_category(category_id, lang)

@category_router.patch("/update_category/{category_id}", response_model=CategoryOut)
async def update_category(category_id: int, data: CategoryUpdate, service=Depends(get_product_service), lang: str = Depends(get_language)):
    return await service.update_category(category_id, data, lang)


@category_router.delete("/delete_category/{category_id}")
async def delete_category(category_id: int, service=Depends(get_product_service)):
    return await service.delete_category(category_id)


product_router = APIRouter(prefix="/products", tags=["Product"])

@product_router.post("/create_product", response_model=ProductOut)
async def create_product(data: ProductCreate, service=Depends(get_product_service), lang: str = Depends(get_language)):
    return await service.create_product(data, lang)

@product_router.get("/stats", response_model=ProductStats)
async def get_stats(service=Depends(get_product_service), lang: str = Depends(get_language)):
    return await service.get_stats(lang)

@product_router.get("/get_product/{product_id}", response_model=ProductOut)
async def get_product(product_id: int, service=Depends(get_product_service), lang: str = Depends(get_language)):
    return await service.get_product(product_id, lang)


@product_router.get("/get_products", response_model=ProductListOut)
async def get_products(
    search: str | None = None,
    category_id: int | None = None,
    brand_id: int | None = None,
    gender: Gender | None = None,
    is_published: bool | None = None,
    is_archived: bool | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
    size_ids: Annotated[list[int] | None, Query()] = None,
    sort_by: ProductSortField = ProductSortField.id,
    order: SortOrder = SortOrder.asc,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    service=Depends(get_product_service),
    lang: str = Depends(get_language),

):
    filters = ProductFilters(
        search=search,
        category_id=category_id,
        brand_id=brand_id,
        gender=gender,
        is_published=is_published,
        is_archived=is_archived,
        min_price=min_price,
        max_price=max_price,
        size_ids=size_ids,
        sort_by=sort_by,
        order=order,
    )
    items, total = await service.get_products(page, page_size, filters, lang)

    return ProductListOut(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        pages=math.ceil(total / page_size) if total else 0,
    )

@product_router.patch("/update_product/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, data: ProductUpdate, service=Depends(get_product_service), lang: str = Depends(get_language)):
    return await service.update_product(product_id, data, lang)


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