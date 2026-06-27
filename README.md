# web3 cbt CBT Diary (去中心化認知行為治療紀錄)

這是一個基於 Web3 架構的純前端 DApp，專為認知行為治療（CBT）中的「ABCDE 思考紀錄表」設計。本專案致力於將心理健康的資料所有權 100% 交還給使用者，透過錢包簽章進行本地端加密，並將資料備份於去中心化網路，實現極致的隱私防護。

##  核心特色

* **無密碼登入：** 透過 MetaMask/phantom 等 Web3 錢包登入，無需註冊傳統帳號。
* **極致隱私（本地端加密）：** 利用使用者錢包的「訊息簽章（Signature）」動態生成 AES 密碼金鑰。資料在離開瀏覽器前即被完全加密，即使是開發者也無法讀取您的心理紀錄。
* **去中心化儲存 (IPFS)：** 加密後的紀錄檔案將上傳至 IPFS 星際文件系統，確保資料不被中心化伺服器審查或刪除。
* **不可篡改的存證 (Sepolia Testnet)：** 將 IPFS 回傳的 CID 寫入以太坊 Sepolia 測試鏈上的智能合約，實現永久的歷史存證。

## 🛠 技術棧 (Tech Stack)

* **前端框架：** React.js / Next.js, Tailwind CSS
* **Web3 互動：** Ethers.js 或 Viem / Wagmi
* **加密技術：** Web Crypto API (AES-GCM), SHA-256 金鑰衍生
* **儲存方案：** IPFS (可串接 Pinata 或 Web3.Storage SDK)
* **區塊鏈：** Ethereum Sepolia Testnet (Solidity 智能合約)

## 🔐 加密與資料流 (Data Flow)

1. **Connect:** 使用者連接錢包。
2. **Derive Key:** 請求使用者簽署固定字串（例如："Sign this message to decrypt your CBT records."）。前端將此簽章 Hash 後作為 AES-256 對稱加密金鑰。
3. **Encrypt:** 使用者填寫 ABCDE 表格，前端使用 AES 金鑰將 JSON 資料加密為密文 (Ciphertext)。
4. **Upload:** 將密文上傳至 IPFS，獲取唯一的資料指紋 CID。
5. **On-Chain:** 呼叫 Sepolia 上的智能合約，將該 CID 綁定至使用者的錢包地址。
6. **Decrypt:** 讀取歷史紀錄時，從合約取得 CID -> 從 IPFS 下載密文 -> 使用錢包簽章衍生的金鑰在本地端解密並渲染。

##  快速開始 (Getting Started)

### 1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/web3-cbt-diary.git](https://github.com/yourusername/web3-cbt-diary.git)
   ```
   
### 2.Install dependencies:
```Bash
npm install
```
Setup environment variables:

複製 .env.example 並重新命名為 .env，填入您的 IPFS API Key 與智能合約地址。

### 3.Run the development server:

```Bash
npm run dev
```

## ⚠️ 免責聲明
本工具僅供自我覺察與心理健康練習使用，無法取代專業醫療診斷、精神科治療與心理諮商。若您目前正經歷強烈的心理危機或有自我傷害的意念，請立即尋求所在地的專業醫療協助或撥打安心專線。
