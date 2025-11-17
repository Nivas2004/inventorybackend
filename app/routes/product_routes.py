from fastapi import APIRouter, HTTPException
from app.database import products_collection
from bson import ObjectId

router = APIRouter()


# -------------------------------------------------
# ADD PRODUCT
# -------------------------------------------------
@router.post("/products/")
async def add_product(product: dict):

    # Convert uid → userId (if frontend sends uid)
    if "uid" in product:
        product["userId"] = product["uid"]
        del product["uid"]

    # User validation
    if "userId" not in product or not product["userId"]:
        raise HTTPException(status_code=400, detail="userId missing")

    # Convert number fields
    try:
        product["purchasePrice"] = float(product["purchasePrice"])
        product["sellingPrice"] = float(product["sellingPrice"])
        product["stock"] = int(product["stock"])
    except:
        raise HTTPException(status_code=400, detail="Invalid number format")

    try:
        result = await products_collection.insert_one(product)

        return {
            "id": str(result.inserted_id),
            "name": product["name"],
            "category": product["category"],
            "supplier": product["supplier"],
            "purchasePrice": product["purchasePrice"],
            "sellingPrice": product["sellingPrice"],
            "stock": product["stock"],
            "userId": product["userId"],
        }

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

        async for doc in cursor:
            products.append({
                "id": str(doc["_id"]),
                "name": doc["name"],
                "category": doc["category"],
                "supplier": doc["supplier"],
                "purchasePrice": doc["purchasePrice"],
                "sellingPrice": doc["sellingPrice"],
                "stock": doc["stock"],
                "userId": doc["userId"]
            })

        return products

    except Exception as e:
        print("❌ Get Products Error:", e)
        raise HTTPException(status_code=500, detail=str(e))



# -------------------------------------------------
# GET ONE PRODUCT FOR EDIT PAGE
# -------------------------------------------------
@router.get("/products/{id}/{userId}")
async def get_product(id: str, userId: str):

    try:
        doc = await products_collection.find_one({"_id": ObjectId(id)})

        if not doc:
            raise HTTPException(status_code=404, detail="Product not found")

        if doc["userId"] != userId:
            raise HTTPException(status_code=403, detail="Access denied")

        return {
            "id": str(doc["_id"]),
            "name": doc["name"],
            "category": doc["category"],
            "supplier": doc["supplier"],
            "purchasePrice": doc["purchasePrice"],
            "sellingPrice": doc["sellingPrice"],
            "stock": doc["stock"],
            "userId": doc["userId"],
        }

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

        # Convert uid → userId if frontend sends uid
        if "uid" in product:
            product["userId"] = product["uid"]
            del product["uid"]

        # Convert only fields that exist
        try:
            if "purchasePrice" in product:
                product["purchasePrice"] = float(product["purchasePrice"])
            if "sellingPrice" in product:
                product["sellingPrice"] = float(product["sellingPrice"])
            if "stock" in product:
                product["stock"] = int(product["stock"])
        except:
            raise HTTPException(status_code=400, detail="Invalid number format")

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
        doc = await products_collection.find_one({"_id": ObjectId(id)})

        if not doc:
            raise HTTPException(status_code=404, detail="Product not found")

        if doc["userId"] != userId:
            raise HTTPException(status_code=403, detail="Access denied")

        await products_collection.delete_one({"_id": ObjectId(id)})

        return {"message": "Product deleted successfully"}

    except Exception as e:
        print("❌ Delete Product Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
