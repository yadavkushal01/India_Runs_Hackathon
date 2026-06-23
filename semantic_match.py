
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)

def build_candidate_text(candidate):

    profile = candidate.get("profile", {})

    summary = profile.get("summary", "")

    skills = " ".join([
        s.get("name", "")
        for s in candidate.get("skills", [])
    ])

    career = " ".join([
        f"{c.get('title','')} {c.get('description','')}"
        for c in candidate.get(
            "career_history",
            []
        )
    ])

    projects = " ".join([
        p.get("description", "")
        for p in candidate.get(
            "projects",
            []
        )
    ])

    return f"""
    {summary}
    {skills}
    {career}
    {projects}
    """

def encode_text(text):
    return model.encode(
        text,
        normalize_embeddings=True
    )

def semantic_similarity(
    jd_embedding,
    candidate
):
    candidate_text = build_candidate_text(
        candidate
    )

    cand_embedding = encode_text(
        candidate_text
    )

    sim = cosine_similarity(
        [jd_embedding],
        [cand_embedding]
    )[0][0]

    return float(sim)

def prepare_jd_embedding(
    jd_text
):
    return encode_text(jd_text)
