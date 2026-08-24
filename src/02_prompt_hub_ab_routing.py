"""
Bước 2 — Prompt Hub & A/B Routing
===================================
NHIỆM VỤ:
  1. Viết 2 system prompt khác nhau (V1: ngắn gọn, V2: có cấu trúc)
  2. Push cả 2 lên LangSmith Prompt Hub qua client.push_prompt()
  3. Pull lại từ Hub qua client.pull_prompt()
  4. Implement A/B routing tất định: hash(request_id) % 2 → V1 hoặc V2
  5. Chạy 50 câu hỏi qua router → ≥ 50 LangSmith traces nữa

DELIVERABLE: 2 prompt version hiển thị trong Prompt Hub trên https://smith.langchain.com
"""
import sys
import hashlib
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def _configure_ascii_streams() -> None:
    """Prevent Windows CP1252 consoles from failing on Unicode output."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="ascii", errors="ignore")


_configure_ascii_streams()

import config  # ⚠️ phải import trước LangChain

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langsmith import Client, traceable

from utils.llm_factory import get_llm, get_embeddings
from utils.data_loader import load_knowledge_base, split_text, build_vectorstore
from qa_pairs import SAMPLE_QUESTIONS


def _ascii_text(value) -> str:
    """Convert console/log text to ASCII-safe output for Windows terminals."""
    text = str(value).replace("Đ", "D").replace("đ", "d")
    text = unicodedata.normalize("NFKD", text)
    return (
        "".join(char for char in text if not unicodedata.combining(char))
        .encode("ascii", errors="ignore")
        .decode("ascii")
    )


# ── 1. Tên Prompt trên Hub ─────────────────────────────────────────────────
PROMPT_V1_NAME = "tran-trong-nghia-rag-prompt-v1"   # ví dụ: "nguyen-rag-v1"
PROMPT_V2_NAME = "tran-trong-nghia-rag-prompt-v2"   # ví dụ: "nguyen-rag-v2"
PROMPT_SOURCES = {}


# ── 2. Định nghĩa 2 Prompt Templates ──────────────────────────────────────
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


# ── 3. Push Prompts lên Prompt Hub ─────────────────────────────────────────
def _is_unchanged_prompt_conflict(error: Exception) -> bool:
    """Return True when LangSmith reports an idempotent unchanged prompt push."""
    message = str(error).lower()
    response = getattr(error, "response", None)
    status_code = getattr(response, "status_code", None)
    return (
        "nothing to commit: prompt has not changed since latest commit" in message
        or (status_code == 409 and "nothing to commit" in message)
    )


def push_prompts_to_hub(client: Client):
    """
    Upload cả 2 prompt templates lên LangSmith Prompt Hub.
    Gợi ý: client.push_prompt(name, object=template, description="...")
    """
    errors = []

    try:
        url = client.push_prompt(
            PROMPT_V1_NAME,
            object=PROMPT_V1,
            description="V1: friendly and concise grounded answers",
        )
        print(f"[OK] Pushed V1 -> {_ascii_text(url)}")
    except Exception as e:
        if _is_unchanged_prompt_conflict(e):
            print(f"[OK] V1 already up to date on Hub: {PROMPT_V1_NAME}")
        else:
            errors.append(f"V1: {e}")
            print(f"[ERROR] V1 error: {_ascii_text(e)}")

    try:
        url = client.push_prompt(
            PROMPT_V2_NAME,
            object=PROMPT_V2,
            description="V2: structured expert grounded answers",
        )
        print(f"[OK] Pushed V2 -> {_ascii_text(url)}")
    except Exception as e:
        if _is_unchanged_prompt_conflict(e):
            print(f"[OK] V2 already up to date on Hub: {PROMPT_V2_NAME}")
        else:
            errors.append(f"V2: {e}")
            print(f"[ERROR] V2 error: {_ascii_text(e)}")

    if errors:
        raise RuntimeError("Could not push all prompts to Hub: " + "; ".join(errors))


# ── 4. Pull Prompts từ Prompt Hub ──────────────────────────────────────────
def pull_prompts_from_hub(client: Client) -> dict:
    """
    Tải 2 prompt từ LangSmith Prompt Hub.
    Fallback về template local nếu Hub không khả dụng.

    Gợi ý: client.pull_prompt(name) → ChatPromptTemplate

    Trả về: {name: ChatPromptTemplate}
    """
    prompts = {}
    prompt_sources = {}

    try:
        prompts[PROMPT_V1_NAME] = client.pull_prompt(PROMPT_V1_NAME)
        prompt_sources[PROMPT_V1_NAME] = "hub"
        print(f"[OK] Pulled '{PROMPT_V1_NAME}' from Hub")
    except Exception as e:
        prompts[PROMPT_V1_NAME] = PROMPT_V1
        prompt_sources[PROMPT_V1_NAME] = "local"
        print(f"[INFO] Using local fallback for '{PROMPT_V1_NAME}': {_ascii_text(e)}")

    try:
        prompts[PROMPT_V2_NAME] = client.pull_prompt(PROMPT_V2_NAME)
        prompt_sources[PROMPT_V2_NAME] = "hub"
        print(f"[OK] Pulled '{PROMPT_V2_NAME}' from Hub")
    except Exception as e:
        prompts[PROMPT_V2_NAME] = PROMPT_V2
        prompt_sources[PROMPT_V2_NAME] = "local"
        print(f"[INFO] Using local fallback for '{PROMPT_V2_NAME}': {_ascii_text(e)}")

    global PROMPT_SOURCES
    PROMPT_SOURCES = prompt_sources
    return prompts


# ── 5. A/B Routing tất định ────────────────────────────────────────────────
def get_prompt_version(request_id: str) -> str:
    """
    Xác định prompt version dựa trên MD5 hash của request_id.

    Quy tắc: hash chẵn → PROMPT_V1_NAME | hash lẻ → PROMPT_V2_NAME
    TÍNH CHẤT: cùng request_id LUÔN cho cùng kết quả (deterministic).

    Gợi ý:
        hash_int = int(hashlib.md5(request_id.encode()).hexdigest(), 16)
        return PROMPT_V1_NAME if hash_int % 2 == 0 else PROMPT_V2_NAME
    """
    hash_int = int(hashlib.md5(request_id.encode("utf-8")).hexdigest(), 16)
    return PROMPT_V1_NAME if hash_int % 2 == 0 else PROMPT_V2_NAME


# ── 6. Traced A/B Query ────────────────────────────────────────────────────
@traceable(name="ab-rag-query", tags=["ab-test", "step2"])
def ask_ab(retriever, llm, prompt, question: str, version: str) -> dict:
    """
    Chạy RAG chain với prompt version được chọn bởi router.

    Bước:
      a) Retrieve top-3 docs từ retriever
      b) Ghép page_content thành context string
      c) Chạy (prompt | llm | StrOutputParser()).invoke({"context": ..., "question": ...})
      d) Trả về {"question": ..., "answer": ..., "version": ...}
    """
    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    answer = (prompt | llm | StrOutputParser()).invoke({
        "context": context,
        "question": question,
    })

    return {
        "question": question,
        "answer": answer,
        "version": version,
    }


# ── 7. Setup Vectorstore (tái sử dụng logic Bước 1) ───────────────────────
def setup_vectorstore():
    """Build the shared FAISS vector store from the project knowledge base."""
    embeddings  = get_embeddings()
    text        = load_knowledge_base()
    chunks      = split_text(text, chunk_size=500, chunk_overlap=50)
    return build_vectorstore(chunks, embeddings)


# ── 8. Main ────────────────────────────────────────────────────────────────
def main():
    """Push/pull prompts and run deterministic A/B routing for 50 questions."""
    print("=" * 60)
    print("  Step 2: Prompt Hub & A/B Routing")
    print("=" * 60)

    if not config.validate():
        sys.exit(1)

    client = Client(api_key=config.LANGSMITH_API_KEY)

    push_prompts_to_hub(client)

    prompts = pull_prompts_from_hub(client)
    if set(PROMPT_SOURCES.values()) != {"hub"}:
        raise RuntimeError(
            "Lần chạy chính thức yêu cầu pull cả hai prompt từ Hub; "
            f"nguồn hiện tại: {PROMPT_SOURCES}"
        )

    # Tạo vectorstore, retriever và LLM
    vectorstore = setup_vectorstore()
    retriever   = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm         = get_llm()

    # Chạy A/B routing cho tất cả câu hỏi
    v1_count, v2_count = 0, 0
    for i, question in enumerate(SAMPLE_QUESTIONS):
        request_id  = f"req-{i:04d}"

        version_key = get_prompt_version(request_id)
        version_tag = "v1" if version_key == PROMPT_V1_NAME else "v2"
        prompt      = prompts[version_key]

        result = ask_ab(retriever, llm, prompt, question, version_tag)

        if version_tag == "v1":
            v1_count += 1
        else:
            v2_count += 1
        print(f"[{i+1:02d}] [prompt-{version_tag}] {question[:55]}...")
        print(f"       A: {_ascii_text(result['answer'])[:100]}\n")

    print(f"\n[STATS] Routing: V1={v1_count} queries | V2={v2_count} queries | Total={len(SAMPLE_QUESTIONS)}")
    print("[OK] Step 2 complete. Check Prompt Hub and LangSmith traces.")


if __name__ == "__main__":
    main()
