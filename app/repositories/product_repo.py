from abc import abstractmethod, ABC
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select, func, or_, and_

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.core.exceptions import CategoryNotFound, SizesNotFound, ProductNotFound, SlugAlreadyExists, SizeNotFound, \
    ImageNotFound, BrandNotFound
from app.models.product import Product, ProductSize, ProductCategory, ProductImage, ProductBrand, product_size_association
from app.schemas.product import CategoryCreate, CategoryUpdate, ProductCreate, ProductUpdate, ProductSizeCreate, \
    ProductSizeUpdate, ProductImageCreate, ProductImageUpdate, BrandCreate, BrandUpdate, ProductFilters, \
    ProductSortField, SortOrder, ProductStats, PriceStats, CategoryStat, BrandStat, GenderStats, PriceBucket, Gender


PRICE_BUCKETS: list[tuple[int, int | None]] = [
    (0, 50),
    (50, 100),
    (100, 200),
    (200, 500),
    (500, 1000),
    (1000, None),
]


class ProductRepository(ABC):
    @abstractmethod
    async def create_category(self, data: CategoryCreate) -> ProductCategory:
        pass

    @abstractmethod
    async def get_categories(self) -> Sequence[ProductCategory]:
        pass

    @abstractmethod
    async def get_category(self, category_id: int):
        pass

    @abstractmethod
    async def update_category(self, category_id: int, data) -> ProductCategory:
        pass

    @abstractmethod
    async def delete_category(self, category_id: int):
        pass

    @abstractmethod
    async def create_product(self, data: ProductCreate):
        pass

    @abstractmethod
    async def get_product(self, product_id: int):
        pass

    @abstractmethod
    async def get_products(self, page: int, page_size: int, filters: "ProductFilters | None" = None):
        pass

    @abstractmethod
    async def get_stats(self, lang: str = "ru"):
        pass

    @abstractmethod
    async def update_product(self, product_id: int, data: ProductUpdate):
        pass

    @abstractmethod
    async def delete_product(self, product_id: int):
        pass

    @abstractmethod
    async def get_sizes(self):
        pass

    @abstractmethod
    async def get_size(self, size_id: int):
        pass

    @abstractmethod
    async def create_size(self, data: ProductSizeCreate):
        pass

    @abstractmethod
    async def update_size(self, size_id: int, data: ProductSizeUpdate):
        pass

    @abstractmethod
    async def delete_size(self, size_id: int):
        pass

    @abstractmethod
    async def get_images_by_product(self, product_id: int) -> Sequence[ProductImage]:
        pass

    @abstractmethod
    async def get_image(self, image_id: int) -> ProductImage:
        pass

    @abstractmethod
    async def create_image(self, data: ProductImageCreate) -> ProductImage:
        pass

    @abstractmethod
    async def update_image(self, image_id: int, data: ProductImageUpdate) -> ProductImage:
        pass

    @abstractmethod
    async def delete_image(self, image_id: int) -> None:
        pass

    @abstractmethod
    async def create_brand(self, data: BrandCreate) -> ProductBrand:
        pass

    @abstractmethod
    async def get_brands(self) -> Sequence[ProductBrand]:
        pass

    @abstractmethod
    async def get_brand(self, brand_id: int) -> ProductBrand:
        pass

    @abstractmethod
    async def update_brand(self, brand_id: int, data: BrandUpdate) -> ProductBrand:
        pass

    @abstractmethod
    async def delete_brand(self, brand_id: int) -> None:
        pass


