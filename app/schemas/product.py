from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Gender(str, Enum):
    male = "male"
    female = "female"


class ProductSortField(str, Enum):
    id = "id"
    title = "title"
    price = "price"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class ProductFilters(BaseModel):
    search: Optional[str] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    gender: Optional[Gender] = None
    is_published: Optional[bool] = None
    is_archived: Optional[bool] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    size_ids: Optional[list[int]] = None
    sort_by: ProductSortField = ProductSortField.id
    order: SortOrder = SortOrder.asc


class CategoryCreate(BaseModel):
    name: str
    slug: str


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


class BrandCreate(BaseModel):
    name: str
    slug: str


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None


class BrandOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


class ProductImageCreate(BaseModel):
    product_id: int
    url: str
    alt: Optional[str] = None
    order: int = 0


class ProductImageUpdate(BaseModel):
    url: Optional[str] = None
    alt: Optional[str] = None
    order: Optional[int] = None


class ProductImageOut(BaseModel):
    id: int
    product_id: int
    url: str
    alt: Optional[str]
    order: int

    model_config = {"from_attributes": True}


class ProductSizeCreate(BaseModel):
    name: str  # XS, S, M, L, XL


class ProductSizeUpdate(BaseModel):
    name: Optional[str] = None


class ProductSizeOut(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    title: str
    description: str
    price: Decimal
    sale_price: Optional[Decimal] = None
    slug: str
    gender: Gender = Gender.male
    is_published: bool = False
    is_archived: bool = False
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    # IDs уже существующих размеров из таблицы product_size
    size_ids: list[int] = []


class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    sale_price: Optional[Decimal] = None
    slug: Optional[str] = None
    gender: Optional[Gender] = None
    is_published: Optional[bool] = None
    is_archived: Optional[bool] = None
    category_id: Optional[int] = None
    brand_id: Optional[int] = None
    # Передай новый полный список ID размеров — заменит текущий
    size_ids: Optional[list[int]] = None


class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    sale_price: Optional[Decimal]
    slug: str
    gender: Optional[Gender]
    is_published: bool
    is_archived: bool
    category: Optional[CategoryOut] = None
    brand: Optional[BrandOut] = None
    images: list[ProductImageOut] = []
    sizes: list[ProductSizeOut] = []

    model_config = {"from_attributes": True}


class ProductListOut(BaseModel):
    items: list[ProductOut]
    total: int
    page: int
    page_size: int
    pages: int
