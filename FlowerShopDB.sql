use master
go
CREATE DATABASE FlowerShopDB;
go
USE FlowerShopDB;

-- Bảng Hoa (Flowers): Lưu thông tin các loại hoa được nhận diện từ CNN
CREATE TABLE Hoa (
    HoaID INT PRIMARY KEY IDENTITY(1,1),          -- Khóa chính, tự tăng
    TenHoa NVARCHAR(100) NOT NULL UNIQUE,         -- Tên hoa (duy nhất), kết quả từ CNN
    MoTa NVARCHAR(500),                            -- Mô tả loại hoa
    AnhMacDinh NVARCHAR(255),                      -- Đường dẫn ảnh đại diện (nếu có)
    NgayTao DATETIME DEFAULT GETDATE()            -- Ngày tạo
);
GO

-- Bảng Sản phẩm (Products): Lưu các sản phẩm bán (liên kết với loại hoa)
CREATE TABLE SanPham (
    SanPhamID INT PRIMARY KEY IDENTITY(1,1),       -- Khóa chính, tự tăng
    HoaID INT NOT NULL,                           -- Khóa ngoại tham chiếu Hoa
    TenSanPham NVARCHAR(100) NOT NULL,            -- Tên sản phẩm
    Gia DECIMAL(10, 2) NOT NULL CHECK (Gia >= 0), -- Giá, không âm
    SoLuong INT NOT NULL CHECK (SoLuong >= 0),    -- Số lượng tồn kho
    AnhURL NVARCHAR(255),                         -- Đường dẫn ảnh sản phẩm
    NgayTao DATETIME DEFAULT GETDATE(),           -- Ngày tạo
    FOREIGN KEY (HoaID) REFERENCES Hoa(HoaID) ON DELETE CASCADE
);
GO

-- Bảng Người dùng (Users): Lưu thông tin khách hàng
CREATE TABLE NguoiDung (
    NguoiDungID INT PRIMARY KEY IDENTITY(1,1),    -- Khóa chính, tự tăng
    HoTen NVARCHAR(100) NOT NULL,                 -- Họ tên
    Email NVARCHAR(100) NOT NULL UNIQUE,          -- Email, duy nhất
    MatKhau NVARCHAR(255) NOT NULL,               -- Mật khẩu (nên mã hóa)
    SoDienThoai NVARCHAR(15),                     -- Số điện thoại
    DiaChi NVARCHAR(255),                         -- Địa chỉ
    VaiTro NVARCHAR(50) DEFAULT 'KhachHang',      -- Vai trò (KhachHang, Admin)
    NgayTao DATETIME DEFAULT GETDATE()            -- Ngày tạo
);
GO

-- Bảng Giỏ hàng (Cart): Lưu các sản phẩm trong giỏ hàng của người dùng
CREATE TABLE GioHang (
    GioHangID INT PRIMARY KEY IDENTITY(1,1),       -- Khóa chính, tự tăng
    NguoiDungID INT NOT NULL,                     -- Khóa ngoại tham chiếu NguoiDung
    SanPhamID INT NOT NULL,                       -- Khóa ngoại tham chiếu SanPham
    SoLuong INT NOT NULL CHECK (SoLuong > 0),     -- Số lượng, lớn hơn 0
    NgayThem DATETIME DEFAULT GETDATE(),          -- Ngày thêm vào giỏ
    FOREIGN KEY (NguoiDungID) REFERENCES NguoiDung(NguoiDungID) ON DELETE CASCADE,
    FOREIGN KEY (SanPhamID) REFERENCES SanPham(SanPhamID) ON DELETE CASCADE
);
GO

-- Bảng Hóa đơn (Orders): Lưu thông tin đơn hàng
CREATE TABLE HoaDon (
    HoaDonID INT PRIMARY KEY IDENTITY(1,1),       -- Khóa chính, tự tăng
    NguoiDungID INT NOT NULL,                     -- Khóa ngoại tham chiếu NguoiDung
    TongTien DECIMAL(12, 2) NOT NULL CHECK (TongTien >= 0), -- Tổng tiền
    NgayDat DATETIME DEFAULT GETDATE(),           -- Ngày đặt hàng
    TrangThai NVARCHAR(50) DEFAULT 'ChuaXuLy',    -- Trạng thái (ChuaXuLy, DaXuLy, DaGiao)
    DiaChiGiaoHang NVARCHAR(255) NOT NULL,        -- Địa chỉ giao hàng
    FOREIGN KEY (NguoiDungID) REFERENCES NguoiDung(NguoiDungID) ON DELETE CASCADE
);
GO

-- Bảng Chi tiết hóa đơn (OrderDetails): Lưu chi tiết sản phẩm trong hóa đơn
CREATE TABLE ChiTietHoaDon (
    ChiTietHoaDonID INT PRIMARY KEY IDENTITY(1,1), -- Khóa chính, tự tăng
    HoaDonID INT NOT NULL,                        -- Khóa ngoại tham chiếu HoaDon
    SanPhamID INT NOT NULL,                       -- Khóa ngoại tham chiếu SanPham
    SoLuong INT NOT NULL CHECK (SoLuong > 0),     -- Số lượng, lớn hơn 0
    DonGia DECIMAL(10, 2) NOT NULL CHECK (DonGia >= 0), -- Đơn giá
    ThanhTien AS (SoLuong * DonGia) PERSISTED,    -- Thành tiền, tính tự động
    FOREIGN KEY (HoaDonID) REFERENCES HoaDon(HoaDonID) ON DELETE CASCADE,
    FOREIGN KEY (SanPhamID) REFERENCES SanPham(SanPhamID) ON DELETE CASCADE
);
GO