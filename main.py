from datetime import datetime, timedelta
from pathlib import Path

DATA_FILE = Path("data.txt")
INVOICE_DIR = Path("hoa_don")

# ============================================================
# 1. CẤU HÌNH TRỤ SẠC
# ============================================================
TRU_SAC = {
    "T01": {"loai": "AC", "cong_suat": 11, "don_gia": 3500},
    "T02": {"loai": "AC", "cong_suat": 11, "don_gia": 3500},
    "T03": {"loai": "DC", "cong_suat": 60, "don_gia": 4000},
    "T04": {"loai": "DC", "cong_suat": 60, "don_gia": 4000},
    "T05": {"loai": "DC", "cong_suat": 60, "don_gia": 4000},
}

# Dung lượng pin dùng cho mục đích MÔ PHỎNG bài tập.
# Khi cần cập nhật thông số thực tế, chỉ sửa dictionary này.
XE_VINFAST = {
    "VF2": {"ten": "VinFast VF 2", "pin": 18.64},
    "VF3": {"ten": "VinFast VF 3", "pin": 18.64},
    "VF5": {"ten": "VinFast VF 5", "pin": 37.23},
    "VF6": {"ten": "VinFast VF 6", "pin": 59.60},
    "VF7": {"ten": "VinFast VF 7 Eco", "pin": 59.60},
    "VF7P": {"ten": "VinFast VF 7 Plus", "pin": 75.30},
    "VF8": {"ten": "VinFast VF 8", "pin": 87.70},
    "VF9": {"ten": "VinFast VF 9", "pin": 123.00},
    "E34": {"ten": "VinFast VF e34", "pin": 41.90},
    "LIMO": {"ten": "VinFast Limo Green", "pin": 59.60},
}

THOI_GIAN_QUY_DINH = 120
PHU_THU_MOI_30_PHUT = 10000

DS_PHIEN = []


# ============================================================
# 2. HÀM NHẬP DỮ LIỆU
# ============================================================
def chuan_hoa(text):
    return " ".join(text.strip().split())


def nhap_so_nguyen(thong_bao, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(thong_bao).strip())
            if min_value is not None and value < min_value:
                print(f"Lỗi: giá trị phải >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Lỗi: giá trị phải <= {max_value}.")
                continue
            return value
        except ValueError:
            print("Lỗi: vui lòng nhập số nguyên hợp lệ.")


def nhap_thoi_gian(thong_bao):
    while True:
        value = input(thong_bao).strip()
        try:
            datetime.strptime(value, "%H:%M")
            return value
        except ValueError:
            print("Lỗi: nhập theo dạng HH:MM, ví dụ 08:30.")


# ============================================================
# 3. HÀM TÌM KIẾM VÀ KIỂM TRA
# ============================================================
def tim_phien(ma_phien):
    for phien in DS_PHIEN:
        if phien["ma_phien"].lower() == ma_phien.strip().lower():
            return phien
    return None


def tru_dang_sac(ma_tru):
    return any(
        p["ma_tru"] == ma_tru and p["trang_thai"] == "Dang sac"
        for p in DS_PHIEN
    )


# ============================================================
# 4. HÀM TÍNH TOÁN
# ============================================================
def tinh_so_phut(bat_dau, ket_thuc):
    start = datetime.strptime(bat_dau, "%H:%M")
    end = datetime.strptime(ket_thuc, "%H:%M")

    # Cho phép phiên sạc qua 00:00.
    if end < start:
        end += timedelta(days=1)

    return int((end - start).total_seconds() / 60)


def tinh_kwh(phien):
    """
    Tính lượng điện nạp dựa trên dung lượng pin và SOC.
    Không cho người dùng nhập trực tiếp kWh.
    """
    return round(
        phien["dung_luong_pin"]
        * (phien["soc_sau"] - phien["soc_truoc"]) / 100,
        2
    )


def tinh_tien_dien(phien):
    return round(tinh_kwh(phien) * phien["don_gia"])


def tinh_phu_thu(phien):
    if not phien["gio_ket_thuc"]:
        return 0

    so_phut = tinh_so_phut(
        phien["gio_bat_dau"],
        phien["gio_ket_thuc"]
    )

    if so_phut <= THOI_GIAN_QUY_DINH:
        return 0

    phut_vuot = so_phut - THOI_GIAN_QUY_DINH
    so_lan = (phut_vuot + 29) // 30
    return so_lan * PHU_THU_MOI_30_PHUT


def tinh_tong_tien(phien):
    return tinh_tien_dien(phien) + tinh_phu_thu(phien)


