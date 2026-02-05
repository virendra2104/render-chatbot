import faiss
import numpy as np

print("🔍 Checking FAISS installation...")

# Vector dimension
DIM = 384

# Create FAISS index (CPU)
index = faiss.IndexFlatL2(DIM)

print("✅ FAISS index created")

# Create dummy vectors
vectors = np.random.random((5, DIM)).astype("float32")

# Add vectors to index
index.add(vectors)

print(f"📦 Vectors added to index: {index.ntotal}")

# Search
query = np.random.random((1, DIM)).astype("float32")
distances, indices = index.search(query, k=3)

print("🔎 Search successful")
print("Indices:", indices)
print("Distances:", distances)

print("\n🎉 FAISS is WORKING perfectly on Python 3.13")
