### **Spesifikasi Fitur Tugas Besar**

#### **Aktor Aplikasi**  
- **Client**: Pengguna yang meminta bantuan hukum.  
- **Lawyer**: Pengguna yang menawarkan bantuan hukum.  
- **Admin**: Mengelola aplikasi dan memastikan proses berjalan dengan baik.

#### **Model Database**  
- **Users**: Model inti untuk autentikasi dan manajemen peran.  
- **Clients**: Ekstensi dari pengguna untuk profil dan status verifikasi klien.  
- **Lawyers**: Ekstensi dari pengguna untuk profil, spesialisasi, dan status verifikasi pengacara.  
- **Cases**: Mengelola kasus hukum yang diajukan oleh klien.  
- **Documents**: Untuk mengunggah dokumen terkait kasus.  
- **Case_Updates**: Untuk mencatat perkembangan kasus.  
- **Conversations**: Untuk mengelola percakapan berbasis websocket.  
- **Messages**: Untuk mengelola pesan dalam percakapan.  

---

### **ToDo List Detail Backend**

#### **Model & Database**
1. **Create models for database integration:**
   - Buat model **Users**, **Clients**, **Lawyers**, **Cases**, **Documents**, **Case_Updates**, **Conversations**, dan **Messages** berdasarkan skema.
   - Tambahkan migrasi database (`python manage.py makemigrations` dan `python manage.py migrate`).
   - Implementasikan validasi pada model (misalnya: validasi dokumen hanya untuk kasus tertentu).

2. **Set up relationships:**
   - Hubungkan model sesuai skema (one-to-one, one-to-many, atau many-to-many).
   - Gunakan `ForeignKey`, `ManyToManyField`, atau `OneToOneField` pada model.

3. **Implement file upload:**
   - Gunakan **Django FileField** untuk dokumen dan konfigurasi direktori upload.
---

#### **Authentication & Authorization**
1. **Create authentication system:**
   - Gunakan **Django Rest Framework (DRF)** untuk API token atau JWT.
   - Tambahkan endpoint login dan logout.

2. **Role-based access:**
   - Buat middleware atau permission classes di DRF untuk membatasi akses berdasarkan peran (`client`, `lawyer`, `admin`).

3. **User registration & verification:**
   - Tambahkan endpoint untuk registrasi **Client** dan **Lawyer**.
---

#### **Admin Feature**
1. **Verified case:**
   - Endpoint untuk admin memverifikasi kasus yang diajukan klien.
   - Status verifikasi kasus diubah menjadi `verified`.

2. **Approve case:**
   - Endpoint untuk admin menyetujui atau menolak kasus.
   - Status kasus diubah menjadi `approved` atau `rejected`.

3. **Management case:**
   - Endpoint CRUD untuk admin melihat, mengubah, atau menghapus kasus.

4. **Management user:**
   - Endpoint CRUD untuk admin mengelola pengguna (verifikasi, suspend, atau hapus).

---

#### **Client Feature**
1. **Case Management:**
   - Endpoint untuk klien membuat kasus baru.
   - Melihat status kasus (open, in progress, closed).
   - Mengunggah dokumen pendukung ke kasus tertentu.
   - Mengunggah dokumen secara anonymus atau tidak dan public atau tidak 

2. **Case Updates:**
   - Melihat perkembangan kasus (dari pengacara).
   - Memberikan umpan balik atau pertanyaan terkait perkembangan kasus.

3. **Conversations:**
   - Mengirim pesan ke pengacara melalui websocket.
   - Melihat riwayat percakapan.
---

#### **Lawyer Feature**
1. **Case Assignment:**
   - Melihat daftar kasus yang ditugaskan.
   - Menerima atau menolak kasus.

2. **Case Updates:**
   - Menambahkan catatan perkembangan kasus.
   - Mengunggah dokumen tambahan untuk kasus tertentu.

3. **Conversations:**
   - Mengirim dan menerima pesan melalui websocket.
   - Melihat riwayat percakapan dengan klien.

4. **Profile Management:**
   - Memperbarui profil pengacara, termasuk spesialisasi dan detail lainnya.
---

#### **General Features**
1. **Search & Filter:**
   - Endpoint untuk mencari kasus berdasarkan status atau klien.
   - Filter percakapan berdasarkan kasus atau waktu.

2. **API Documentation:**
   - Gunakan **DRF Docs** atau **Swagger** untuk mendokumentasikan API secara otomatis.
---