# ============================================================
# 5. HIỂN THỊ TRỤ SẠC
# ============================================================
def hien_thi_tru():
    print("\n" + "=" * 85)
    print("DANH SÁCH TRỤ SẠC")
    print("=" * 85)
    print(
        f"{'Mã trụ':<10}{'Loại':<10}"
        f"{'Công suất':<18}{'Đơn giá':<22}{'Trạng thái'}"
    )

    for ma, info in TRU_SAC.items():
        state = "Đang sạc" if tru_dang_sac(ma) else "Trống"
        print(
            f"{ma:<10}{info['loai']:<10}"
            f"{str(info['cong_suat']) + ' kW':<18}"
            f"{info['don_gia']:>10,} đ/kWh       {state}"
        )


# ============================================================
# 6. CHỌN XE
# ============================================================
def chon_xe():
    print("\nDANH SÁCH XE VINFAST")
    print("-" * 70)

    for ma, xe in XE_VINFAST.items():
        print(f"{ma:<6} - {xe['ten']:<25} - Pin {xe['pin']} kWh")

    while True:
        ma_xe = input("Chọn mã xe: ").strip().upper()
        if ma_xe in XE_VINFAST:
            return ma_xe
        print("Mã xe không hợp lệ.")


# ============================================================
# 7. TẠO PHIÊN SẠC
# ============================================================
def tao_phien():
    print("\n--- TẠO PHIÊN SẠC ---")

    ma_phien = input("Mã phiên: ").strip()

    if not ma_phien:
        print("Lỗi: mã phiên không được để trống.")
        return

    if tim_phien(ma_phien):
        print("Lỗi: mã phiên đã tồn tại.")
        return

    hien_thi_tru()

    ma_tru = input("Chọn mã trụ: ").strip().upper()

    if ma_tru not in TRU_SAC:
        print("Lỗi: mã trụ không tồn tại.")
        return

    if tru_dang_sac(ma_tru):
        print("Lỗi: trụ đang có xe sạc, không thể mở phiên mới.")
        return

    bien_so = chuan_hoa(input("Biển số xe: "))
    chu_xe = chuan_hoa(input("Tên chủ xe: "))

    if not bien_so or not chu_xe:
        print("Lỗi: biển số và tên chủ xe không được để trống.")
        return

    ma_xe = chon_xe()
    xe = XE_VINFAST[ma_xe]

    soc_truoc = nhap_so_nguyen(
        "Phần trăm pin trước khi sạc (0-99): ",
        0, 99
    )

    soc_sau = nhap_so_nguyen(
        f"Phần trăm pin sau khi sạc ({soc_truoc + 1}-100): ",
        soc_truoc + 1, 100
    )

    gio_bat_dau = nhap_thoi_gian("Giờ bắt đầu (HH:MM): ")

    tru = TRU_SAC[ma_tru]

    DS_PHIEN.append({
        "ma_phien": ma_phien,
        "ma_tru": ma_tru,
        "loai_tru": tru["loai"],
        "cong_suat_tru": tru["cong_suat"],
        "don_gia": tru["don_gia"],
        "bien_so": bien_so,
        "chu_xe": chu_xe,
        "ma_xe": ma_xe,
        "ten_xe": xe["ten"],
        "dung_luong_pin": xe["pin"],
        "soc_truoc": soc_truoc,
        "soc_sau": soc_sau,
        "gio_bat_dau": gio_bat_dau,
        "gio_ket_thuc": "",
        "trang_thai": "Dang sac"
    })

    print("\nTạo phiên sạc thành công.")
    print("Lưu ý: khách hàng không nhập kWh hoặc đơn giá.")
    print("Chương trình sẽ tự tính lượng điện và tiền khi kết thúc phiên.")


# ============================================================
# 8. KẾT THÚC PHIÊN
# ============================================================
def ket_thuc_phien():
    print("\n--- KẾT THÚC PHIÊN SẠC ---")

    ma = input("Nhập mã phiên: ").strip()
    p = tim_phien(ma)

    if not p:
        print("Không tìm thấy phiên.")
        return

    if p["trang_thai"] != "Dang sac":
        print("Phiên này không ở trạng thái đang sạc.")
        return

    gio_ket_thuc = nhap_thoi_gian("Giờ kết thúc (HH:MM): ")

    if tinh_so_phut(p["gio_bat_dau"], gio_ket_thuc) <= 0:
        print("Lỗi: thời gian kết thúc phải sau thời gian bắt đầu.")
        return

    p["gio_ket_thuc"] = gio_ket_thuc
    p["trang_thai"] = "Hoan thanh"

    print("\nĐã hoàn thành phiên sạc.")
    print(f"Dung lượng nạp: {tinh_kwh(p):.2f} kWh")
    print(f"Tiền điện: {tinh_tien_dien(p):,} đồng")
    print(f"Phụ thu: {tinh_phu_thu(p):,} đồng")
    print(f"Tổng tiền: {tinh_tong_tien(p):,} đồng")


