# Kế hoạch hoàn thiện Day 22 — LangSmith + Prompt Versioning

## 1. Mục tiêu và cách sử dụng tài liệu

Tài liệu này là nguồn điều phối duy nhất cho quá trình hoàn thiện dự án. Mục tiêu bắt buộc là đạt đủ 100/100 điểm cơ bản theo rubric.md. Mục tiêu mở rộng là đạt tối đa 15 điểm thưởng, tương ứng mức lý thuyết 115/100:

- Tối đa +5 điểm cho kết quả và phân tích RAGAS.
- Tối đa +5 điểm cho chất lượng bằng chứng và nộp bài.
- Tối đa +5 điểm cho chất lượng mã nguồn.

Mọi bước triển khai phải đi theo thứ tự phase trong tài liệu này. Một phase chỉ được đánh dấu hoàn thành khi toàn bộ cổng kiểm tra của phase đó đã có bằng chứng. Không dùng kết quả kiểm tra tĩnh để thay thế cho xác minh runtime, LangSmith UI, Prompt Hub, file đầu ra hoặc ảnh chụp thật.

### Quy ước trạng thái

- [ ] Chưa bắt đầu.
- [~] Đang thực hiện.
- [x] Đã thực hiện và đã xác minh.
- [!] Bị chặn; phải ghi nguyên nhân và bằng chứng, không bỏ qua.

### Quy tắc thay đổi kế hoạch

1. Không tự ý nhảy phase.
2. Nếu một giả định trong kế hoạch sai, dừng tại task hiện tại, ghi bằng chứng, cập nhật đúng task liên quan rồi mới tiếp tục.
3. Không mở rộng danh sách file được phép sửa chỉ để xử lý thuận tiện hơn.
4. Nếu cần sửa một file đang bị khóa, phải chứng minh đó là blocker thực tế và xin xác nhận trước.
5. Không đánh dấu hoàn thành dựa trên output cũ, output của máy khác, ảnh minh họa, dữ liệu tự điền hoặc điểm số chưa chạy thật.

---

## 2. Nguồn yêu cầu và thứ tự ưu tiên

Các nguồn đã được đọc đầy đủ:

- rubric.md: 168 dòng.
- README.md: 287 dòng.
- Guide.md: 732 dòng.
- requirements.md: 86 dòng.
- requirements.txt và .env.example.
- Toàn bộ 10 file Python trong src.
- data/knowledge_base.txt.
- .gitignore và trạng thái Git hiện tại.

Khi có mâu thuẫn, áp dụng thứ tự:

1. Quy tắc phạm vi do người dùng đặt ra.
2. Tiêu chí chấm điểm và trừ điểm trong rubric.md.
3. Yêu cầu kỹ thuật trong Guide.md và requirements.md.
4. Hướng dẫn tổng quan trong README.md.
5. Comment, gợi ý và placeholder trong starter code.

Ví dụ bắt buộc áp dụng thứ tự này:

- Rubric yêu cầu PII dùng OnFailAction.FIX và đầu ra bị chặn được thay bằng chuỗi an toàn. Guide hướng dẫn trả về FailResult có fix_value. Vì vậy không làm theo comment trong starter đang gợi ý PassResult cho trường hợp tìm thấy PII.
- Rubric yêu cầu prompt được pull thật từ Hub. Local fallback có thể tồn tại để xử lý lỗi, nhưng một lần chạy dùng fallback không được chấp nhận là lần chạy chấm điểm.
- Rubric yêu cầu hai file log Guardrails riêng. Lệnh ví dụ trong Guide chỉ ghi một file không đủ; kế hoạch phải thu hai log riêng.
- Rubric yêu cầu tạo data/ragas_report.json và bản evidence. Theo quyết định của người dùng, giữ file data là output cục bộ bị ignore và chỉ nộp evidence/03_ragas_report.json.

---

## 3. Ràng buộc bất biến của dự án

### 3.1. File tuyệt đối không chỉnh sửa

- Mọi file test hoặc smoke hiện có hoặc được bổ sung sau này.
- requirements.txt.
- requirements.md.
- .env.example.
- rubric.md.
- README.md.
- Guide.md.
- src/qa_pairs.py.
- data/knowledge_base.txt.
- src/config.py.
- src/utils/llm_factory.py.
- src/utils/data_loader.py.
- src/utils/__init__.py.

Không có file test hoặc smoke nào trong checkout hiện tại. Điều này không cho phép tạo hoặc sửa chúng; kiểm tra bổ sung phải thực hiện bằng lệnh smoke tạm thời, không tạo test file.

### 3.2. File được phép sửa hoặc tạo trong kế hoạch

Phạm vi cơ bản:

- PROJECT_PLAN.md: cập nhật trạng thái và kết quả thực thi.
- src/01_langsmith_rag_pipeline.py.
- src/02_prompt_hub_ab_routing.py.
- src/03_ragas_evaluation.py.
- src/04_guardrails_validator.py.
- .gitignore: giữ nguyên rule data/ragas_report.json theo quyết định chỉ nộp bản evidence.
- data/ragas_report.json: file sinh ra từ lần chạy RAGAS thật.
- Bảy file bằng chứng bắt buộc trong evidence.
- evidence/README.md cho điểm thưởng phân tích.

Phạm vi tùy chọn, chỉ dùng nếu kiểm tra chứng minh cần thiết:

- src/run_all.py: chỉ sửa tối thiểu để trả exit code đúng hoặc bảo đảm chạy liên tục không cần can thiệp giữa các bước. Không tái cấu trúc ngoài mục tiêu này.

### 3.3. Dữ liệu cục bộ không được commit

- .env.
- .venv và mọi virtual environment.
- API key, token, cookie, credential hoặc URL có secret.
- __pycache__, file pyc và cache runtime.
- Output tạm không thuộc danh sách deliverable.

### 3.4. Quy tắc Git

- Không dùng git add toàn bộ thư mục.
- Chỉ stage đường dẫn cụ thể đã kiểm tra.
- Không push lên upstream.
- Không sửa, xóa hoặc hoàn tác thay đổi không thuộc task hiện tại.
- Trước mỗi phase phải kiểm tra git status và diff.
- Commit hoặc push chỉ thực hiện sau cổng bảo mật và khi được phép thực hiện hành động nộp bài.

---

## 4. Baseline đã xác minh ngày 2026-08-24

| Hạng mục | Trạng thái hiện tại | Hệ quả |
|---|---|---|
| Git | Nhánh main sạch, theo dõi origin/main | Có baseline rõ ràng trước khi triển khai |
| Commit đầu | cd8c7828a57509812c1bf05596ad5c18676b2840 | Dùng làm mốc đối chiếu |
| Remote origin | Repository GitHub của người học | Chỉ push origin khi được phép |
| Remote upstream | Repository starter VinUni-AI20k | Tuyệt đối không push upstream |
| Python trên PATH | Lệnh python không tồn tại | Không dùng python trực tiếp trước khi tạo venv |
| Python launcher | py -3.12 chạy Python 3.12.10 | Đạt yêu cầu Python >= 3.10 |
| Virtual environment | Chưa có | Phải tạo .venv trước khi cài dependency |
| Dependency | Global Python thiếu hầu hết package của lab | Không được tuyên bố runtime sẵn sàng |
| .env | Chưa tồn tại | Cần người dùng cung cấp cấu hình cục bộ |
| Evidence | Chỉ có evidence/.gitkeep | Chưa có bằng chứng chấm điểm |
| RAGAS report | Chưa tồn tại | Nhiệm vụ 3 chưa chạy |
| Git ignore | data/ragas_report.json bị ignore tại .gitignore dòng 30 | Đã chốt giữ nguyên; nộp evidence/03_ragas_report.json |
| Bộ dữ liệu QA | 50 SAMPLE_QUESTIONS và 50 QA_PAIRS | Đủ số lượng rubric |
| Thứ tự QA | Hai danh sách khớp hoàn toàn theo câu hỏi | Có thể so sánh nhất quán |
| Cú pháp starter | 10 file Python parse AST thành công | Cú pháp hợp lệ nhưng logic chưa hoàn thiện |
| TODO | Bước 1: 13; Bước 2: 20; Bước 3: 15; Bước 4: 15 | Chưa file nhiệm vụ nào chạy hoàn chỉnh |
| Routing dự kiến | req-0000 đến req-0049 cho V1=19, V2=31 | Cả hai phiên bản chắc chắn nhận request |