class SQLAlchemyProductRepository:
    def __init__(self, session):
        self.session = session

    async def create_category(self, data: CategoryCreate) -> ProductCategory:
        obj = ProductCategory(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_categories(self) -> Sequence[ProductCategory]:
        stmt = select(ProductCategory)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_category(self, category_id: int) -> ProductCategory:
        stmt = select(ProductCategory).where(ProductCategory.id == category_id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise CategoryNotFound(category_id)
        return obj

    async def update_category(self, category_id: int, data: CategoryUpdate) -> ProductCategory:
        obj = await self.get_category(category_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete_category(self, category_id: int) -> None:
        obj = await self.get_category(category_id)
        await self.session.delete(obj)
        await self.session.commit()

    @staticmethod
    def _product_query():
        return select(Product).options(
            selectinload(Product.images),
            selectinload(Product.sizes),
            selectinload(Product.category),
            selectinload(Product.brand),
        )

    async def _resolve_sizes(self, size_ids: list[int]) -> list[ProductSize]:
        if not size_ids:
            return []
        stmt = select(ProductSize).where(ProductSize.id.in_(size_ids))
        result = await self.session.execute(stmt)
        found = result.scalars().all()
        if len(found) != len(size_ids):
            found_ids = {s.id for s in found}
            missing = set(size_ids) - found_ids
            raise SizesNotFound(missing)
        return list(found)

    async def get_product(self, product_id: int) -> Product:
        stmt = self._product_query().where(Product.id == product_id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise ProductNotFound(product_id)
        return obj

    @staticmethod
    def _build_filter_conditions(filters: ProductFilters | None) -> list:
        conditions = []
        if filters is None:
            return conditions

        if filters.search:
            pattern = f"%{filters.search}%"
            conditions.append(
                or_(Product.title.ilike(pattern), Product.description.ilike(pattern))
            )
        if filters.category_id is not None:
            conditions.append(Product.category_id == filters.category_id)
        if filters.brand_id is not None:
            conditions.append(Product.brand_id == filters.brand_id)
        if filters.gender is not None:
            conditions.append(Product.gender == filters.gender.value)
        if filters.is_published is not None:
            conditions.append(Product.is_published == filters.is_published)
        if filters.is_archived is not None:
            conditions.append(Product.is_archived == filters.is_archived)
        if filters.min_price is not None:
            conditions.append(Product.price >= filters.min_price)
        if filters.max_price is not None:
            conditions.append(Product.price <= filters.max_price)
        if filters.size_ids:
            size_subq = (
                select(product_size_association.c.product_id)
                .where(product_size_association.c.size_id.in_(filters.size_ids))
                .group_by(product_size_association.c.product_id)
                .having(func.count() == len(filters.size_ids))
            )
            conditions.append(Product.id.in_(size_subq))
        return conditions

    @staticmethod
    def _build_order_by(filters: ProductFilters | None):
        sort_by = filters.sort_by if filters else ProductSortField.id
        order = filters.order if filters else SortOrder.asc
        column = {
            ProductSortField.id: Product.id,
            ProductSortField.title: Product.title,
            ProductSortField.price: Product.price,
        }[sort_by]
        return column.desc() if order == SortOrder.desc else column.asc()

    async def get_products(
        self, page: int, page_size: int, filters: ProductFilters | None = None
    ) -> tuple[Sequence[Product], int]:
        conditions = self._build_filter_conditions(filters)

        count_stmt = select(func.count()).select_from(Product)
        if conditions:
            count_stmt = count_stmt.where(*conditions)
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one()

        offset = (page - 1) * page_size
        stmt = self._product_query()
        if conditions:
            stmt = stmt.where(*conditions)
        stmt = stmt.order_by(self._build_order_by(filters)).offset(offset).limit(page_size)
        result = await self.session.execute(stmt)
        return result.scalars().all(), total

    async def get_stats(self, lang: str = "ru") -> ProductStats:
        bucket_cols = []
        for i, (lo, hi) in enumerate(PRICE_BUCKETS):
            cond = Product.price >= lo if hi is None else and_(Product.price >= lo, Product.price < hi)
            bucket_cols.append(func.count().filter(cond).label(f"bucket_{i}"))

        agg_stmt = select(
            func.count().label("total"),
            func.count().filter(Product.is_published.is_(True)).label("published"),
            func.count().filter(Product.is_archived.is_(True)).label("archived"),
            func.count().filter(
                Product.is_published.is_(False), Product.is_archived.is_(False)
            ).label("drafts"),
            func.count().filter(Product.sale_price.isnot(None)).label("on_sale"),
            func.min(Product.price).label("min_price"),
            func.max(Product.price).label("max_price"),
            func.avg(Product.price).label("avg_price"),
            func.count().filter(Product.gender == Gender.male.value).label("male"),
            func.count().filter(Product.gender == Gender.female.value).label("female"),
            *bucket_cols,
        )
        agg = (await self.session.execute(agg_stmt)).one()

        category_name = ProductCategory.name_en if lang == "en" else ProductCategory.name_ru
        category_stmt = (
            select(ProductCategory.id, category_name.label("name"), func.count(Product.id).label("count"))
            .join(Product, Product.category_id == ProductCategory.id)
            .group_by(ProductCategory.id, category_name)
            .order_by(func.count(Product.id).desc())
        )
        categories = (await self.session.execute(category_stmt)).all()

        brand_stmt = (
            select(ProductBrand.id, ProductBrand.name, func.count(Product.id).label("count"))
            .join(Product, Product.brand_id == ProductBrand.id)
            .group_by(ProductBrand.id, ProductBrand.name)
            .order_by(func.count(Product.id).desc())
        )
        brands = (await self.session.execute(brand_stmt)).all()

        return ProductStats(
            total=agg.total,
            published=agg.published,
            archived=agg.archived,
            drafts=agg.drafts,
            on_sale=agg.on_sale,
            price=PriceStats(
                min=agg.min_price,
                max=agg.max_price,
                avg=round(agg.avg_price, 2) if agg.avg_price is not None else None,
            ),
            by_category=[CategoryStat(id=c.id, name=c.name, count=c.count) for c in categories],
            by_brand=[BrandStat(id=b.id, name=b.name, count=b.count) for b in brands],
            by_gender=GenderStats(male=agg.male, female=agg.female),
            price_buckets=[
                PriceBucket(**{"from": lo, "to": hi, "count": getattr(agg, f"bucket_{i}")})
                for i, (lo, hi) in enumerate(PRICE_BUCKETS)
            ],
        )

    async def create_product(self, data: ProductCreate) -> Product:
        if data.category_id:
            await self.get_category(data.category_id)
        if data.brand_id:
            await self.get_brand(data.brand_id)

        sizes = await self._resolve_sizes(data.size_ids)

        payload = data.model_dump(exclude={"size_ids"})
        obj = Product(**payload)
        obj.sizes = sizes
        self.session.add(obj)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            if "product_slug_key" in str(e):
                raise SlugAlreadyExists(data.slug)
            raise
        await self.session.refresh(obj)
        return await self.get_product(obj.id)

    async def update_product(self, product_id: int, data: ProductUpdate) -> Product:
        obj = await self.get_product(product_id)  # бросит ProductNotFound

        update_data = data.model_dump(exclude_unset=True)
        size_ids = update_data.pop("size_ids", None)

        if "category_id" in update_data and update_data["category_id"] is not None:
            await self.get_category(update_data["category_id"])
        if "brand_id" in update_data and update_data["brand_id"] is not None:
            await self.get_brand(update_data["brand_id"])

        for field, value in update_data.items():
            setattr(obj, field, value)

        if size_ids is not None:
            obj.sizes = await self._resolve_sizes(size_ids)

        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            if "product_slug_key" in str(e):
                raise SlugAlreadyExists(update_data.get("slug", ""))
            raise
        return await self.get_product(product_id)

    async def delete_product(self, product_id: int) -> None:
        obj = await self.get_product(product_id)
        await self.session.delete(obj)
        await self.session.commit()

    async def get_sizes(self) -> Sequence[ProductSize]:
        stmt = select(ProductSize)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_size(self, size_id: int) -> ProductSize:
        stmt = select(ProductSize).where(ProductSize.id == size_id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise SizeNotFound(size_id)
        return obj

    async def create_size(self, data: ProductSizeCreate) -> ProductSize:
        obj = ProductSize(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj


    async def update_size(self, size_id: int, data: ProductSizeUpdate) -> ProductSize:
        obj = await self.get_size(size_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj


    async def delete_size(self, size_id: int):
        obj = await self.get_size(size_id)
        await self.session.delete(obj)
        await self.session.commit()

    async def get_images_by_product(self, product_id: int) -> Sequence[ProductImage]:
        stmt = select(ProductImage).where(ProductImage.product_id == product_id).order_by(ProductImage.order)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_image(self, image_id: int) -> ProductImage:
        stmt = select(ProductImage).where(ProductImage.id == image_id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise ImageNotFound(image_id)
        return obj

    async def create_image(self, data: ProductImageCreate) -> ProductImage:
        # проверяем что продукт существует
        await self.get_product(data.product_id)
        obj = ProductImage(**data.model_dump())
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update_image(self, image_id: int, data: ProductImageUpdate) -> ProductImage:
        obj = await self.get_image(image_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete_image(self, image_id: int) -> None:
        obj = await self.get_image(image_id)
        await self.session.delete(obj)
        await self.session.commit()

    async def create_brand(self, data: BrandCreate) -> ProductBrand:
        obj = ProductBrand(**data.model_dump())
        self.session.add(obj)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            if "brand_slug_key" in str(e):
                raise SlugAlreadyExists(data.slug)
            raise
        await self.session.refresh(obj)
        return obj

    async def get_brands(self) -> Sequence[ProductBrand]:
        stmt = select(ProductBrand)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_brand(self, brand_id: int) -> ProductBrand:
        stmt = select(ProductBrand).where(ProductBrand.id == brand_id)
        result = await self.session.execute(stmt)
        obj = result.scalar_one_or_none()
        if not obj:
            raise BrandNotFound(brand_id)
        return obj

    async def update_brand(self, brand_id: int, data: BrandUpdate) -> ProductBrand:
        obj = await self.get_brand(brand_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        try:
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            if "brand_slug_key" in str(e):
                raise SlugAlreadyExists(data.slug or "")
            raise
        await self.session.refresh(obj)
        return obj

    async def delete_brand(self, brand_id: int) -> None:
        obj = await self.get_brand(brand_id)
        await self.session.delete(obj)
        await self.session.commit()