# ============================================================
# 9. HIỂN THỊ PHIÊN
# ============================================================
def hien_thi_phien(ds=None):
    if ds is None:
        ds = DS_PHIEN

    if not ds:
        print("Chưa có phiên sạc.")
        return
    print("\n" + "=" * 150)
    print("DANH SÁCH PHIÊN SẠC")
    print("=" * 150)

    print(
        f"{'Mã':<8}{'Trụ':<6}{'Xe':<22}"
        f"{'Biển số':<14}{'Chủ xe':<18}"
        f"{'SOC':<12}{'kWh':>9}{'Đơn giá':>13}"
        f"{'BĐ':>7}{'KT':>7}{'Trạng thái':<15}"
    )
    print("-" * 150)

    for p in ds:
        kwh = tinh_kwh(p) if p["trang_thai"] != "Dang sac" else 0
        soc = f"{p['soc_truoc']}%-{p['soc_sau']}%"

        print(
            f"{p['ma_phien']:<8}"
            f"{p['ma_tru']:<6}"
            f"{p['ten_xe'][:20]:<22}"
            f"{p['bien_so']:<14}"
            f"{p['chu_xe'][:16]:<18}"
            f"{soc:<12}"
            f"{kwh:>9.2f}"
            f"{p['don_gia']:>13,.0f}"
            f"{p['gio_bat_dau']:>7}"
            f"{p['gio_ket_thuc'] or '-':>7}"
            f"{p['trang_thai']:<15}"
        )


# ============================================================
# 10. HỦY / XÓA
# ============================================================
def huy_xoa():
    ma = input("Nhập mã phiên: ").strip()
    p = tim_phien(ma)

    if not p:
        print("Không tìm thấy phiên.")
        return

    print("1. Hủy phiên đang sạc")
    print("2. Xóa phiên khỏi danh sách")

    chon = input("Lựa chọn: ").strip()

    if chon == "1":
        if p["trang_thai"] != "Dang sac":
            print("Chỉ có thể hủy phiên đang sạc.")
            return

        gio_huy = nhap_thoi_gian("Giờ hủy (HH:MM): ")

        if tinh_so_phut(p["gio_bat_dau"], gio_huy) <= 0:
            print("Giờ hủy không hợp lệ.")
            return

        p["gio_ket_thuc"] = gio_huy
        p["trang_thai"] = "Da huy"

        print("Đã hủy phiên.")

    elif chon == "2":
        xac_nhan = input("Xác nhận xóa? (Y/N): ").strip().upper()

        if xac_nhan == "Y":
            DS_PHIEN.remove(p)
            print("Đã xóa phiên.")
        else:
            print("Đã hủy thao tác.")

    else:
        print("Lựa chọn không hợp lệ.")


# ============================================================
# 11. TÌM KIẾM
# ============================================================
def tim_kiem():
    print("\n1. Theo mã phiên")
    print("2. Theo biển số")
    print("3. Theo mã trụ")

    chon = input("Lựa chọn: ").strip()
    tu_khoa = input("Nhập từ khóa: ").strip().lower()

    if chon == "1":
        kq = [
            p for p in DS_PHIEN
            if tu_khoa in p["ma_phien"].lower()
        ]
    elif chon == "2":
        kq = [
            p for p in DS_PHIEN
            if tu_khoa in p["bien_so"].lower()
        ]
    elif chon == "3":
        kq = [
            p for p in DS_PHIEN
            if tu_khoa in p["ma_tru"].lower()
        ]
    else:
        print("Lựa chọn không hợp lệ.")
        return

    hien_thi_phien(kq)


# ============================================================
# 12. SẮP XẾP
# ============================================================
def sap_xep():
    if not DS_PHIEN:
        print("Chưa có dữ liệu.")
        return

    print("\n1. Theo kWh")
    print("2. Theo số tiền thanh toán")

    tieu_chi = input("Tiêu chí: ").strip()

    print("1. Tăng dần")
    print("2. Giảm dần")

    thu_tu = input("Thứ tự: ").strip()

    if tieu_chi not in ("1", "2") or thu_tu not in ("1", "2"):
        print("Lựa chọn không hợp lệ.")
        return

    reverse = thu_tu == "2"

    if tieu_chi == "1":
        DS_PHIEN.sort(key=tinh_kwh, reverse=reverse)
    else:
        DS_PHIEN.sort(key=tinh_tong_tien, reverse=reverse)

    hien_thi_phien()