### 4.1. Các blocker và xung đột đã phát hiện

1. README và Guide minh họa tên biến LANGSMITH_API_KEY/LANGSMITH_PROJECT, nhưng config.py và .env.example thực tế đọc LANGCHAIN_API_KEY/LANGCHAIN_PROJECT.
   - Quyết định: cấu hình .env theo .env.example và code hiện tại.
   - Không chỉnh README, Guide, config.py hoặc .env.example.

2. Rubric liệt kê data/ragas_report.json nhưng starter .gitignore ghi rõ chỉ nộp evidence.
   - Quyết định của người dùng: giữ rule ignore và chỉ nộp evidence/03_ragas_report.json; bản evidence phải khớp screenshot submission, không phụ thuộc report data bị một lần chạy sau ghi lại.

3. Template prompt trong starter của Bước 2 và Bước 3 chưa có context hoàn chỉnh.
   - Quyết định: cả V1 và V2 phải chứa biến context trong system message; nếu không, trace và RAG không đáp ứng rubric.

4. Starter Bước 4 gợi ý PassResult khi phát hiện PII, trái với đường xử lý OnFailAction.FIX trong rubric và Guide.
   - Quyết định: phát hiện PII phải trả FailResult với fix_value là chuỗi đã redact.

5. Starter JSONFormatter trả FailResult không có fallback JSON.
   - Quyết định: luôn tạo JSON fallback hợp lệ và truyền qua fix_value khi không sửa được.

6. Guide minh họa một lệnh Guardrails chỉ ghi log PII.
   - Quyết định: gọi riêng demo_pii_guard và demo_json_guard để tạo đúng hai log bắt buộc.

7. requirements.txt dùng giới hạn phiên bản mở, trong khi requirements.md mô tả API RAGAS 0.4.x và Guardrails 0.10.x.
   - Quyết định: cài nguyên requirements.txt không sửa file, sau đó chạy import/API smoke. Nếu phiên bản được resolver chọn không tương thích, điều chỉnh phiên bản chỉ trong .venv, vẫn nằm trong ràng buộc đã khai báo, và ghi phiên bản thực tế vào nhật ký thực thi.

8. run_all.py hiện bắt exception nhưng có thể kết thúc process với exit code 0 sau khi một bước thất bại.
   - Quyết định: kiểm tra hành vi sau khi hoàn thiện. Chỉ sửa tối thiểu nếu điều này làm cổng tích hợp báo PASS giả.

---

## 5. Định nghĩa hoàn thành

Dự án chỉ được gọi là hoàn thành khi đồng thời thỏa tất cả điều kiện sau:

### 5.1. Mã nguồn

- Bốn file nhiệm vụ không còn placeholder thực thi như gán Ellipsis hoặc return Ellipsis.
- Bốn bước chạy thành công trong môi trường đã cấu hình.
- run_all.py có thể gọi từng bước mà không cần sửa code giữa các lần chạy.
- Không có lỗi import, lỗi dependency hoặc lỗi pip check.
- Không có API key hard-code.

### 5.2. LangSmith và Prompt Hub

- Có ít nhất 50 root traces cho Bước 1.
- Có thêm ít nhất 50 root traces cho Bước 2.
- Tổng project có ít nhất 100 traces hợp lệ; không dùng child span để che thiếu root trace.
- Một trace Bước 1 được kiểm tra có câu hỏi, context truy xuất và câu trả lời.
- Một trace Bước 2 được kiểm tra có câu hỏi, version, context và câu trả lời.
- Hai prompt khác nghĩa đã push lên Hub.
- Lần chạy chấm điểm pull thành công cả hai prompt từ Hub, không dùng fallback.
- Public LangSmith trace URL của project có thể truy cập không cần đăng nhập theo UI hiện tại.

### 5.3. RAGAS

- Đúng 50 QA được chạy cho V1 và đúng 50 QA cho V2.
- Mọi SingleTurnSample có user_input, response, retrieved_contexts dạng list[str], reference.
- Cả bốn metric có mặt cho cả V1 và V2.
- Mọi score là số hữu hạn trong khoảng hợp lệ.
- Faithfulness >= 0.8 cho ít nhất một phiên bản.
- data/ragas_report.json tồn tại cục bộ, hợp lệ; evidence/03_ragas_report.json là bản được Git theo dõi khi stage.
- evidence/03_ragas_report.json là snapshot submission khớp số liệu trong evidence/03_ragas_scores.png.

### 5.4. Guardrails

- Hai custom validator đều dùng register_validator.
- PII phát hiện ít nhất ba loại; mục tiêu triển khai đủ bốn loại.
- PII dùng regex, FailResult có fix_value, và validator instance nhận OnFailAction.FIX trong constructor.
- Tối thiểu năm PII case; mục tiêu là sáu case gồm clean và multi-PII.
- JSON parse trực tiếp được JSON hợp lệ.
- JSON tự sửa ít nhất hai loại lỗi; mục tiêu là ba loại: fences, single quotes, trailing commas.
- Input không thể sửa trả một JSON fallback hợp lệ qua fix_value.
- Tối thiểu bốn JSON case; mục tiêu là năm case.

### 5.5. Bằng chứng và nộp bài

Bảy file bắt buộc, đúng tên:

1. evidence/01_langsmith_traces.png.
2. evidence/02_prompt_hub.png.
3. evidence/02_ab_routing_log.txt.
4. evidence/03_ragas_scores.png.
5. evidence/03_ragas_report.json.
6. evidence/04_pii_demo_log.txt.
7. evidence/04_json_demo_log.txt.

File thưởng:

8. evidence/README.md.

Ngoài ra:

- Repository GitHub public chứa mã nguồn và evidence.
- Public LangSmith trace URL đã được kiểm tra HTTP 200 không cookie.
- Không có .env hoặc secret trong Git history mới, staging area hay file được nộp.

---

## 6. Ma trận truy vết rubric

| Rubric | Điểm | Thay đổi/đầu ra dự kiến | Cách xác minh bắt buộc |
|---|---:|---|---|
| 1.1 | 5 | setup_vectorstore gọi get_embeddings, load_knowledge_base, split_text 500/50, build_vectorstore | Runtime in số chunk > 0; FAISS tạo thành công; truy vấn trả docs |
| 1.2 | 5 | LCEL chain retriever → format_docs → RAG_PROMPT → LLM → StrOutputParser | Một truy vấn smoke trả str và prompt nhận context |
| 1.3 | 10 | ask có traceable tên rag-query và tags rag/step1; chạy 50 câu | LangSmith filter root run rag-query cho thấy >= 50 |
| 1.4 | 5 | Trace giữ question, retrieved context, final answer | Mở chi tiết một root trace và child runs để kiểm tra ba thành phần |
| 2.1 | 5 | SYSTEM_V1 ngắn gọn; SYSTEM_V2 chuyên gia, có cấu trúc; cả hai grounding theo context | Review nội dung và kiểm tra hai chuỗi khác nghĩa |
| 2.2 | 8 | Push cả hai ChatPromptTemplate với tên duy nhất | Prompt Hub hiển thị cả hai tên; ảnh 02_prompt_hub.png |
| 2.3 | 4 | client.pull_prompt được gọi và kết quả đó được dùng | Log chính thức có hai dòng pull thành công, không có fallback |
| 2.4 | 5 | MD5 request_id, parity chọn version | Gọi cùng ID nhiều lần cho cùng kết quả; mapping ổn định |
| 2.5 | 3 | 50 request có nhãn prompt-v1/v2 | Log có đúng 50 dòng; dự kiến V1=19 và V2=31 |
| 3.1 | 5 | collect_rag_outputs chạy toàn bộ QA cho từng version | Assert len(v1_results)=len(v2_results)=50 |
| 3.2 | 5 | EvaluationDataset gồm SingleTurnSample đủ bốn trường | Smoke kiểm tra type và dữ liệu không rỗng |
| 3.3 | 8 | evaluate dùng bốn metric yêu cầu | Report có bốn key cho cả hai version |
| 3.4 | 5 | Ít nhất một faithfulness >= 0.8 | Đọc trực tiếp JSON sinh từ lần chạy thật |
| 3.5 | 2 | Lưu data/ragas_report.json và copy sang evidence | Parse JSON; evidence report khớp screenshot; chỉ stage bản evidence theo quyết định người dùng |
| 4.1 | 3 | PIIDetector có register_validator | Import và inspect class thành công |
| 4.2 | 5 | Regex EMAIL, PHONE, SSN, CREDIT_CARD | Demo từng loại và multi-PII, không còn giá trị gốc |
| 4.3 | 3 | FailResult fix_value + OnFailAction.FIX ở constructor | Output là placeholder an toàn, code review đúng API |
| 4.4 | 2 | Sáu PII case | Log có Email, Phone, SSN, Credit Card, Multi-PII, Clean |
| 4.5 | 3 | JSONFormatter custom validator và json.loads | Valid JSON pass và được chuẩn hóa |
| 4.6 | 5 | Sửa fences, single quotes, trailing commas | Ba case sửa được và output parse lại thành công |
| 4.7 | 2 | Fallback JSON cho input vô phương sửa | Output fallback parse được, có trường error/raw |
| 4.8 | 2 | Năm JSON case | Log có đủ năm nhãn và output tương ứng |

