### 2. `structure.md`

```markdown
# 🗂 專案目錄結構 (Project Structure)

本專案採用純前端架構（基於 React / Next.js），將業務邏輯、Web3 互動與加密模組高度解耦，以便於未來的維護與擴充。

```text
web3-cbt-diary/
├── public/                 # 靜態資源 (Images, Favicon, Icons)
├── src/
│   ├── components/         # 可重用的 UI 元件
│   │   ├── layout/         # 頁面佈局 (Navbar, Footer)
│   │   ├── form/           # ABCDE 表格輸入元件
│   │   └── web3/           # 錢包連接按鈕、網路狀態提示
│   │
│   ├── contracts/          # 智能合約相關設定
│   │   ├── CBTDiary.json   # 智能合約的 ABI 檔案
│   │   └── addresses.js    # Sepolia 測試網的合約地址常數
│   │
│   ├── hooks/              # 自訂的 React Hooks
│   │   ├── useWeb3.js      # 處理錢包連接、簽章請求、發送交易
│   │   ├── useCrypto.js    # 封裝加解密邏輯，處理金鑰的暫存狀態
│   │   └── useIPFS.js      # 處理與 IPFS API 的上傳/下載互動
│   │
│   ├── utils/              # 無狀態的純函數工具模組
│   │   ├── encryption.js   # 核心密碼學邏輯：簽章轉 Hash、AES-GCM 加解密實作
│   │   └── formatter.js    # 資料格式化工具（時間戳轉換、地址縮寫等）
│   │
│   ├── pages/              # 路由頁面 (若為 Next.js 則為 App/Pages Router)
│   │   ├── index.js        # 首頁 (Landing Page & 錢包登入)
│   │   ├── new-record.js   # 填寫新的 ABCDE 思考紀錄表
│   │   └── history.js      # 歷史紀錄列表與解密展示
│   │
│   ├── styles/             # 全域 CSS 與 Tailwind 設定
│   └── config/             # 專案環境變數設定與常數檔
│
├── .env.example            # 環境變數範例檔
├── package.json            # 依賴套件清單
├── next.config.js          # Next.js 設定檔 (如適用)
└── README.md               # 專案說明文件

---

目錄說明
/src/hooks/useCrypto.js
這個 Hook 負責整個系統最核心的安全機制。它會呼叫 Web3 provider 請求使用者簽署特定的訊息，並將簽章傳遞給 /utils/encryption.js 以衍生出 AES Key。基於安全考量，衍生出的 Key 僅會保存在 React State 或記憶體中，絕對不會寫入 localStorage，確保使用者關閉分頁後金鑰即被銷毀。

/src/utils/encryption.js
實作 Web Crypto API 的模組。

deriveKeyFromSignature(signature): 使用 SHA-256 將簽章字串壓縮成 256-bit 的 Uint8Array 金鑰。

encryptData(data, key): 使用 AES-GCM 演算法加密 ABCDE 的 JSON 物件，會自動產生隨機的 IV (Initialization Vector)，並與密文一起打包回傳。

decryptData(encryptedBundle, key): 拆解 IV 與密文，還原出原始的 JSON 資料。

/src/contracts/
包含與以太坊 Sepolia 網路互動所需的介面。我們預期合約內會有一個映射 (Mapping) 結構，例如 mapping(address => string[]) public userCIDs，用以記錄該錢包地址擁有的所有 IPFS CIDs。前端將使用 Ethers.js 配合這裡的 ABI 呼叫 addCID(string cid) 等函數。
