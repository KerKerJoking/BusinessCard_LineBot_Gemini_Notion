# [Python] Line名片機器人(Gemini、Notion) - 部署及操作說明

## 一、 取得程式碼

**從 GitHub 取得程式碼**

在選定的資料夾開啟命令提示字元(cmd)，並執行以下指令從 GitHub Clone專案：

```bash
git clone https://github.com/KerKerJoking/BusinessCard_LineBot_Gemini_Notion
```

## 二、 Gemini、Line、Notion 環境準備

### 取得 Google API Key

前往 [Google AI Studio](https://aistudio.google.com/app/apikey) 創建 API Key，這會用於將名片照面提交給 Google Gemini 模型進行識別並回傳 Json 格式資料。

![Google API](https://lh3.googleusercontent.com/pw/AP1GczPJ4NVuZdQSYTRRHH8ZY35w4uAn-QyFf4vSIJc50aE__aifGVP9IdW_bNSIqGaVzChDsu7KF9DwBWYPdQamMT-E_hV07sPLuZUoefi3U5XcO_m_I51H_oByN-zzPcrJIKR00m5aGs_qiYsOOWnE8teN=w1973-h827-s-no-gm?authuser=0)

### 取得 LINE Access Token / Channel Secret

登入 [LINE Developers](https://developers.line.biz/console/)，如果還沒有建立Bot就先建立一個，Access Token 可以在 Messaging API 頁面找到，Channel Secret 可以在 Basic settings 頁面找到。

![Line Access Token](https://lh3.googleusercontent.com/pw/AP1GczOirAgExqb9vp0rZ1X9io1aCk2dOsb42--6HPSFsStJ3xKTX8N7-PnGkghmrHGRklU_7DvP3-ubKcVnKh9fTYk1hd222eeDITTi3HsaG6F5R2y0Ubw7nfwu_-B_Hs7j8KkPrEQtay_gqrvEw1FhZ8cz=w1916-h1520-s-no-gm?authuser=0)

![Line Channel Secret](https://lh3.googleusercontent.com/pw/AP1GczOpnRH9m7IQqQUyCYk-OENU0lCfbbdJlpqE5Oq-Y8X3bV7OpGDWV2LJWUWlTkeT0SR7gsYlYL8F61pb6IT44Nr0Rq9v-_dojoKQxBodWWXxiwiknw2gy3Y8Nsy-p6M20vEob0iKO5fDrhcv7vINjvr0=w1384-h1578-s-no-gm?authuser=0)

### 取得 Notion Integration Secret

登入 Notion，進入 [Integrations](https://www.notion.so/profile/integrations)，創建新的 Integration 並取得 Integration Secret。

![Notion API](https://lh3.googleusercontent.com/pw/AP1GczMFxQ_mMjT21BUFnlOfi33uFQ6Zny9ORi0yqqbT9m5HTNtWn6Ndql3gs5HTYs14mXBH1bP6aTI9rdjGBahl2LT8zUd2qDvoLzRatAVPRTiPCdGKYcShJuQQY-Ki7R-OAyEYwDcDU8XyrYooNUe90jD6=w2031-h1103-s-no-gm?authuser=0)

### 建立 Notion DB

在你的 Notion 頁面建立一個新的 Data Base 用來儲存名片資訊，Data Base ID 會是 DB 頁面網址中 "/" 之後 "?v=" 之前的中間這段文字。

Data Base 的 Tittle 欄位名稱改為 "UUID"，另外分別建立欄位： "Name"、"Phone"、"Email"、"Address"、"Tittle"、"Company"，欄位格式一律使用 Text。

另外需要將剛剛建立的 Integration 連結到這個 Data Base，這樣我們才能透過 API 存取這裡面的資料。

![Notion DB](https://lh3.googleusercontent.com/pw/AP1GczNc59NqU5-bORZN9Qq2tb3Z665uKrEmK9bCO9al0uE1d2JFXgFOW9Wcij1VjmMkiSN_0S9boNAyhvGagfm_zElt-J2bXYl3c6abHoZaj4jkcUy--_uQgfN9XpxCYbZ_bRN9_IlevXZ_UGEGnwZ-ZwtW=w3060-h1421-s-no-gm?authuser=0)

## 三、 執行程式

### 執行 setup.bat

進入 Clone 下來的專案目錄，並執行 `setup.bat`，首次執行會自動建立一個 `venv` 環境，並安裝所有使用到的套件。

### 依序填入資訊

首次執行時程式會要求填入你所使用的 API 資訊，此時將稍早取得的所有 API 資訊依序填入即可，完成後會顯示 “Running on http://127.0.0.1:5000"，表示執行成功了。

![首次執行setup.bat](https://lh3.googleusercontent.com/pw/AP1GczO8gKjyzak0wOYFy3simb7AhTgrww9EgClGQ46coS0qjSOUfNGGHnRKj-_ZfYzAddOIqZm-tgXVj6QAjRgPmr6MN-4P7x3dZG_LQXtNz-1r5yEVCxlgMzfpxizGTdOCWFbPLIhmj-nv9mknL_Ysp-uu=w1766-h1134-s-no-gm?authuser=0)

## 四、 Ngrok 與 LINE Webhook 設定

這段主要是要讓我們執行的程式有一個對外服務的網址，若可以的話，修改程式碼自行對外 host 是更好的做法，但測試時可以用 ngrok。

### 下載並設定 Ngrok

前往 [Ngrok 官方網站](https://dashboard.ngrok.com/get-started/setup/windows)，下載適用於 Windows 的 Ngrok 執行檔，並將兩行指令複製下來。

![下載 ngrok](https://lh3.googleusercontent.com/pw/AP1GczNl9dFRwBikLSGXDcz9-TxNT4IPnN4DLwuPpoCzm9z74yJpSh9ETE9TPKUf_PDm6n7kqLe_VQZ4yBFcirojVi9LcLGEQ1TcCZi5ZuO6YYQTFPTyuB-EOJUlQe17iTKr9xbdBDMMfdxT2oIsGssKAy1G=w1646-h1445-s-no-gm?authuser=0)

### 執行 Ngrok

從 ngrok 所在資料夾開啟命令提示字元(cmd)，並執行剛剛從 ngrok 網站複製下來的兩條指令，不過第二條指令的 port 號 8000 要修改為 5000。執行成功後會出現一個 Forwarding 的網址，這個要複製起來貼給我們的 Linebot。

![執行cmd](https://lh3.googleusercontent.com/pw/AP1GczOFdSk7UkjVbQzHz35UFuIz_Ll_-eMhcCH1JBizw9HKor3sEunxPS-VbnHRQH8CyrbOGHsMg_7VaOo-6U1tL-3ISfHqPlPUzsOBZ6u4IYQYMSEf1an_2KFtO5yT9mDYxioIfS0C73acvYfDEL_AkcP8=w1083-h251-s-no-gm?authuser=0)

![配置 authtoken 及執行 ngrok](https://lh3.googleusercontent.com/pw/AP1GczPSMT6r_R77QlYUdbSnf_Hb-5AG_zzO5JB5DwNLgAouQ5mud0Clq5iD15d9UI7iFAFAYRcet8l7l83K4IgFNaOIO0x7rLhR8OwrUO8eSlPeyy03NHQByZ0PSTjPj8Qgcv2DWCzqOtK3mzSA-pnQl5mW=w1509-h393-s-no-gm?authuser=0)

![ngrok 執行成功](https://lh3.googleusercontent.com/pw/AP1GczMuBNZRLiHY8Z5hRRA_D7XPw9J_H1YyByJl9wh3YpBeAlc9okUpoua4EOBINT6OSeOJci-aeG-gob8LrXuIvOvXkeJx0PI7pZoIRiMeVhngChC6Wy9JhLqoMVFnBoq4G0nP6Y9UJkrJ5mtaFjmG11rU=w1452-h447-s-no-gm?authuser=0)

## 五、功能實測

### 新增名片紀錄

透過 Linebot 對話視窗傳送名片照片，程式會將名片的資訊提取出來回復在對話視窗，並同時將資料儲存到 Notion Data Base。

![新增名片紀錄](https://lh3.googleusercontent.com/pw/AP1GczOoZ1Z3jJHXoNhy_QCYoxXHarWNDdhXcnOZoDc-_fhKdqcEKAEkNJCbbuzgkB9hoACDMwvRWrWI_Ljg-HEDJLajrOPWYhA5KUoBe9zS1wN0jL2PH5sgGTvKioTImUnYfmZn7F_Ra0Q1tNu3llP3HtFI=w876-h1283-s-no-gm?authuser=0)

### 查詢名片資料

直接輸入名片擁有者的名字、公司名稱、職稱等訊息片段，Linebot 會從 Notion Data Base 查詢相關的名片資料，並直接回覆在對話視窗。

![查詢名片資料](https://lh3.googleusercontent.com/pw/AP1GczO67ESJhKWf8jko9q8gVh4IuY-u4ew0hqR9uNfUz26SDaOgBFVTpWlp0Y2m8GR3WpULCN-Fd2S6zs6ozJg5jJOKK3Iq4Yw4nBama-iwhIZ9WmTCmYir0YlA5Js0J532AqSCF9sCDpsnq64ykQWEqvc0=w870-h567-s-no-gm?authuser=0)

### 編輯名片資料

若需編輯某一筆名片資料，可以使用 `/edit` 指令，編輯成功後，Linebot 會回應該欄位已成功更新的訊息，並重新查詢該名片的資料以確認更新是否正確。

![編輯名片資料](https://lh3.googleusercontent.com/pw/AP1GczMH2TgvBUn-sSOrFO2RPJWyBcUH0iWNrMDDhg-pBa1n0uCyeVEx9jqSgZRwcmYOz_vm-un3JAK-i_psQP4h3M5jFqByTnEKOpsh7Vb7l68v0GIJh9NPBdNydcifVAKR0OxDGqFNmdJXwOmvCUFbO5LH=w875-h933-s-no-gm?authuser=0)

### 刪除名片資料

使用 `/del` 指令來刪除特定的名片資料，刪除成功後，Linebot 會回應已成功刪除該 UUID 的訊息。

![刪除名片資料](https://lh3.googleusercontent.com/pw/AP1GczNmkVSFnPE0ZTNYNMQlu9zyCXPScJBr_DeQ2Cp25S-CbNS3JJ8XQbEksWzzHG5tyGHBA2ywdoJuzuqOmJXI2lpdHtrKBbQZWp9DQmkTXkz1fzpcPAqmoOF1AN7dvEHxP3MGBZoSRuk4OHJwrathCUnL=w873-h454-s-no-gm?authuser=0)