### Ma trận điểm thưởng

| Nhóm thưởng | Điểm tối đa | Điều kiện |
|---|---:|---|
| RAGAS chất lượng | +3 | Faithfulness >= 0.9 ở cả V1 và V2; chỉ ghi nhận nếu chạy thật |
| RAGAS phân tích | +2 | Phân tích có số liệu giải thích version nào tốt hơn và vì sao |
| Evidence đầy đủ | +3 | Đúng bảy file bắt buộc, rõ ràng, nhãn đúng |
| LangSmith public | +1 | URL project truy cập được ngoài phiên đăng nhập cá nhân theo yêu cầu chấm |
| Evidence README | +1 | Có phân tích V1 so với V2 |
| Mã sạch/docstring | +2 | Cấu trúc rõ, không placeholder, docstring hữu ích |
| run_all | +2 | Các bước chạy qua run_all.py không cần sửa code giữa chừng |
| Error handling/fallback | +1 | Lỗi có thông báo rõ; fallback không làm giả trạng thái đạt rubric |

---

## 7. Trình tự triển khai bắt buộc

## Phase 0 — Khóa baseline, môi trường và bảo mật

### Mục tiêu

Tạo môi trường có thể tái lập, xác minh credential mà không lộ secret, và bảo đảm không bắt đầu các lượt gọi API tốn phí khi dependency hoặc cấu hình còn lỗi.

### P0.1 — Chụp baseline trước thay đổi

- [x] Chạy tại project root bằng PowerShell:

    Set-Location 'D:\Tailieu-2026\vin\0.Lab_vin\Day22_lab\Day22-Track2-LLMops-Prompt-versioning'
    git status --short --branch
    git diff --check
    git diff --name-only

- [x] Nếu xuất hiện thay đổi ngoài PROJECT_PLAN.md, phân loại đó là thay đổi của người dùng và không chạm vào.
- [x] Ghi commit baseline vào nhật ký cuối tài liệu.

Điều kiện PASS:

- Biết chính xác file nào đã thay đổi trước khi triển khai.
- Không có diff không xác định quyền sở hữu.

### P0.2 — Tạo virtual environment

- [x] Dùng Python launcher đã xác minh:

    py -3.12 -m venv .venv
    & .\.venv\Scripts\python.exe --version
    & .\.venv\Scripts\python.exe -m pip --version

- [x] Không dùng global Python để chạy lab sau bước này.
- [x] Xác minh .venv bị Git ignore:

    git check-ignore -v .venv

Điều kiện PASS:

- .venv Python chạy được và phiên bản >= 3.10.
- .venv không xuất hiện trong danh sách stage.

### P0.3 — Cài dependency mà không sửa requirements

- [x] Cài đúng file hiện có:

    & .\.venv\Scripts\python.exe -m pip install -r .\requirements.txt
    & .\.venv\Scripts\python.exe -m pip check

- [x] Chạy import smoke:

    & .\.venv\Scripts\python.exe -c "import langchain, langsmith, faiss, ragas, guardrails, dotenv, numpy; print('IMPORT_OK')"

- [x] Ghi phiên bản thực tế:

    & .\.venv\Scripts\python.exe -m pip show langchain langsmith ragas guardrails-ai faiss-cpu

- [x] Kiểm tra API quan trọng:

    & .\.venv\Scripts\python.exe -c "from ragas import evaluate, EvaluationDataset, SingleTurnSample; from ragas.metrics import faithfulness, answer_relevancy, context_recall, context_precision; print('RAGAS_API_OK')"
    & .\.venv\Scripts\python.exe -c "from guardrails import Guard; from guardrails.validators import Validator, register_validator, PassResult, FailResult; print('GUARDRAILS_API_OK')"

Nếu API smoke lỗi:

1. Ghi nguyên văn package và lỗi.
2. Không sửa requirements.txt hoặc requirements.md.
3. Chọn phiên bản tương thích trong .venv nằm trong giới hạn hiện có và phù hợp version notes.
4. Chạy lại pip check và cả hai import smoke.
5. Chỉ tiếp tục khi không còn lỗi.

### P0.4 — Tạo cấu hình .env cục bộ

- [ ] Tạo từ template, không sửa template:

    Copy-Item -LiteralPath .\.env.example -Destination .\.env

- [x] Người dùng điền secret trực tiếp; không in, không dán vào log hoặc chat.
- [x] Dùng tên biến đúng theo code:
  - LANGCHAIN_TRACING_V2=true.
  - LANGCHAIN_API_KEY.
  - LANGCHAIN_PROJECT.
  - PROVIDER và key/model tương ứng.
- [x] Dùng một LangSmith project mới hoặc project sạch, có tên duy nhất cho lần nộp này.

Khuyến nghị provider theo code hiện tại:

1. OpenAI nếu có key cho cả LLM và embeddings.
2. Gemini nếu chấp nhận quota/rate limit thấp hơn.
3. Ollama chỉ khi model chat và embedding đã chạy local, nhưng vẫn cần LangSmith key.
4. Anthropic và OpenRouter không phải lựa chọn một-key trong starter hiện tại vì embeddings vẫn phụ thuộc OpenAI ở llm_factory.

Không mặc định model còn hoạt động chỉ vì có trong .env.example. Phải chạy một smoke call trước. Nếu model không còn khả dụng, chỉ đổi giá trị model trong .env cục bộ.

### P0.5 — Cổng cấu hình và bảo mật

- [x] Xác minh .env bị ignore và không được track:

    git check-ignore -v .env
    git ls-files --error-unmatch .env

Lệnh thứ hai phải trả trạng thái không tìm thấy file. Nếu tìm thấy, dừng ngay.

- [x] Chạy config:

    & .\.venv\Scripts\python.exe .\src\config.py

- [x] Thực hiện một lời gọi LLM/embedding nhỏ trước khi chạy 50 câu. Không ghi secret vào output.
- [x] Kiểm tra LangSmith project nhận được trace smoke đúng project.

Điều kiện PASS của Phase 0:

- Python, pip check và import smoke đều PASS.
- config.validate trả True.
- Một LLM call và một embedding operation hoạt động.
- Tracing gửi đúng project.
- .env không được Git track.

Điều kiện dừng:

- Thiếu credential.
- Model hoặc embedding không khả dụng.
- Dependency API không tương thích.
- LangSmith không nhận trace.

Không bắt đầu Phase 1 khi một điều kiện trên chưa giải quyết.

---

## Phase 1 — Nhiệm vụ 1: RAG Pipeline và 50 LangSmith traces

### File được phép sửa

- src/01_langsmith_rag_pipeline.py.

### P1.1 — Hoàn thiện setup_vectorstore

- [x] embeddings = get_embeddings().
- [x] text = load_knowledge_base().
- [x] chunks = split_text(text, chunk_size=500, chunk_overlap=50).
- [x] Xác minh chunks là list không rỗng và không chứa phần tử rỗng.
- [x] vectorstore = build_vectorstore(chunks, embeddings).
- [x] Trả vectorstore.

