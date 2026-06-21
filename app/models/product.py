from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, Numeric, String, Table, Column, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


product_size_association = Table(
    "product_size_association",
    Base.metadata,
    Column("product_id", ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("size_id", ForeignKey("size.id", ondelete="CASCADE"), primary_key=True),
    Column("stock", Integer, default=0, nullable=False),
)


class ProductCategory(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name_ru: Mapped[str] = mapped_column(String(100), nullable=False)
    name_en: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def localized_name(self, lang: str) -> str:
        return self.name_en if lang == "en" else self.name_ru


class ProductBrand(Base):
    __tablename__ = "brand"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    products: Mapped[list["Product"]] = relationship(back_populates="brand")


class ProductSize(Base):
    __tablename__ = "size"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)  # XS, S, M, L, XL

    products: Mapped[list["Product"]] = relationship(
        back_populates="sizes", secondary=product_size_association
    )


class ProductImage(Base):
    __tablename__ = "product_image"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), nullable=False)

    url: Mapped[str] = mapped_column(String(500), nullable=False)
    alt: Mapped[str | None] = mapped_column(String(255), nullable=True)
    order: Mapped[int] = mapped_column(Integer, default=0)

    product: Mapped["Product"] = relationship(back_populates="images")


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    sale_price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    slug: Mapped[str] = mapped_column(String(300), unique=True, nullable=False)
    gender: Mapped[str] = mapped_column(String(20), nullable=False, default="male")
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)

    category_id: Mapped[int | None] = mapped_column(ForeignKey("category.id"), nullable=True)
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brand.id"), nullable=True)

    category: Mapped[Optional["ProductCategory"]] = relationship(back_populates="products")
    brand: Mapped[Optional["ProductBrand"]] = relationship(back_populates="products")
    images: Mapped[list["ProductImage"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    sizes: Mapped[list["ProductSize"]] = relationship(
        back_populates="products", secondary=product_size_association
    )