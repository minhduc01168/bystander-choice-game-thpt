# 📖 Hướng dẫn cài đặt và chạy chương trình

Bộ hướng dẫn này giúp bạn cài đặt và chạy **Ren'Py game** và **Streamlit dashboard** cho dự án "Bystander Choice Game".

## 📋 Yêu cầu hệ thống

- **Windows 10/11** (hoặc macOS/Linux)
- **Python 3.8+** (khuyến nghị Python 3.10 hoặc cao hơn)
- **Kết nối internet** để tải dependencies

---

## 🎮 PHẦN 1: Cài đặt và chạy Ren'Py Game

### Bước 1: Cài đặt Ren'Py Launcher

1. Truy cập trang web chính thức: [https://www.renpy.org/](https://www.renpy.org/)
2. Tải xuống **Ren'Py SDK** phù hợp với hệ điều hành của bạn:
   - **Windows**: Chọn `renpy-[version]-sdk.zip`
   - **macOS**: Chọn `renpy-[version]-sdk.dmg`
   - **Linux**: Chọn `renpy-[version]-sdk.tar.bz2`

3. Giải nén file tải xuống vào một thư mục (ví dụ: `C:\RenPy`)

### Bước 2: Mở dự án Ren'Py

1. Mở **Ren'Py Launcher** từ thư mục vừa giải nén
2. Nhấp **"Add Project"** hoặc **"Browse"**
3. Chỉ đến thư mục game của dự án:
   ```
   [đường_dẫn_dự_án]\code\bystander_choice_game\game
   ```
4. Chọn dự án này từ danh sách và nhấp **"Launch Project"** để chạy game

### Bước 3: Chạy game từ Command Line (Tùy chọn)

Nếu bạn muốn chạy game từ terminal:

#### Windows:

```powershell
# Điều hướng đến thư mục Ren'Py
cd C:\RenPy

# Chạy game (thay thế đường dẫn phù hợp)
renpy.exe "C:\đường_dẫn_dự_án\code\bystander_choice_game\game"
```

#### macOS/Linux:

```bash
# Điều hướng đến thư mục Ren'Py
cd ~/RenPy

# Chạy game
./renpy "đường_dẫn_dự_án/code/bystander_choice_game/game"
```

### Bước 4: Chơi game

- Khi game khởi động, bạn sẽ thấy menu chính
- Chọn **"Start Game"** để bắt đầu
- Thực hiện các lựa chọn trong từng scenario
- Dữ liệu lựa chọn của bạn sẽ được lưu vào:
  ```
  code/bystander_choice_game/data/choice_data.csv
  code/bystander_choice_game/data/player_results.csv
  ```

---

## 📊 PHẦN 2: Cài đặt và chạy Streamlit Dashboard

### Bước 1: Chuẩn bị môi trường Python

Mở **Terminal** hoặc **PowerShell** và điều hướng đến thư mục dự án:

```powershell
cd "C:\đường_dẫn_dự_án\code\bystander_choice_game\dashboard"
```

### Bước 2: Tạo Virtual Environment (Khuyến nghị)

Tạo một virtual environment để cô lập dependencies:

#### Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt):

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

#### macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài đặt Dependencies

Cài đặt các thư viện cần thiết từ file `requirements.txt`:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Các thư viện sẽ được cài đặt:**

- `streamlit>=1.32` - Framework cho web app
- `pandas>=2.0` - Xử lý dữ liệu
- `plotly>=5.18` - Vẽ biểu đồ tương tác

### Bước 4: Chuẩn bị dữ liệu

Dashboard cần dữ liệu từ game để hoạt động. Đảm bảo bạn đã chạy game ít nhất một lần để tạo file dữ liệu:

```
code/bystander_choice_game/data/
├── choice_data.csv
├── player_results.csv
└── player_summary.csv
```

Nếu không có dữ liệu, bạn có thể tạo dữ liệu mẫu:

```bash
# Đang ở thư mục dashboard
python data/sample_data_generator.py
```

### Bước 5: Chạy Streamlit App

Khởi động dashboard:

```bash
streamlit run app.py
```

**Kết quả dự kiến:**

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Truy cập **http://localhost:8501** trong trình duyệt web của bạn.

### Bước 6: Sử dụng Dashboard

Dashboard cung cấp các chức năng:

1. **Tabs chính:**
   - 📊 **KPI Overview** - Thống kê tổng hợp
   - 📈 **Behavior Analysis** - Phân tích hành vi
   - 🎮 **Scenario Performance** - Hiệu suất từng tình huống
   - 👤 **Player Details** - Chi tiết từng người chơi
   - 🧠 **Psychological Analysis** - Phân tích tâm lý
   - 💡 **Research Insights** - Những phát hiện chính

2. **Lọc dữ liệu:**
   - Sử dụng các filter ở sidebar để lọc theo scenario, player ID, v.v.
   - Dữ liệu sẽ cập nhật tự động

---

## 🔄 Quy trình công việc đầy đủ

### Chu kỳ normal:

1. **Chạy game Ren'Py** → sinh dữ liệu

   ```
   code/bystander_choice_game/data/choice_data.csv (các lựa chọn của người chơi)
   code/bystander_choice_game/data/player_results.csv (kết quả)
   ```

2. **Chạy Streamlit Dashboard** → phân tích dữ liệu

   ```
   streamlit run app.py
   ```

3. **Xem biểu đồ và phân tích** trong trình duyệt

### Diagram:

```
┌─────────────────────┐
│  Ren'Py Game        │
│  (code/game/)       │
└──────────┬──────────┘
           │ tạo dữ liệu
           ▼
┌─────────────────────┐
│  CSV Files          │
│  choice_data.csv    │
│  player_results.csv │
└──────────┬──────────┘
           │ đọc dữ liệu
           ▼
┌─────────────────────┐
│  Streamlit App      │
│  (dashboard/)       │
└──────────┬──────────┘
           │
           ▼
   http://localhost:8501
```

---

## 🛠️ Xử lý sự cố

### ❌ Vấn đề: "Python not found"

**Giải pháp:**

- Cài đặt Python từ [python.org](https://www.python.org/)
- Chọn **"Add Python to PATH"** khi cài đặt
- Khởi động lại terminal

### ❌ Vấn đề: "Module not found: streamlit"

**Giải pháp:**

```bash
# Kiểm tra virtual environment đã được kích hoạt chưa
# (trên Windows sẽ thấy (venv) ở đầu dòng lệnh)

# Cài đặt lại dependencies
pip install -r requirements.txt
```

### ❌ Vấn đề: "No data files found"

**Giải pháp:**

- Chạy game Ren'Py ít nhất một lần
- Hoặc tạo dữ liệu mẫu:
  ```bash
  cd dashboard
  python data/sample_data_generator.py
  streamlit run app.py
  ```

### ❌ Vấn đề: "Port 8501 already in use"

**Giải pháp:**

```bash
# Chạy trên port khác
streamlit run app.py --server.port 8502
```

### ❌ Vấn đề: "Ren'Py game không khởi động"

**Giải pháp:**

- Kiểm tra đường dẫn game folder chính xác
- Đảm bảo cấu trúc thư mục:
  ```
  game/
  ├── config/
  ├── core/
  ├── game/
  ├── screens/
  ├── story/
  └── tl/
  ```

---

## 📦 Tổng hợp Commands

### Nếu bạn cần chạy lại từ đầu:

```powershell
# 1. Vào thư mục dashboard
cd "C:\đường_dẫn_dự_án\code\bystander_choice_game\dashboard"

# 2. Tạo virtual environment (lần đầu)
python -m venv venv

# 3. Kích hoạt virtual environment
venv\Scripts\Activate.ps1

# 4. Cài đặt dependencies
pip install -r requirements.txt

# 5. Chạy app
streamlit run app.py
```

### Lần sau (nếu environment đã có):

```powershell
cd "C:\đường_dẫn_dự_án\code\bystander_choice_game\dashboard"
venv\Scripts\Activate.ps1
streamlit run app.py
```

---

## 📝 Cấu trúc dự án

```
bystander-choice-game-thpt/
├── README.md                           # Tổng quan dự án
├── INSTALLATION_GUIDE.md               # File này
├── code/
│   └── bystander_choice_game/
│       ├── game/                       # Ren'Py game folder
│       │   ├── config/                 # Cấu hình game
│       │   ├── core/                   # Logic chính
│       │   ├── story/                  # Script câu chuyện
│       │   ├── screens/                # Giao diện UI
│       │   ├── assets/                 # Hình ảnh, âm thanh
│       │   ├── saves/                  # Save game
│       │   └── data/                   # Dữ liệu output
│       │
│       └── dashboard/                  # Streamlit dashboard
│           ├── app.py                  # Ứng dụng chính
│           ├── requirements.txt        # Dependencies
│           ├── analysis.py             # Phân tích dữ liệu
│           ├── data/
│           │   ├── data_loader.py      # Tải dữ liệu CSV
│           │   └── sample_data_generator.py
│           └── helpers/
│               └── custom_style.py     # Tùy chỉnh giao diện
│
└── docs/                               # Tài liệu khác
```

---

## 🎯 Tiếp theo

- 📖 [Ren'Py Documentation](https://www.renpy.org/doc/html/)
- 📊 [Streamlit Documentation](https://docs.streamlit.io/)
- 🐼 [Pandas Documentation](https://pandas.pydata.org/docs/)
- 📈 [Plotly Documentation](https://plotly.com/python/)

---

**Cập nhật lần cuối:** 2026-09-14