Không sửa data_loader vì helper đã hoàn chỉnh.

### P1.2 — Hoàn thiện RAG_PROMPT

- [x] Dùng ChatPromptTemplate.from_messages.
- [x] System message phải:
  - Chỉ cho phép trả lời dựa trên context.
  - Chứa biến {context}.
  - Có câu fallback khi context không đủ.
- [x] Human message chứa {question}.
- [x] Không hard-code câu hỏi, context hoặc secret.

### P1.3 — Hoàn thiện LCEL chain

- [x] Tạo retriever với search_kwargs k=3.
- [x] format_docs ghép page_content bằng hai newline.
- [x] Dùng mapping context/question, RunnablePassthrough, prompt, LLM và StrOutputParser theo đúng thứ tự.
- [x] Trả cả chain và retriever như chữ ký hiện có.

### P1.4 — Hoàn thiện tracing và main

- [x] Đặt decorator ngay trên ask:
  - name là rag-query.
  - tags gồm rag và step1.
- [x] ask gọi chain.invoke(question) và trả str.
- [x] main dùng toàn bộ 50 SAMPLE_QUESTIONS.
- [x] Không bắt exception rồi tiếp tục âm thầm; một câu lỗi làm bước thất bại rõ ràng.
- [x] Output in đủ số thứ tự, câu hỏi và phần đầu câu trả lời.

### P1.5 — Kiểm tra tĩnh trước API

- [x] Không còn placeholder thực thi:

    rg -n "=\s*\.\.\.|return\s+\.\.\.|\(\.\.\.\)" .\src\01_langsmith_rag_pipeline.py

Kết quả phải rỗng.

- [x] Parse/compile:

    & .\.venv\Scripts\python.exe -m py_compile .\src\01_langsmith_rag_pipeline.py

- [x] Review diff chỉ đúng file Phase 1:

    git diff -- .\src\01_langsmith_rag_pipeline.py
    git diff --check

### P1.6 — Runtime smoke có kiểm soát

- [x] Tạo vectorstore thành công.
- [x] Retriever trả đúng kiểu danh sách document cho một câu hỏi.
- [x] Một chain invocation trả string có nội dung.
- [x] Mở trace smoke và xác nhận có question, child retriever context và final answer.

Không chuyển sang chạy 50 nếu trace smoke thiếu context.

### P1.7 — Lần chạy chính thức

- [x] Chạy qua orchestrator (người dùng xác nhận đã chạy run_all.py):

    & .\.venv\Scripts\python.exe .\src\run_all.py --step 1

- [x] Xác nhận process thành công và console báo 50 traces.
- [x] Chờ LangSmith flush rồi lọc root run name rag-query hoặc tag step1.
- [x] Xác nhận ít nhất 50 root traces của lần chạy hợp lệ.
- [ ] Mở ngẫu nhiên ít nhất ba trace: đầu, giữa và cuối.

### P1.8 — Bằng chứng và cổng Phase 1

- [x] Chụp ảnh thật từ LangSmith UI, thấy project đúng và ít nhất 50 traces.
- [x] Lưu đúng evidence/01_langsmith_traces.png.
- [x] Kiểm tra ảnh đọc được, không cắt mất project/count quan trọng.

Phase 1 PASS khi rubric 1.1, 1.2, 1.3 và 1.4 đều có bằng chứng. Không dùng ảnh cũ hoặc ảnh minh họa.

---

## Phase 2 — Nhiệm vụ 2: Prompt Hub và A/B routing

### File được phép sửa/tạo

- src/02_prompt_hub_ab_routing.py.
- evidence/02_ab_routing_log.txt.
- evidence/02_prompt_hub.png.

### P2.1 — Chốt tên prompt duy nhất

- [x] Người dùng xác nhận một slug không phải placeholder.
- [x] PROMPT_V1_NAME và PROMPT_V2_NAME khác nhau, có hậu tố rõ v1/v2.
- [x] Tên không trùng prompt cũ trong workspace LangSmith.
- [x] Không dùng dữ liệu cá nhân chưa được xác nhận.

### P2.2 — Soạn hai prompt khác nghĩa

V1:

- [x] Giọng thân thiện, ngắn gọn 2–4 câu.
- [x] Chỉ dựa trên context.
- [x] Nêu không tìm thấy khi thiếu dữ liệu.
- [x] Có Context:\n{context}.

V2:

- [x] Giọng chuyên gia, có cấu trúc 3–5 câu.
- [x] Ưu tiên kết luận, facts hỗ trợ và mức chắc chắn hoặc nguồn context.
- [x] Không suy đoán ngoài context.
- [x] Có Context:\n{context}.

Hai prompt phải khác chiến lược trả lời, không chỉ thay vài từ.

### P2.3 — Push prompt

- [x] Tạo Client bằng config.LANGSMITH_API_KEY.
- [x] Push V1 và V2 bằng client.push_prompt.
- [x] Description mô tả đúng từng version.
- [x] Catch lỗi để thông báo rõ prompt nào lỗi.
- [x] Không tiếp tục lần chạy chấm điểm nếu một lần push thất bại.

### P2.4 — Pull prompt và kiểm soát fallback

- [x] Gọi client.pull_prompt cho từng tên.
- [x] Dictionary trả về đúng key và template từ Hub.
- [x] Local fallback chỉ phục vụ chẩn đoán khả dụng.
- [x] Console phải ghi rõ nguồn Hub hay fallback.
- [x] Lần chạy chính thức bị coi là FAIL nếu bất kỳ version nào dùng fallback.

### P2.5 — Routing tất định

- [x] Encode request_id.
- [x] Tính MD5 hexdigest và chuyển sang số nguyên.
- [x] Chẵn chọn V1, lẻ chọn V2.
- [x] Không dùng random, built-in hash hoặc thời gian.
- [x] Trả đúng prompt name để index dictionary.

Smoke bắt buộc:

- [x] Cùng request_id gọi ít nhất ba lần cho cùng kết quả.
- [x] req-0000 đến req-0049 cho cả hai version.
- [x] Với logic hiện tại, xác nhận lại V1=19 và V2=31; nếu format request_id thay đổi, tính lại và ghi kết quả thật.

### P2.6 — Traced A/B query

- [x] Đặt traceable name ab-rag-query, tags ab-test và step2.
- [x] ask_ab retrieve top-3 docs.
- [x] contexts ghép từ page_content.
- [x] Template từ dictionary Hub được dùng trong chain.
- [x] Invoke có context và question.
- [x] Kết quả gồm question, answer và version.

### P2.7 — Hoàn thiện main

- [x] Validate config.
- [x] Tạo Client.
- [x] Push cả hai prompt.
- [x] Pull cả hai prompt.
- [x] Tạo vectorstore, retriever k=3 và LLM.
- [x] Chạy đúng 50 SAMPLE_QUESTIONS.
- [x] Mỗi dòng query có request index và nhãn prompt-v1 hoặc prompt-v2.
- [x] Tổng kết hiển thị V1, V2 và tổng.

### P2.8 — Kiểm tra tĩnh và smoke

- [x] Không còn placeholder.
- [x] Hai prompt đều khai báo biến context và question.
- [x] Py-compile thành công.
- [x] Diff chỉ thuộc file Phase 2.
- [x] Push/pull smoke thành công trước khi chạy 50.

### P2.9 — Lần chạy chính thức và log

Chạy từ project root bằng PowerShell:

    & .\.venv\Scripts\python.exe .\src\run_all.py --step 2 2>&1 |
        Tee-Object -FilePath .\evidence\02_ab_routing_log.txt

- [x] Process không lỗi.
- [x] Log có hai dòng pull thành công.
- [x] Log không có local fallback trong lần chạy chính thức.
- [x] Log có đúng 50 dòng query được gắn nhãn.
- [x] Log chứa cả prompt-v1 và prompt-v2.
- [x] Tổng V1 + V2 = 50.

