from fastapi import APIRouter, HTTPException
from app.database import products_collection
from bson import ObjectId

router = APIRouter()

# -------------------------------------------------
# ADD PRODUCT
# -------------------------------------------------
@router.post("/products/")
async def add_product(product: dict):

    # Convert uid → userId
    if "uid" in product:
        product["userId"] = product["uid"]
        del product["uid"]

    if "userId" not in product or not product["userId"]:
        raise HTTPException(status_code=400, detail="userId missing")

    # Convert numeric values
    try:
        product["purchasePrice"] = float(product["purchasePrice"])
        product["sellingPrice"] = float(product["sellingPrice"])
        product["stock"] = int(product["stock"])
    except:
        raise HTTPException(status_code=400, detail="Invalid number format")

    try:
        result = await products_collection.insert_one(product)
        return { "id": str(result.inserted_id), **product }

    except Exception as e:
        print("❌ Add Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# GET ALL PRODUCTS FOR ONE USER
# -------------------------------------------------
@router.get("/products/user/{userId}")
async def get_all_products(userId: str):
    try:
        products = []
        cursor = products_collection.find({"userId": userId})

        async for product in cursor:
            product["id"] = str(product["_id"])
            del product["_id"]
            products.append(product)

        return products

    except Exception as e:
        print("❌ Get Products Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# GET SINGLE PRODUCT
# -------------------------------------------------
@router.get("/products/{id}/{userId}")
async def get_product(id: str, userId: str):

    try:
        product = await products_collection.find_one({"_id": ObjectId(id)})

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product["userId"] != userId:
            raise HTTPException(status_code=403, detail="Access denied")

        product["id"] = str(product["_id"])
        del product["_id"]
        return product

    except Exception as e:
        print("❌ Get Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# UPDATE PRODUCT
# -------------------------------------------------
@router.put("/products/{id}/{userId}")
async def update_product(id: str, userId: str, product: dict):

    try:
        existing = await products_collection.find_one({"_id": ObjectId(id)})

        if not existing:
            raise HTTPException(status_code=404, detail="Product not found")

        if existing["userId"] != userId:
            raise HTTPException(status_code=403, detail="Access denied")

        # Convert uid → userId if sent
        if "uid" in product:
            product["userId"] = product["uid"]
            del product["uid"]

        # Convert numeric fields
        try:
            if "purchasePrice" in product:
                product["purchasePrice"] = float(product["purchasePrice"])
            if "sellingPrice" in product:
                product["sellingPrice"] = float(product["sellingPrice"])
            if "stock" in product:
                product["stock"] = int(product["stock"])
        except:
            raise HTTPException(status_code=400, detail="Invalid data format")

        await products_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": product}
        )

        return {"message": "Product updated successfully"}

    except Exception as e:
        print("❌ Update Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# DELETE PRODUCT
# -------------------------------------------------
@router.delete("/products/{id}/{userId}")
async def delete_product(id: str, userId: str):

    try:
        product = await products_collection.find_one({"_id": ObjectId(id)})

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product["userId"] != userId:
            raise HTTPException(status_code=403, detail="Access denied")

        await products_collection.delete_one({"_id": ObjectId(id)})

        return {"message": "Product deleted successfully"}

    except Exception as e:
        print("❌ Delete Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
