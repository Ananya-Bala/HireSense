from endee import Endee
from sentence_transformers import SentenceTransformer
from data.role_profiles import role_profiles

# Connect to Endee
client = Endee()
client.set_base_url("http://localhost:8080/api/v1")

# Create index if not exists
try:
    print("Creating index 'role_profiles'...")
    client.create_index(
        name="role_profiles",
        dimension=384,
        space_type="cosine",
        precision="float32"
    )
    print("Index created successfully.")
except Exception as e:
    print(f"Index creation failed or already exists: {e}")
    # Try to get the index to see if it exists
    try:
        test_index = client.get_index("role_profiles")
        print("Index already exists, continuing...")
    except Exception as e2:
        print(f"Cannot access index: {e2}")
        raise

index = client.get_index("role_profiles")

model = SentenceTransformer("all-MiniLM-L6-v2")

vectors = []

for role_name, categories in role_profiles.items():

    # Combine all categories into one semantic description
    role_text = f"""
    Role: {role_name}.
    Core Skills: {", ".join(categories['core_skills'])}.
    Tooling Skills: {", ".join(categories['tooling_skills'])}.
    Production Skills: {", ".join(categories['production_skills'])}.
    Research Skills: {", ".join(categories['research_skills'])}.
    """

    embedding = model.encode(role_text).tolist()

    vectors.append({
        "id": role_name,
        "vector": embedding,
        "meta": {
            "role_name": role_name,
            "core_skills": categories["core_skills"],
            "tooling_skills": categories["tooling_skills"],
            "production_skills": categories["production_skills"],
            "research_skills": categories["research_skills"]
        }
    })

# Insert into Endee
index.upsert(vectors)

print("Role profiles inserted successfully.")