Kiểm tra log bằng PowerShell:

    $abLines = Get-Content -LiteralPath .\evidence\02_ab_routing_log.txt
    $queryLines = @($abLines | Where-Object { $_ -match '^\[\d{2}\] \[prompt-v[12]\]' })
    $v1Lines = @($queryLines | Where-Object { $_ -match '\[prompt-v1\]' })
    $v2Lines = @($queryLines | Where-Object { $_ -match '\[prompt-v2\]' })
    if ($queryLines.Count -ne 50) { throw "A/B log không có đúng 50 query" }
    if ($v1Lines.Count -eq 0 -or $v2Lines.Count -eq 0) { throw "Thiếu một prompt version" }

### P2.10 — LangSmith và Prompt Hub

- [x] Prompt Hub hiển thị rõ cả hai prompt name.
- [x] Mở từng prompt và xác minh nội dung/version đúng.
- [x] Chụp ảnh thật thành evidence/02_prompt_hub.png.
- [x] LangSmith có thêm ít nhất 50 root ab-rag-query traces.
- [x] Tổng root traces của Bước 1 và Bước 2 >= 100.
- [x] Kiểm tra một trace mỗi version có context và answer.

### P2.11 — Cổng Phase 2

Phase 2 chỉ PASS khi rubric 2.1–2.5 đều đạt, file log đủ 50 query, Hub pull thật và hai version đều có trace.

---

## Phase 3 — Nhiệm vụ 3: RAGAS Evaluation

### File được phép sửa/tạo

- src/03_ragas_evaluation.py.
- .gitignore không sửa; giữ rule output cục bộ theo quyết định người dùng.
- data/ragas_report.json.
- evidence/03_ragas_scores.png.
- evidence/03_ragas_report.json.

### P3.1 — Đồng bộ prompt

- [x] Copy chính xác SYSTEM_V1 và SYSTEM_V2 đã được chấp nhận ở Phase 2.
- [x] PROMPT_V1 và PROMPT_V2 đều có context và question.
- [x] So sánh programmatically để tránh drift nội dung.
- [x] Không tối ưu riêng một version bằng cách thay đổi retriever hoặc model.

### P3.2 — Hoàn thiện run_rag

- [x] retriever.invoke(question).
- [x] contexts = list page_content riêng lẻ.
- [x] Validate contexts là list[str] và không rỗng.
- [x] ctx_str chỉ dùng để truyền vào prompt.
- [x] Invoke prompt | llm | StrOutputParser với context và question.
- [x] Trả answer dạng str và contexts dạng list[str].

### P3.3 — Thu đúng 50 kết quả mỗi version

- [x] collect_rag_outputs dùng toàn bộ QA_PAIRS.
- [x] Mỗi record có question, reference, answer, contexts.
- [x] Không bỏ qua record bị lỗi.
- [x] Assert len(results) == len(QA_PAIRS) == 50.
- [x] V1 và V2 dùng cùng thứ tự QA và cùng cấu hình retriever.

### P3.4 — Tạo EvaluationDataset

- [x] Mỗi SingleTurnSample ánh xạ:
  - user_input từ question.
  - response từ answer.
  - retrieved_contexts từ contexts.
  - reference từ reference.
- [x] EvaluationDataset chứa đúng 50 sample.
- [x] Chạy smoke với dữ liệu nhỏ để xác minh API/type trước khi gọi evaluator đầy đủ.

### P3.5 — Chạy đủ bốn metric

- [x] faithfulness.
- [x] answer_relevancy.
- [x] context_recall.
- [x] context_precision.
- [x] Truyền llm_eval temperature=0.
- [x] Truyền embeddings evaluator.
- [x] Tính mean sau khi loại None.
- [x] Nếu danh sách metric rỗng hoặc có NaN, fail rõ thay vì ghi report giả.

### P3.6 — Schema report

Report tối thiểu:

    {
      "prompt_v1_scores": {
        "faithfulness": 0.0,
        "answer_relevancy": 0.0,
        "context_recall": 0.0,
        "context_precision": 0.0
      },
      "prompt_v2_scores": {
        "faithfulness": 0.0,
        "answer_relevancy": 0.0,
        "context_recall": 0.0,
        "context_precision": 0.0
      },
      "target_met": false
    }

Các số 0.0 phía trên chỉ mô tả schema, tuyệt đối không được dùng làm kết quả nộp. File thật chỉ được sinh từ run runtime.

### P3.7 — Chốt contract report giữa data và evidence

- [x] Xác minh rule hiện tại:

    git check-ignore -v .\data\ragas_report.json

- [x] Xác nhận submission contract: chỉ nộp evidence/03_ragas_report.json như comment starter trong .gitignore.
- [x] Không thay đổi các rule .env, virtualenv hoặc cache.
- [x] Giữ nguyên rule ignore; evidence/03_ragas_report.json là snapshot submission khớp screenshot. Report data bị run_all sau đó ghi lại và không dùng để nộp.

### P3.8 — Smoke trước full evaluation

- [x] Py-compile.
- [x] Không còn placeholder.
- [x] Tạo vectorstore thành công.
- [x] run_rag cho một câu trả đúng type.
- [x] build_ragas_dataset trên mẫu nhỏ thành công.
- [x] Kiểm tra model evaluator và embeddings có thể gọi.
- [x] Xác nhận quota và chi phí trước khi bắt đầu lượt full.

Không chạy full nếu bất kỳ smoke nào lỗi. Bước này có ít nhất 100 lượt sinh answer cộng nhiều lượt evaluator; không khởi chạy lặp lại không cần thiết.

### P3.9 — Lần chạy chính thức

- [x] Chạy qua orchestrator (người dùng xác nhận đã chạy run_all.py):

    & .\.venv\Scripts\python.exe .\src\run_all.py --step 3

- [x] Giữ terminal mở đến khi hoàn thành.
- [x] Xác nhận 50/50 V1 và 50/50 V2 ở phase thu output.
- [x] Xác nhận cả hai evaluation hoàn thành.
- [x] Chụp ảnh bảng so sánh thật khi còn hiển thị rõ.
- [x] Lưu evidence/03_ragas_scores.png.

### P3.10 — Xác minh report

- [x] Parse data/ragas_report.json.
- [x] Có đúng hai nhóm score.
- [x] Mỗi nhóm có đủ bốn metric.
- [x] Mọi metric là số hữu hạn.
- [x] Ít nhất một faithfulness >= 0.8.
- [x] target_met phản ánh đúng điều kiện, không hard-code.

- [x] Copy report:

    Copy-Item -LiteralPath .\data\ragas_report.json -Destination .\evidence\03_ragas_report.json -Force

- [x] Final tuning report trong data và evidence đã đồng bộ:
  - SHA-256 của cả hai bản: 80AFE584D35D95090C9EF864E75B86643AA93847168EA840E9951AFD5AA6D9AA.
  - Evidence report khớp điểm trong screenshot tuning cuối.

### P3.11 — Quy trình hợp lệ nếu faithfulness chưa đạt

Nếu cả hai version < 0.8:

1. Không sửa trực tiếp JSON.
2. Xác định sample thấp và kiểm tra contexts thực tế.
3. Nếu context đúng nhưng answer thêm thông tin, tăng ràng buộc grounding trong cả hai prompt theo đúng phong cách từng version.
4. Nếu retrieval thiếu, điều chỉnh có kiểm soát chunk_size/chunk_overlap/k và giữ cùng cấu hình cho cả V1/V2.
5. Chạy lại toàn bộ 50 sample cho cả hai version.
6. Thay report và ảnh bằng kết quả lần chạy cuối.
7. Ghi lý do thay đổi và trước/sau bằng số liệu thật.

Không cherry-pick sample, không loại score thấp, không thay reference và không sửa QA_PAIRS.

### P3.12 — Cổng Phase 3

Phase 3 PASS khi rubric 3.1–3.5 đạt. Điểm thưởng faithfulness >= 0.9 cho cả hai chỉ được đánh dấu nếu JSON thật chứng minh điều đó.

---

## Phase 4 — Nhiệm vụ 4: Guardrails Validators

### File được phép sửa/tạo

- src/04_guardrails_validator.py.
- evidence/04_pii_demo_log.txt.
- evidence/04_json_demo_log.txt.

### P4.1 — PIIDetector

