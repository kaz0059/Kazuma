import os, datetime, numpy as np
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from sentence_transformers import SentenceTransformer

AI_NAME = "Ren"

# === Local Embedding Wrapper ===
class LocalEmbedding:
    def __init__(self, model_name="all-MiniLM-L6-v2"): self.model = SentenceTransformer(model_name)
    def get_query_embedding(self,q): return self.model.encode(q).tolist()
    def get_text_embedding(self,t): return self.model.encode(t).tolist()
    def get_text_embedding_batch(self,texts, **kwargs): return [self.model.encode(x).tolist() for x in texts]
    def get_agg_embedding_from_queries(self,queries,**kwargs): return np.mean([self.get_query_embedding(q) for q in queries],axis=0).tolist()

Settings.embed_model = LocalEmbedding()

BASE = os.path.expanduser("~/AI_Assistant")
logpath = os.path.join(BASE,"memory/conversation_log.txt")
knowledge = os.path.join(BASE,"memory/knowledge")
os.makedirs(knowledge, exist_ok=True)

llm = Ollama(model="llama3")

def reflect_and_categorize():
    today = datetime.date.today().strftime("%Y%m%d")
    marker = os.path.join(knowledge, f"done_{today}.flag")
    if os.path.exists(marker) or not os.path.exists(logpath): return

    text = open(logpath,"r",encoding="utf-8").read()
    prompt = f"You are {AI_NAME}, reflecting on today’s dialogue. Categorize into Coding, Design, Research, Personal, Productivity, etc."

    result = str(llm(prompt + "\n\n" + text))
    sections = result.split("\n\n"); category="General"

    for sec in sections:
        if ":" in sec: category = sec.split(":")[0].strip()
        outdir = os.path.join(knowledge, category); os.makedirs(outdir, exist_ok=True)
        with open(os.path.join(outdir,f"journal_{today}.txt"),"a",encoding="utf-8") as f:
            f.write(sec + f"\n\n-- Compiled by {AI_NAME}\n")

    open(marker,"w").write("done")

if __name__=="__main__":
    reflect_and_categorize()