# ============================================================
# 13. TÍNH PHÍ
# ============================================================
def xem_phi():
    ma = input("Nhập mã phiên: ").strip()
    p = tim_phien(ma)

    if not p:
        print("Không tìm thấy phiên.")
        return

    if p["trang_thai"] != "Hoan thanh":
        print("Chỉ tính thanh toán cho phiên đã hoàn thành.")
        return

    print("\n--- CHI TIẾT THANH TOÁN ---")
    print(f"Xe             : {p['ten_xe']}")
    print(f"Dung lượng pin : {p['dung_luong_pin']} kWh")
    print(f"SOC            : {p['soc_truoc']}% -> {p['soc_sau']}%")
    print(f"Dung lượng nạp : {tinh_kwh(p):.2f} kWh")
    print(f"Đơn giá        : {p['don_gia']:,.0f} đồng/kWh")
    print(f"Tiền điện      : {tinh_tien_dien(p):,} đồng")
    print(f"Phụ thu        : {tinh_phu_thu(p):,} đồng")
    print(f"Tổng thanh toán: {tinh_tong_tien(p):,} đồng")


# ============================================================
# 14. XUẤT HÓA ĐƠN
# ============================================================
def xuat_hoa_don():
    ma = input("Nhập mã phiên: ").strip()
    p = tim_phien(ma)

    if not p:
        print("Không tìm thấy phiên.")
        return

    if p["trang_thai"] != "Hoan thanh":
        print("Phiên chưa hoàn thành.")
        return

    INVOICE_DIR.mkdir(exist_ok=True)

    so_phut = tinh_so_phut(
        p["gio_bat_dau"],
        p["gio_ket_thuc"]
    )

    content = f"""============================================================
                    HOA DON SAC XE DIEN
============================================================
Ma phien        : {p['ma_phien']}
Bien so         : {p['bien_so']}
Chu xe          : {p['chu_xe']}
Xe              : {p['ten_xe']}
Dung luong pin  : {p['dung_luong_pin']} kWh
SOC             : {p['soc_truoc']}% -> {p['soc_sau']}%
Ma tru          : {p['ma_tru']} ({p['loai_tru']})
Cong suat tru   : {p['cong_suat_tru']} kW
Gio bat dau     : {p['gio_bat_dau']}
Gio ket thuc    : {p['gio_ket_thuc']}
Thoi gian       : {so_phut} phut
------------------------------------------------------------
Dung luong nap  : {tinh_kwh(p):.2f} kWh
Don gia         : {p['don_gia']:,.0f} dong/kWh
Tien dien       : {tinh_tien_dien(p):,} dong
Phu thu         : {tinh_phu_thu(p):,} dong
TONG THANH TOAN : {tinh_tong_tien(p):,} dong
============================================================
"""

    try:
        file = INVOICE_DIR / f"hoa_don_{p['ma_phien']}.txt"
        file.write_text(content, encoding="utf-8")
        print(f"Đã xuất hóa đơn: {file}")
    except OSError as e:
        print(f"Lỗi khi xuất hóa đơn: {e}")


# ============================================================
# 15. THỐNG KÊ
# ============================================================
def thong_ke():
    ds = [
        p for p in DS_PHIEN
        if p["trang_thai"] == "Hoan thanh"
    ]

    if not ds:
        print("Chưa có phiên hoàn thành.")
        return

    tong_kwh = sum(tinh_kwh(p) for p in ds)
    doanh_thu = sum(tinh_tong_tien(p) for p in ds)

    san_luong = {ma: 0 for ma in TRU_SAC}

    for p in ds:
        san_luong[p["ma_tru"]] += tinh_kwh(p)

    max_tru = max(san_luong, key=san_luong.get)

    print("\n--- THỐNG KÊ ---")
    print(f"Tổng số phiên hoàn thành : {len(ds)}")
    print(f"Tổng điện năng            : {tong_kwh:.2f} kWh")
    print(f"Tổng doanh thu            : {doanh_thu:,} đồng")
    print(
        f"Trụ có sản lượng cao nhất: "
        f"{max_tru} ({san_luong[max_tru]:.2f} kWh)"
    )