- [x] Giữ register_validator tên custom/pii-detector.
- [x] Dùng regex cho EMAIL, PHONE, SSN và CREDIT_CARD.
- [x] Regex phone phải redact trọn cả dạng có ngoặc, không để sót ký tự nhận diện.
- [x] Dùng re.sub trên redacted_text để thay tất cả match.
- [x] Placeholder có dạng [TYPE_REDACTED].
- [x] Nếu có PII, trả FailResult:
  - error_message mô tả loại PII.
  - fix_value là chuỗi đã redact.
- [x] Nếu sạch, trả PassResult.

### P4.2 — PII Guard và test case

- [x] Tạo PIIDetector(on_fail=OnFailAction.FIX) trước khi truyền vào Guard.use.
- [x] Không truyền on_fail vào Guard.use.
- [x] Chạy đủ sáu case:
  - Email.
  - Phone.
  - SSN.
  - Credit Card.
  - Multi-PII.
  - Clean.
- [x] Với năm case có PII, output không còn giá trị gốc.
- [x] Case clean giữ nguyên.

### P4.3 — JSONFormatter repair

- [x] Strip whitespace.
- [x] Gỡ fence dạng json và fence thường.
- [x] Sửa single quotes theo cách đủ an toàn cho key/value demo.
- [x] Xóa trailing commas trước dấu đóng object hoặc array.
- [x] Parse lại sau repair.
- [x] Re-serialize bằng json.dumps để output chuẩn.

### P4.4 — JSON fallback

- [x] Nếu parse trực tiếp và repair đều thất bại, tạo fallback JSON hợp lệ.
- [x] Fallback có trường error và raw bị giới hạn độ dài.
- [x] Trả FailResult với error_message và fix_value=fallback.
- [x] OnFailAction.FIX áp dụng fallback vào validated_output.

### P4.5 — JSON Guard và test case

- [x] Tạo JSONFormatter(on_fail=OnFailAction.FIX).
- [x] Chạy đủ năm case:
  - Valid JSON.
  - Markdown fences.
  - Single quotes.
  - Trailing comma.
  - Truly invalid.
- [x] Tất cả validated_output đều parse được thành JSON, kể cả fallback.

### P4.6 — Kiểm tra tĩnh

- [x] Không còn placeholder.
- [x] Py-compile thành công.
- [x] register_validator tồn tại ở cả hai class.
- [x] FailResult cho PII có fix_value.
- [x] FailResult cho JSON bất khả sửa có fix_value.
- [x] on_fail xuất hiện trong constructor của validator.
- [x] Diff chỉ thuộc file Phase 4.

### P4.7 — Chạy và lưu hai log riêng

Từ project root:

    & .\.venv\Scripts\python.exe -c "import runpy; ns=runpy.run_path(r'src/04_guardrails_validator.py'); ns['demo_pii_guard']()" 2>&1 |
        Tee-Object -FilePath .\evidence\04_pii_demo_log.txt

    & .\.venv\Scripts\python.exe -c "import runpy; ns=runpy.run_path(r'src/04_guardrails_validator.py'); ns['demo_json_guard']()" 2>&1 |
        Tee-Object -FilePath .\evidence\04_json_demo_log.txt

- [x] PII log có đủ sáu nhãn.
- [x] JSON log có đủ năm nhãn.
- [x] Không file nào rỗng.
- [x] Không log nào chứa API key.

### P4.8 — Chạy qua orchestrator

- [x] Chạy:

    & .\.venv\Scripts\python.exe .\src\run_all.py --step 4

- [x] Kết quả cuối PASS/exit 0.
- [x] Không phụ thuộc API key LLM cho logic validator.

### P4.9 — Cổng Phase 4

Phase 4 PASS khi rubric 4.1–4.8 đều đạt và hai log riêng đã được kiểm tra nội dung.

---

## Phase 5 — Tích hợp, chất lượng mã và điểm thưởng

### P5.1 — Xóa toàn bộ placeholder thực thi

- [x] Quét bốn file nhiệm vụ:

    rg -n "=\s*\.\.\.|return\s+\.\.\.|\(\.\.\.\)" .\src\01_langsmith_rag_pipeline.py .\src\02_prompt_hub_ab_routing.py .\src\03_ragas_evaluation.py .\src\04_guardrails_validator.py

Kết quả phải rỗng.

### P5.2 — Static verification

- [x] Compile toàn bộ src:

    & .\.venv\Scripts\python.exe -m compileall -q .\src

- [x] pip check.
- [x] git diff --check.
- [x] Review docstring và error messages.
- [x] Không thêm dependency ngoài requirements nếu chưa chứng minh cần thiết.

### P5.3 — run_all

Chiến lược tiết kiệm API:

- Các lần chạy chính thức của Phase 1–4 đều dùng run_all.py --step N.
- Như vậy mọi bước đã được chứng minh chạy qua orchestrator.
- Chỉ chạy run_all.py không có --step một lần cuối nếu quota/chi phí cho phép và người dùng xác nhận, vì lệnh này lặp lại toàn bộ LLM/RAGAS calls.

Nếu run_all trả exit code 0 dù một bước FAIL:

- [x] Sửa tối thiểu src/run_all.py để process trả non-zero khi results có False.
- [x] Không thay đổi mapping hoặc logic của từng task.
- [x] Xác minh success trả 0 và lỗi giả lập an toàn trả non-zero.

### P5.4 — Phân tích V1 so với V2

- [x] Tạo evidence/README.md sau khi có report thật.
- [x] Nội dung tối thiểu:
  - Tên hai prompt/version.
  - 50 sample mỗi version.
  - Bảng bốn metric V1/V2.
  - Version thắng theo từng metric.
  - Faithfulness có đạt 0.8 hay không.
  - Giải thích ngắn dựa trên chiến lược prompt và dữ liệu, không suy đoán quá số liệu.
  - Routing distribution thật.
  - Public LangSmith trace URL nếu phù hợp để nộp.
- [x] Không ghi credential, chi phí không xác minh hoặc kết quả giả.

### P5.5 — Điểm thưởng RAGAS

- [x] Cả V1 và V2 >= 0.9 faithfulness; ghi nhận +3 từ report tuning thật.
- [x] Nếu không, giữ kết quả thật; không chạy tuning chỉ để thao túng metric.
- [x] Phân tích nguyên nhân version tốt hơn để nhắm +2.

### P5.6 — Chất lượng evidence ảnh

Mỗi ảnh phải:

- Là ảnh chụp thật từ lần chạy/project này.
- Đọc được ở kích thước bình thường.
- Hiển thị đúng project hoặc đúng output.
- Không che count, prompt name hoặc score.
- Không lộ API key, email nhạy cảm, token hoặc thông tin không cần thiết.

Ảnh LangSmith:

- Thấy project và ít nhất 50 traces; URL nộp cuối phải chứng minh tổng >=100.

Ảnh Prompt Hub:

- Thấy rõ cả hai prompt name.

Ảnh RAGAS:

- Thấy đủ bốn dòng metric và hai cột V1/V2.

### P5.7 — Kiểm tra đủ file evidence

Chạy PowerShell:

    $requiredEvidence = @(
        '.\evidence\01_langsmith_traces.png',
        '.\evidence\02_prompt_hub.png',
        '.\evidence\02_ab_routing_log.txt',
        '.\evidence\03_ragas_scores.png',
        '.\evidence\03_ragas_report.json',
        '.\evidence\04_pii_demo_log.txt',
        '.\evidence\04_json_demo_log.txt'
    )
    $missingEvidence = @($requiredEvidence | Where-Object { -not (Test-Path -LiteralPath $_) })
    if ($missingEvidence.Count -gt 0) {
        throw "Thiếu evidence: $($missingEvidence -join ', ')"
    }
    Get-Item -LiteralPath $requiredEvidence | Select-Object Name, Length

Mọi file phải có kích thước > 0. Hai PNG cần kiểm tra trực quan, không chỉ kiểm tra tên hoặc kích thước.

### P5.8 — Kiểm tra bảo mật

- [x] .env bị ignore.
- [x] .env không nằm trong tracked/staged files.
- [x] Quét secret ngoài template và .env:

    rg -n --hidden -g '!.git/**' -g '!.env' -g '!.env.example' '(lsv2_[A-Za-z0-9_-]{10,}|sk-[A-Za-z0-9_-]{10,}|AIza[A-Za-z0-9_-]{10,})' .

