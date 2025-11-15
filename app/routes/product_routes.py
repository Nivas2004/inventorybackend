from fastapi import APIRouter, HTTPException
from app.schemas import Product
from app.database import products_collection, users_collection
from bson import ObjectId
router = APIRouter()
@router.post("/products/")
async def add_product(product: Product):
    try:
        product_dict = product.dict()
        result = await products_collection.insert_one(product_dict)
        return {
            "id": str(result.inserted_id),
            "name": product.name,
            "category": product.category,
            "supplier": product.supplier,
            "purchasePrice": product.purchasePrice,
            "sellingPrice": product.sellingPrice,
            "stock": product.stock,
        }
    except Exception as e:
        print("🔥 FULL ERROR BELOW 🔥")
        import traceback
        traceback.print_exc()
        print("❌ Add Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/products/")
async def get_all_products():
    try:
        products = []
        cursor = products_collection.find({})
        async for product in cursor:
            products.append({
                "id": str(product["_id"]),
                "name": product["name"],
                "category": product["category"],
                "supplier": product["supplier"],
                "purchasePrice": product["purchasePrice"],
                "sellingPrice": product["sellingPrice"],
                "stock": product["stock"],
            })
        return products

    except Exception as e:
        print("❌ Get Products Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
@router.get("/products/{id}")
async def get_product(id: str):
    try:
        product = await products_collection.find_one({"_id": ObjectId(id)})

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        return {
            "id": str(product["_id"]),
            "name": product["name"],
            "category": product["category"],
            "supplier": product["supplier"],
            "purchasePrice": product["purchasePrice"],
            "sellingPrice": product["sellingPrice"],
            "stock": product["stock"],
        }
    except Exception as e:
        print("❌ Get Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
@router.put("/products/{id}")
async def update_product(id: str, product: Product):
    try:
        result = await products_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": product.dict()}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"message": "Product updated successfully"}
    except Exception as e:
        print("❌ Update Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
@router.delete("/products/{id}")
async def delete_product(id: str):
    try:
        result = await products_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count == 1:
            return {"message": "Product deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Product not found")

    except Exception as e:
        print("❌ Delete Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
async def test_db():
    try:
        await products_collection.find_one({})
        return {"message": "🟢 MongoDB connection OK"}
    except Exception as e:
        return {"message": "🔴 MongoDB connection FAILED", "error": str(e)}