# ============================================================
# 16. LƯU FILE TXT
# ============================================================
def luu_du_lieu():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            for p in DS_PHIEN:
                fields = [
                    p["ma_phien"],
                    p["ma_tru"],
                    p["loai_tru"],
                    str(p["cong_suat_tru"]),
                    str(p["don_gia"]),
                    p["bien_so"],
                    p["chu_xe"].replace("|", "/"),
                    p["ma_xe"],
                    p["ten_xe"].replace("|", "/"),
                    str(p["dung_luong_pin"]),
                    str(p["soc_truoc"]),
                    str(p["soc_sau"]),
                    p["gio_bat_dau"],
                    p["gio_ket_thuc"],
                    p["trang_thai"]
                ]

                f.write("|".join(fields) + "\n")

        print(f"Đã lưu {len(DS_PHIEN)} phiên vào {DATA_FILE}.")

    except OSError as e:
        print(f"Lỗi ghi file: {e}")


# ============================================================
# 17. ĐỌC FILE TXT
# ============================================================
def doc_du_lieu():
    if not DATA_FILE.exists():
        print("Chưa có file dữ liệu, bắt đầu với danh sách rỗng.")
        return

    temp = []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                line = line.strip()

                if not line:
                    continue

                d = line.split("|")

                if len(d) != 15:
                    print(f"Bỏ qua dòng {line_no}: sai cấu trúc.")
                    continue

                try:
                    p = {
                        "ma_phien": d[0],
                        "ma_tru": d[1],
                        "loai_tru": d[2],
                        "cong_suat_tru": float(d[3]),
                        "don_gia": float(d[4]),
                        "bien_so": d[5],
                        "chu_xe": d[6],
                        "ma_xe": d[7],
                        "ten_xe": d[8],
                        "dung_luong_pin": float(d[9]),
                        "soc_truoc": int(d[10]),
                        "soc_sau": int(d[11]),
                        "gio_bat_dau": d[12],
                        "gio_ket_thuc": d[13],
                        "trang_thai": d[14]
                    }

                    if p["ma_tru"] not in TRU_SAC:
                        raise ValueError("Trụ không tồn tại.")

                    if p["ma_xe"] not in XE_VINFAST:
                        raise ValueError("Mẫu xe không tồn tại.")

                    if not (
                        0 <= p["soc_truoc"]
                        < p["soc_sau"]
                        <= 100
                    ):
                        raise ValueError("SOC không hợp lệ.")

                    datetime.strptime(
                        p["gio_bat_dau"], "%H:%M"
                    )

                    if p["gio_ket_thuc"]:
                        datetime.strptime(
                            p["gio_ket_thuc"], "%H:%M"
                        )

                    temp.append(p)

                except (ValueError, IndexError):
                    print(
                        f"Bỏ qua dòng {line_no}: "
                        f"dữ liệu không hợp lệ."
                    )

        DS_PHIEN.clear()
        DS_PHIEN.extend(temp)

        print(f"Đã đọc {len(DS_PHIEN)} phiên từ file.")

    except OSError as e:
        print(f"Lỗi đọc file: {e}")


# ============================================================
# 18. MENU
# ============================================================
def menu():
    print("\n" + "=" * 65)
    print("       QUẢN LÝ TRẠM SẠC XE ĐIỆN VINFAST")
    print("=" * 65)
    print("1.  Tạo phiên sạc")
    print("2.  Hiển thị danh sách trụ")
    print("3.  Hiển thị danh sách phiên")
    print("4.  Kết thúc phiên sạc")
    print("5.  Hủy / Xóa phiên")
    print("6.  Tìm kiếm")
    print("7.  Sắp xếp")
    print("8.  Tính phí")
    print("9.  Xuất hóa đơn")
    print("10. Thống kê")
    print("11. Lưu dữ liệu")
    print("12. Đọc dữ liệu")
    print("0.  Thoát")
    print("=" * 65)


# ============================================================
# 19. CHƯƠNG TRÌNH CHÍNH
# ============================================================
def chay():
    doc_du_lieu()

    while True:
        menu()

        try:
            chon = int(input("Lựa chọn: ").strip())
        except ValueError:
            print("Vui lòng nhập số.")
            continue

        if chon == 1:
            tao_phien()
        elif chon == 2:
            hien_thi_tru()
        elif chon == 3:
            hien_thi_phien()
        elif chon == 4:
            ket_thuc_phien()
        elif chon == 5:
            huy_xoa()
        elif chon == 6:
            tim_kiem()
        elif chon == 7:
            sap_xep()
        elif chon == 8:
            xem_phi()
        elif chon == 9:
            xuat_hoa_don()
        elif chon == 10:
            thong_ke()
        elif chon == 11:
            luu_du_lieu()
        elif chon == 12:
            doc_du_lieu()
        elif chon == 0:
            luu_du_lieu()
            print("Kết thúc chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    chay()
