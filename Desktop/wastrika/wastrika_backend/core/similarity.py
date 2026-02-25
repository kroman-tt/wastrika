import numpy as np
import faiss

def find_top_matches(
    query_vector,
    database_path='data/all_embeddings.npy',
    names_path='data/image_names.npy',
    top_n=5
):
    # Load data
    all_embeddings = np.load(database_path)
    image_names = np.load(names_path)

    # Convert to float32 (FAISS requires this)
    all_embeddings = all_embeddings.astype('float32')
    query_vector = query_vector.astype('float32')

    # Normalize vectors (important for cosine similarity)
    faiss.normalize_L2(all_embeddings)
    query_vector = query_vector.reshape(1, -1)
    faiss.normalize_L2(query_vector)

    # Create FAISS index
    dimension = all_embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Add embeddings to index
    index.add(all_embeddings)

    # Search
    similarities, indices = index.search(query_vector, top_n)

    results = []
    for i in range(top_n):
        idx = indices[0][i]
        similarity_score = similarities[0][i]

        results.append({
            "image_name": image_names[idx],
            "score": float(similarity_score)
        })

    return results


if __name__ == "__main__":
    test_query = np.random.rand(2048).astype('float32')
    matches = find_top_matches(test_query)

    print("\nTop 5 Matches:")
    for m in matches:
        print(f"File: {m['image_name']} | Confidence: {m['score']:.4f}")