from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Gender(str, Enum):
    male = "male"
    female = "female"


GENDER_LABELS: dict[str, dict[str, str]] = {
    "ru": {"male": "Мужской", "female": "Женский"},
    "en": {"male": "Male", "female": "Female"},
}


def gender_label(value: str | None, lang: str) -> str | None:
    if value is None:
        return None
    labels = GENDER_LABELS.get(lang, GENDER_LABELS["ru"])
    return labels.get(value, value)


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
    name_ru: str
    name_en: str
    slug: str


class CategoryUpdate(BaseModel):
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    slug: Optional[str] = None


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}

    @classmethod
    def localized(cls, obj, lang: str) -> "CategoryOut":
        return cls(id=obj.id, name=obj.localized_name(lang), slug=obj.slug)


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
    name: str


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
    size_ids: Optional[list[int]] = None


class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    sale_price: Optional[Decimal]
    slug: str
    gender: Optional[Gender]
    gender_label: Optional[str] = None
    is_published: bool
    is_archived: bool
    category: Optional[CategoryOut] = None
    brand: Optional[BrandOut] = None
    images: list[ProductImageOut] = []
    sizes: list[ProductSizeOut] = []

    model_config = {"from_attributes": True}

    @classmethod
    def localized(cls, obj, lang: str) -> "ProductOut":
        return cls(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            price=obj.price,
            sale_price=obj.sale_price,
            slug=obj.slug,
            gender=obj.gender,
            gender_label=gender_label(obj.gender, lang),
            is_published=obj.is_published,
            is_archived=obj.is_archived,
            category=CategoryOut.localized(obj.category, lang) if obj.category else None,
            brand=BrandOut.model_validate(obj.brand) if obj.brand else None,
            images=[ProductImageOut.model_validate(i) for i in obj.images],
            sizes=[ProductSizeOut.model_validate(s) for s in obj.sizes],
        )


class ProductListOut(BaseModel):
    items: list[ProductOut]
    total: int
    page: int
    page_size: int
    pages: int


class PriceStats(BaseModel):
    min: Optional[Decimal] = None
    max: Optional[Decimal] = None
    avg: Optional[Decimal] = None


class CategoryStat(BaseModel):
    id: int
    name: str
    count: int


class BrandStat(BaseModel):
    id: int
    name: str
    count: int


class GenderStats(BaseModel):
    male: int = 0
    female: int = 0


class PriceBucket(BaseModel):
    from_: Decimal = Field(alias="from")
    to: Optional[Decimal] = None
    count: int

    model_config = {"populate_by_name": True}


class ProductStats(BaseModel):
    total: int
    published: int
    archived: int
    drafts: int
    on_sale: int
    price: PriceStats
    by_category: list[CategoryStat]
    by_brand: list[BrandStat]
    by_gender: GenderStats
    price_buckets: list[PriceBucket]