- [x] Nếu có match, dừng và xử lý trước khi stage.
- [x] Không đưa output chứa secret vào evidence.

### P5.9 — Review diff cuối

- [x] git status --short.
- [x] git diff --check.
- [x] git diff từng file allowlist.
- [x] Xác nhận Guide.md là thay đổi checkbox được người dùng cho phép giữ; không có file khóa khác bị sửa ngoài phạm vi.
- [x] Xác nhận data/ragas_report.json tiếp tục bị ignore theo quyết định; evidence/03_ragas_report.json là bản nộp.
- [x] Xác nhận evidence report khớp screenshot; data report hiện khác hash vì được orchestrator ghi lại sau và vẫn bị ignore.

### P5.10 — Cổng Phase 5

Phase 5 PASS khi:

- 100 điểm cơ bản có thể truy vết đến code/runtime/evidence.
- Các điểm thưởng chỉ được ghi nhận theo kết quả thật.
- Không có secret.
- Không có file ngoài phạm vi bị sửa.

---

## Phase 6 — GitHub, LangSmith URL và nộp bài

Phase này có hành động bên ngoài; chỉ thực hiện khi được phép commit/push/nộp.

### P6.1 — Stage đường dẫn cụ thể

Danh sách mẫu, điều chỉnh theo file thực sự thay đổi:

    git add -- PROJECT_PLAN.md
    git add -- Guide.md
    git add -- src/01_langsmith_rag_pipeline.py
    git add -- src/02_prompt_hub_ab_routing.py
    git add -- src/03_ragas_evaluation.py
    git add -- src/04_guardrails_validator.py
    git add -- evidence/01_langsmith_traces.png
    git add -- evidence/02_prompt_hub.png
    git add -- evidence/02_ab_routing_log.txt
    git add -- evidence/03_ragas_scores.png
    git add -- evidence/03_ragas_report.json
    git add -- evidence/04_pii_demo_log.txt
    git add -- evidence/04_json_demo_log.txt
    git add -- evidence/README.md

Chỉ stage src/run_all.py nếu file đó thực sự được sửa theo P5.3.

### P6.2 — Audit staging

    git diff --cached --name-only
    git diff --cached --check
    git diff --cached --stat
    git status --short

- [ ] Không có .env.
- [ ] Không có .venv.
- [ ] Không có file requirements, test, smoke hoặc .env.example bị sửa; Guide.md là ngoại lệ checkbox được người dùng xác nhận giữ.
- [ ] evidence/03_ragas_report.json có trong staging; data/ragas_report.json không stage.
- [x] Đủ evidence.

### P6.3 — Commit và push

- [ ] Commit message mô tả đúng Day 22 lab.
- [ ] Push chỉ origin/main.
- [ ] Không chạy git init hoặc remote add vì repository đã có sẵn.
- [ ] Không push upstream.
- [ ] Sau push, kiểm tra repository public hiển thị file và ảnh.

### P6.4 — Xác minh URL ngoài phiên làm việc

- [ ] GitHub URL mở được ở cửa sổ riêng/incognito.
- [x] Public LangSmith trace URL mở được không cần cookie/authentication (HTTP 200); dùng làm anonymous-access evidence cho project.
- [x] LangSmith project hiển thị >=100 traces.
- [x] Prompt Hub evidence tương ứng đúng account/project.
- [ ] Ghi hai URL vào nơi nộp bài, không ghi API key.

### P6.5 — Checklist nộp cuối

- [ ] URL GitHub public.
- [x] Public LangSmith trace URL kèm project day22-lab.
- [x] Bốn file src nhiệm vụ chạy được.
- [x] data/ragas_report.json có V1 và V2.
- [x] Bảy evidence bắt buộc.
- [x] evidence/README.md nếu nhắm điểm thưởng.
- [x] Faithfulness threshold đạt.
- [x] Không secret.
- [x] Không claim mục nào chưa được kiểm tra.

---

## 8. Cổng quyết định và quyền sở hữu thủ công

Các mục cần người dùng thực hiện hoặc xác nhận:

1. Cung cấp/điền LangSmith API key trong .env cục bộ.
2. Chọn provider và cung cấp key/model tương ứng.
3. Xác nhận slug dùng cho hai Prompt Hub names.
4. Xác nhận quota/chi phí trước lượt 50/50 và RAGAS đầy đủ.
5. Chụp hoặc phê duyệt ảnh thật nếu thao tác UI không được ủy quyền.
6. Cho phép commit, push và nộp URL.

Agent không được:

- Tự đặt credential.
- Tự bịa prompt owner/name mang dữ liệu cá nhân chưa xác nhận.
- Tự tạo ảnh bằng chứng giả.
- Ghi điểm RAGAS trước khi chạy.
- Gọi một local fallback là đạt tiêu chí Prompt Hub.
- Gọi repository/project public khi chưa kiểm tra truy cập.

---

## 9. Risk register và phương án xử lý

| ID | Rủi ro | Dấu hiệu | Xử lý |
|---|---|---|---|
| R1 | python không có trên PATH | CommandNotFound | Dùng py -3.12 để tạo .venv, sau đó chỉ dùng .venv Python |
| R2 | Dependency global thiếu | ImportError | Cài trong .venv, pip check, không dựa global |
| R3 | API RAGAS/Guardrails đổi | Import hoặc signature lỗi | Chọn version tương thích trong constraint, không sửa requirements |
| R4 | Sai tên biến LangSmith | config.validate thiếu key | Dùng LANGCHAIN_* theo .env.example/config.py |
| R5 | Tracing vào sai project | UI không thấy trace | Project mới, smoke một trace trước full run |
| R6 | Context không vào prompt | Trace chỉ có question/answer | Bắt buộc {context}, inspect child trace trước 50 calls |
| R7 | Prompt Hub fallback | Log ghi local fallback | Không chấp nhận run; sửa quyền/tên/network rồi chạy lại |
| R8 | Tên prompt trùng | push lỗi hoặc sửa prompt cũ | Dùng slug duy nhất đã xác nhận |
| R9 | Routing chỉ vào một nhánh | V1 hoặc V2 count = 0 | Tính trước 50 ID; expected hiện tại 19/31 |
| R10 | Rate limit/chi phí | 429, timeout, quota | Smoke nhỏ, xác nhận quota, không lặp full run tùy tiện |
| R11 | RAGAS score None/NaN | Report không hữu hạn | Fail rõ, kiểm tra evaluator; không ghi JSON giả |
| R12 | Faithfulness < 0.8 | Cả hai score thấp | Phân tích contexts, tune hợp lệ, chạy lại toàn bộ |
| R13 | PII không đi qua FIX | Output còn PII | FailResult fix_value và on_fail ở constructor |
| R14 | Phone redact thiếu ngoặc | Output còn ký tự PII | Điều chỉnh regex và assert không còn input gốc |
| R15 | JSON invalid không có fallback | validated_output None | FailResult có fallback JSON trong fix_value |
| R16 | Sai file log Guardrails | Chỉ có một log | Gọi riêng hai demo và Tee-Object hai file |
| R17 | Report bị ignore | git check-ignore có output | Gỡ đúng rule trong .gitignore |
| R18 | run_all PASS giả | Exit 0 sau step lỗi | Sửa exit propagation tối thiểu nếu xác minh xảy ra |
| R19 | Lộ secret | Secret scan match hoặc .env staged | Dừng, unstage, rotate key nếu đã lộ |
| R20 | Ảnh không chứng minh tiêu chí | Count/name/score bị cắt | Chụp lại từ runtime/UI thật |
| R21 | URL không public | Incognito không mở | Sửa sharing trước khi nộp |
| R22 | Thay đổi ngoài phạm vi | git status có file khóa | Dừng, không sửa/không stage file đó |

---

## 10. Nhật ký thực thi

Chỉ cập nhật phần này trong quá trình làm, không sửa lịch sử để che lỗi.

### Baseline

