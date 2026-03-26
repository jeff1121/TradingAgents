# LLM Clients - 一致性改進

## 待修正問題

### 1. `validate_model()` 從未被呼叫
- 在 `get_llm()` 中加入驗證呼叫，對未知模型發出警告（非錯誤）

### 2. 參數處理不一致
| 客戶端 | API 金鑰參數 | 特殊參數 |
|--------|---------------|----------------|
| OpenAI | `api_key` | `reasoning_effort` |
| Anthropic | `api_key` | `thinking_config` → `thinking` |
| Google | `google_api_key` | `thinking_budget` |

**修正方式：** 使用統一的 `api_key` 標準化，並對應到各供應商專用金鑰

### 3. `base_url` 被接受但未使用
- `AnthropicClient`：接受 `base_url` 但從未使用
- `GoogleClient`：接受 `base_url` 但從未使用（正確——Google 不支援此功能）

**修正方式：** 從不支援的客戶端中移除未使用的 `base_url`

### 4. 使用 CLI 的模型更新 validators.py
- 在功能 2 完成後，將 `VALID_MODELS` 字典與 CLI 模型選項同步
