# 開發者指引

本項目使用 `init.sql` 來初始化交易相關的資料庫表。執行 `sqlite3` 或其他 SQL 工具導入該文件即可建立所需表結構。

主要表結構如下：
- `accounts`：保存賬戶資訊與保證金數據。
- `trades`：記錄每筆交易的詳細信息。
- `positions`：追蹤當前持倉狀況。
- `price_data`：保存歷史價格資料。
- `strategy_signals`：存儲策略輸出的信號。
- `portfolio_history`：統計組合每日或每根K線的表現。

後續開發中，如需新增字段或表，請同步更新 `init.sql` 並保持文件格式一致。

## 對話規範
- 所有與開發者的對話回應應使用簡體中文。

## BINACNE API
- API密钥
1d1DpAVtc66gSvEQ7zq24kM1obDIRwD42Fqk2AtaT2MfYzPoEfu35NJV0wJEmtds
- 密钥:
8orw6ggjB7bdS3CDkRLfQBqh2s5AhDvjP2v1QOxlbZdqApFxauEKWZuEvIdNSCK6