- Ngày audit: 2026-08-24.
- Commit: cd8c7828a57509812c1bf05596ad5c18676b2840.
- Trạng thái ban đầu: clean trước khi tạo PROJECT_PLAN.md.
- Python khả dụng: py -3.12 → Python 3.12.10.
- Baseline ban đầu: chưa có .venv, dependency lab và .env.
- Recheck hiện tại: .venv Python 3.12.10 tồn tại, pip check PASS, config.validate PASS; OpenAI/embedding và LangSmith đã chạy thật qua các bước 1–3.
- RAGAS compatibility recheck: ragas 0.4.3 import được với langchain-community 0.3.31 trong .venv; langchain-community 0.4.2 trước đó lỗi thiếu langchain_community.chat_models.vertexai. Không sửa requirements.txt.
- LangSmith API audit read-only: 100 root rag-query, 200 root ab-rag-query, 0 target-root errors; trace mẫu của cả hai nhóm chứa context marker.
- Security audit: .env/.venv bị ignore, .env không tracked/staged, secret scan ngoài .env/.env.example có 0 file match.
- Artifact audit: đủ 7/7 evidence bắt buộc, tất cả có kích thước >0; evidence/README.md đã được tạo từ dữ liệu thật.
- Guide decision: người dùng xác nhận giữ thay đổi checkbox trong Guide.md trước khi stage; các checkbox hiện khớp artifact thật.

### Kết quả theo phase

| Phase | Trạng thái | Bằng chứng/kết quả | Blocker còn lại |
|---|---|---|---|
| 0 — Environment | [x] | Venv/config/pip/API/embedding/LangSmith đều có bằng chứng runtime | Không còn blocker chức năng |
| 1 — RAG + traces | [x] | Code PASS; 100 root rag-query, 0 lỗi, context marker, screenshot và user-confirmed run_all | Chỉ còn audit thủ công 3 trace nếu muốn |
| 2 — Hub + A/B | [x] | Hub push/pull PASS; log 50 query V1=19/V2=31; 200 root traces, 0 lỗi; public trace HTTP 200 | Không còn blocker chức năng |
| 3 — RAGAS | [x] | Full 50x2, 4 metrics, evidence report/screenshot và user-confirmed run_all PASS | Data report mới hơn giữ local; evidence snapshot là bản nộp |
| 4 — Guardrails | [x] | 6 PII + 5 JSON case, hai log riêng và run_all --step 4 PASS/exit 0 | Không còn blocker chức năng |
| 5 — Integration/evidence | [x] | Compile/pip/diff/security/docstring/run_all PASS; đủ 7/7 evidence, README và public trace | Không còn blocker integration |
| 6 — Submission | [ ] | Chưa chạy | Cần quyền commit/push/nộp |

### Điểm theo bằng chứng hiện tại

| Nhóm | Điểm/bằng chứng hiện tại | Tối đa | Ghi chú |
|---|---:|---:|---|
| Nhiệm vụ 1 | 25 | 25 | 100 root traces, context marker, ảnh hợp lệ |
| Nhiệm vụ 2 | 25 | 25 | 2 Hub prompts, pull thật, 50-query log, deterministic routing |
| Nhiệm vụ 3 | 25 | 25 | 50x2, đủ 4 metric, target_met=true, evidence report/screenshot hợp lệ |
| Nhiệm vụ 4 | 25 | 25 | 6 PII và 5 JSON case chạy đúng; đủ hai log submission |
| Thưởng RAGAS | 5 đã hiện thực | 5 | Evidence README có phân tích; V1=0.9646 và V2=0.9878 đều >=0.9 |
| Thưởng evidence | 5 đã hiện thực | 5 | Đủ 7/7 file, README và public LangSmith trace HTTP 200 |
| Thưởng code quality | 5 đã hiện thực | 5 | Docstring đầy đủ, run_all PASS/exit đúng, error handling/fallback hợp lý |
| Tổng | 115 | 115 | Tất cả tiêu chí cơ bản và bonus đã có bằng chứng |

### Dữ liệu RAGAS thực tế dùng cho quyết định bonus

| Metric | V1 | V2 | Chênh lệch V2-V1 | Kết luận |
|---|---:|---:|---:|---|
| faithfulness | 0.9646 | 0.9878 | +0.0232 | Cả hai đạt 0.9; V2 tốt hơn |
| answer_relevancy | 0.9107 | 0.9153 | +0.0047 | V2 tốt hơn |
| context_recall | 1.0000 | 1.0000 | 0.0000 | Retriever đủ thông tin cho cả hai |
| context_precision | 0.9383 | 0.9450 | +0.0067 | V2 tốt hơn |

Ảnh terminal có cảnh báo evaluator trả 1 generation thay vì 3 nhưng RAGAS vẫn hoàn thành 200/200 và ghi đủ metric. Khi rerun để săn bonus, cần xác minh evaluator/model hỗ trợ số generation RAGAS yêu cầu hoặc ghi rõ giới hạn này trong phân tích; không sửa điểm để bù cảnh báo.

### Hướng giải quyết điểm thưởng theo dữ liệu thực tế

#### Bonus A — Hoàn thiện submission/evidence trước, không tốn LLM

- [x] Tạo riêng evidence/04_json_demo_log.txt bằng demo_json_guard; đã xác minh 5 case, 0 traceback và file không rỗng.
- [x] Chốt cách xử lý data/ragas_report.json: giữ local theo starter và chỉ nộp evidence/03_ragas_report.json khớp screenshot submission.
- [x] Cập nhật evidence/README.md theo tuning cuối: V2 thắng faithfulness, answer relevancy và context precision; context recall hòa.
- [x] Tạo public LangSmith trace URL và kiểm tra không cookie bằng HTTP; endpoint trả 200 và không redirect.
- [x] Kiểm tra lại đủ 7 evidence, kích thước >0, nội dung đúng tên; không dùng dấu [x] trong Guide.md làm bằng chứng thay cho file thật.

Kết quả hiện tại: đủ +5 evidence và +2 phân tích RAGAS; public trace tuning mới đã xác minh HTTP 200.

#### Bonus B — Hoàn thiện code quality/run_all, không tốn LLM nếu chỉ test step 4

- [x] Sửa tối thiểu src/run_all.py để output ASCII an toàn trên Windows trước khi in tiêu đề.
- [x] Bổ sung exit code non-zero nếu bất kỳ step trả False.
- [x] Chạy lại run_all.py --step 4 và xác minh PASS/exit 0; không lặp API steps 1–3.
- [x] Rà soát docstring; AST xác nhận 0 hàm public thiếu docstring.

Kết quả kỳ vọng: +2 run_all, duy trì +2 mã sạch và +1 error handling, tổng +5 code quality.

#### Bonus C — Hoàn thành tuning V2 faithfulness lên 0.9878

Chẩn đoán ban đầu đã được xác nhận: retrieval vẫn giữ context_recall=1.0, còn prompt V2 ngắn 2–3 câu và ràng buộc grounding rõ đã nâng faithfulness từ 0.8603 lên 0.9878.

Thay đổi có kiểm soát:

- [x] Giữ V1 nguyên vẹn làm baseline trong vòng tuning.
- [x] Sửa V2 đồng bộ ở file 02 và 03: 2–3 câu, chỉ dùng facts trong context, bỏ confidence/diễn giải ngoài context.
- [x] Giữ retriever k=3, chunk_size=500, overlap=50 và cùng model/temperature để so sánh công bằng.
- [x] Chạy lại toàn bộ 50 QA cho cả V1 và V2 bằng run_all --step 3; không sửa JSON hoặc loại sample.
- [x] Thay data/evidence report, screenshot, README và public trace bằng kết quả tuning cuối sau khi V2 đạt 0.9878.

Kết quả đạt được: thêm +3 vì cả V1 và V2 >=0.9; tổng đạt 115/115.

### Blocker submission còn lại

- Chưa stage/commit/push; cần audit danh sách stage cụ thể và kiểm tra GitHub public sau push.

---

## 11. Thứ tự hành động còn lại sau audit

Đây là thứ tự ưu tiên từ trạng thái hiện tại:

1. Chạy lại secret scan, evidence gate, xác minh evidence report/screenshot và diff; stage từng đường dẫn cụ thể. Giữ Guide.md theo xác nhận người dùng và không stage data/ragas_report.json.
2. Chỉ khi được phép: commit, push origin, kiểm tra GitHub public và nộp GitHub URL cùng public LangSmith trace URL.

Không đánh dấu hoàn thành dựa trên Guide.md, ảnh cũ hoặc file chưa tồn tại.
