"""
Bước 3 — RAGAS Evaluation
===========================
NHIỆM VỤ:
  1. Chạy 50 QA pairs qua CẢ 2 prompt version, lưu answers + contexts
  2. Tạo EvaluationDataset với các SingleTurnSample object
  3. Đánh giá với 4 RAGAS metrics: faithfulness, answer_relevancy,
     context_recall, context_precision
  4. In bảng so sánh V1 vs V2
  5. Lưu kết quả vào data/ragas_report.json

DELIVERABLE: faithfulness ≥ 0.8 cho ít nhất 1 prompt version
             + file data/ragas_report.json được tạo ra

⏰ LƯU Ý: Bước này mất ~15-30 phút. Hãy bắt đầu sớm!
"""
import sys
import json
import warnings
import unicodedata
warnings.filterwarnings("ignore")

from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def _configure_ascii_streams() -> None:
    """Prevent Windows CP1252 consoles from failing on Unicode output."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="ascii", errors="ignore")


def _ascii_text(value) -> str:
    """Convert dynamic console text to readable ASCII without Vietnamese marks."""
    text = str(value).replace("Đ", "D").replace("đ", "d")
    text = unicodedata.normalize("NFKD", text)
    return (
        "".join(char for char in text if not unicodedata.combining(char))
        .encode("ascii", errors="ignore")
        .decode("ascii")
    )


_configure_ascii_streams()

import config  # ⚠️ phải import trước LangChain

import numpy as np
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from ragas import evaluate, EvaluationDataset, SingleTurnSample
from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision

from utils.llm_factory import get_llm, get_embeddings
from utils.data_loader import load_knowledge_base, split_text, build_vectorstore
from qa_pairs import QA_PAIRS


# ── 1. Prompt Templates (copy từ Bước 2) ──────────────────────────────────
# SYSTEM_V1 and SYSTEM_V2 mirror the approved prompts from step 2.
SYSTEM_V1 = (
    "You are a friendly AI assistant. Use only the supplied context to answer "
    "the question. Keep the answer concise and clear in 2-4 sentences. "
    "If the context does not contain the answer, say that you do not have "
    "enough information instead of guessing.\n\n"
    "Context:\n{context}"
)
PROMPT_V1 = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_V1),
    ("human",  "{question}"),
])

SYSTEM_V2 = (
    "You are an expert information analyst. Answer using only facts explicitly "
    "stated in the supplied context. Write 2-3 concise sentences: give the "
    "direct answer first, followed only by essential supporting facts from the "
    "context. Do not add general knowledge, examples, confidence statements, "
    "causes, implications, or conclusions unless they are explicitly present "
    "in the context. If the context is insufficient, state only that the "
    "information is unavailable.\n\n"
    "Context:\n{context}"
)
PROMPT_V2 = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_V2),
    ("human",  "{question}"),
])

PROMPTS = {"v1": PROMPT_V1, "v2": PROMPT_V2}


# ── 2. Setup Vectorstore ───────────────────────────────────────────────────
def setup_vectorstore():
    """Tái sử dụng — tạo FAISS vectorstore từ knowledge base."""
    embeddings  = get_embeddings()
    text        = load_knowledge_base()
    chunks      = split_text(text, chunk_size=500, chunk_overlap=50)
    return build_vectorstore(chunks, embeddings)


# ── 3. Chạy RAG và thu thập kết quả ───────────────────────────────────────
def run_rag(retriever, llm, prompt, question: str) -> dict:
    """
    Chạy RAG chain cho 1 câu hỏi.

    ⚠️ QUAN TRỌNG: trả về contexts là LIST of strings, KHÔNG phải string đã ghép!
    RAGAS cần từng đoạn riêng để tính context_recall và context_precision.

    Trả về: {"answer": str, "contexts": list[str]}
    """
    docs = retriever.invoke(question)

    contexts = [doc.page_content for doc in docs]
    if not contexts:
        raise ValueError(f"Retriever returned no context for question: {question}")
    if not all(isinstance(context, str) for context in contexts):
        raise TypeError("retrieved contexts must be a list[str]")

    ctx_str = "\n\n".join(contexts)

    answer = (prompt | llm | StrOutputParser()).invoke({
        "context": ctx_str,
        "question": question,
    })

    return {"answer": str(answer), "contexts": contexts}


def collect_rag_outputs(vectorstore, prompt_version: str) -> list:
    """
    Chạy tất cả 50 QA pairs qua prompt version được chỉ định.
    Trả về: list of dict với keys: question, reference, answer, contexts
    """
    if prompt_version not in PROMPTS:
        raise ValueError(f"Unknown prompt version: {prompt_version}")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm       = get_llm()
    prompt    = PROMPTS[prompt_version]

    results = []
    print(f"\nRunning {len(QA_PAIRS)} questions with prompt {prompt_version} ...")

    for i, qa in enumerate(QA_PAIRS, 1):
        out = run_rag(retriever, llm, prompt, qa["question"])

        results.append({
            "question":  qa["question"],
            "reference": qa["reference"],
            "answer":    out["answer"],
            "contexts":  out["contexts"],
        })
        print(f"  [{i:02d}/50] {qa['question'][:60]}")

    if len(results) != len(QA_PAIRS):
        raise RuntimeError(
            f"Expected {len(QA_PAIRS)} RAG results, got {len(results)}"
        )
    return results


# ── 4. Tạo RAGAS EvaluationDataset ────────────────────────────────────────
def build_ragas_dataset(rag_results: list) -> EvaluationDataset:
    """
    Chuyển đổi kết quả RAG thành RAGAS EvaluationDataset.

    Mỗi SingleTurnSample cần 4 trường:
      user_input         → câu hỏi
      response           → câu trả lời đã tạo
      retrieved_contexts → list[str] các đoạn đã retrieve
      reference          → đáp án chuẩn (ground truth)
    """
    samples = [
        SingleTurnSample(
            user_input=r["question"],
            response=r["answer"],
            retrieved_contexts=r["contexts"],
            reference=r["reference"],
        )
        for r in rag_results
    ]

    return EvaluationDataset(samples=samples)


# ── 5. Chạy RAGAS Evaluation ──────────────────────────────────────────────
def run_ragas_eval(rag_results: list, version: str) -> dict:
    """
    Đánh giá kết quả RAG với 4 RAGAS metrics.
    Trả về: dict {metric_name: mean_score}

    Lưu ý: evaluate() thực hiện rất nhiều lần gọi LLM → mất 5-10 phút / version.
    """
    print(f"\nEvaluating RAGAS for prompt {version} ... please wait")

    dataset = build_ragas_dataset(rag_results)

    # LLM và Embeddings riêng để RAGAS dùng làm evaluator
    llm_eval = get_llm(temperature=0)
    emb_eval = get_embeddings()

    metrics = [faithfulness, answer_relevancy, context_recall, context_precision]
    result = evaluate(
        dataset,
        metrics=metrics,
        llm=llm_eval,
        embeddings=emb_eval,
    )

    # Tính mean score cho mỗi metric
    # result["faithfulness"] trả về list of floats → dùng np.mean()
    scores = {}
    for key in ["faithfulness", "answer_relevancy", "context_recall", "context_precision"]:
        raw = result[key]
        if hasattr(raw, "tolist"):
            raw = raw.tolist()
        if not isinstance(raw, (list, tuple)):
            raw = [raw]

        values = []
        for value in raw:
            if value is None:
                continue
            numeric = float(value)
            if np.isfinite(numeric):
                values.append(numeric)
        if not values:
            raise ValueError(f"RAGAS metric '{key}' returned no finite scores")
        scores[key] = float(np.mean(values))

    # In kết quả
    print(f"\nRAGAS results - Prompt {version.upper()}:")
    for k, v in scores.items():
        marker = " [TARGET]" if k == "faithfulness" and v >= 0.8 else ""
        print(f"  {k:30s}: {v:.4f}{marker}")

    return scores


# ── 6. Main ────────────────────────────────────────────────────────────────
def main():
    """Evaluate both prompt versions and persist the final RAGAS report."""
    print("=" * 60)
    print("  Step 3: RAGAS Evaluation")
    print("=" * 60)

    if not config.validate():
        sys.exit(1)

    vectorstore = setup_vectorstore()

    # Thu thập kết quả RAG cho cả V1 và V2
    v1_results = collect_rag_outputs(vectorstore, "v1")
    v2_results = collect_rag_outputs(vectorstore, "v2")

    # Chạy RAGAS evaluation
    v1_scores = run_ragas_eval(v1_results, "v1")
    v2_scores = run_ragas_eval(v2_results, "v2")

    # In bảng so sánh
    print("\n" + "=" * 65)
    print(f"  {'Metric':30s}  {'V1':>8}  {'V2':>8}  Winner")
    print("=" * 65)
    for metric in ["faithfulness", "answer_relevancy", "context_recall", "context_precision"]:
        s1, s2  = v1_scores[metric], v2_scores[metric]
        winner  = "V1" if s1 > s2 else "V2" if s2 > s1 else "TIE"
        print(f"  {metric:30s}  {s1:>8.4f}  {s2:>8.4f}  {winner}")

    # Kiểm tra mục tiêu
    best_faith = max(v1_scores["faithfulness"], v2_scores["faithfulness"])
    if best_faith >= 0.8:
        print(f"\nTarget met: faithfulness = {best_faith:.4f} >= 0.8")
    else:
        print(f"\nTarget not met ({best_faith:.4f} < 0.8).")
        print("   Review chunking, retriever k and grounding prompts.")

    report = {
        "prompt_v1_scores": v1_scores,
        "prompt_v2_scores": v2_scores,
        "target_met": best_faith >= 0.8,
    }
    report_path = Path(__file__).parent.parent / "data" / "ragas_report.json"
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Report saved to {report_path}")


if __name__ == "__main__":
    main()
