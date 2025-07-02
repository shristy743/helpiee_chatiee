import json, pathlib
import torch, numpy as np
from sentence_transformers import SentenceTransformer, util

class AnswerAgent:
    def __init__(self, kb_path="knowledge_base.json",
                 model_name="all-MiniLM-L6-v2", threshold=0.55):
        self.kb_path   = pathlib.Path(kb_path)
        self.model     = SentenceTransformer(model_name)        # ~90 MB
        self.threshold = threshold
        self._load_kb()

    def _load_kb(self):
        self.kb = json.loads(self.kb_path.read_text())
        self.questions = [item["question"] for item in self.kb]
        self.answers   = [item["answer"]   for item in self.kb]
        # pre‑compute embeddings for speed
        self.q_embeds = self.model.encode(self.questions,
                                          convert_to_tensor=True,
                                          normalize_embeddings=True)

    def respond(self, user_msg):
        u_embed = self.model.encode(user_msg,
                                    convert_to_tensor=True,
                                    normalize_embeddings=True)
        sims = util.cos_sim(u_embed, self.q_embeds).flatten()
        best_idx = int(torch.argmax(sims))
        if sims[best_idx] >= self.threshold:
            return self.answers[best_idx]
        return None  # unknown

    def learn(self, question, answer):
        self.kb.append({"question": question, "answer": answer})
        self.kb_path.write_text(json.dumps(self.kb, indent=2))
        self._load_kb()    # rebuild vectors
