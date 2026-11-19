============================================================
BÀI TẬP LỚN PYTHON
XÂY DỰNG CHƯƠNG TRÌNH QUẢN LÝ TRẠM SẠC XE ĐIỆN VINFAST
============================================================

1. MỤC TIÊU
Xây dựng chương trình console bằng Python để quản lý các phiên
sạc xe điện, trụ sạc, tính điện năng tiêu thụ, tính tiền, tìm kiếm,
sắp xếp, thống kê, xuất hóa đơn và lưu/đọc dữ liệu TXT.

2. CÔNG NGHỆ
- Python 3
- List
- Dictionary
- Hàm
- if/elif/else
- for/while
- try/except
- File TXT
- datetime

3. DANH MỤC XE MÔ PHỎNG
Chương trình có:
- VinFast VF 2
- VinFast VF 3
- VinFast VF 5
- VinFast VF 6
- VinFast VF 7 Eco
- VinFast VF 7 Plus
- VinFast VF 8
- VinFast VF 9
- VinFast VF e34
- VinFast Limo Green

Lưu ý: dung lượng pin trong chương trình được dùng làm dữ liệu
mô phỏng cho bài tập. Thông số xe thực tế có thể thay đổi theo
phiên bản/thị trường/thời điểm; không dùng chương trình này làm
hệ thống thanh toán thực tế.

4. NGUYÊN TẮC QUAN TRỌNG
Khách hàng KHÔNG nhập trực tiếp:
- số kWh
- đơn giá
- số tiền

Đơn giá do hệ thống quy định theo trụ sạc.
Dung lượng điện nạp được chương trình tự tính từ dung lượng pin
và phần trăm pin trước/sau khi sạc.

5. CÔNG THỨC
KWh nạp:
    kWh = Dung lượng pin × (SOC sau - SOC trước) / 100

Tiền điện:
    Tiền điện = KWh × Đơn giá trụ

Phụ thu:
    Nếu thời gian phiên > 120 phút:
    10.000 đồng cho mỗi 30 phút vượt, làm tròn lên.

Tổng tiền:
    Tổng tiền = Tiền điện + Phụ thu

6. TRỤ SẠC MÔ PHỎNG
T01, T02:
- AC
- 11 kW
- 3.500 đồng/kWh

T03, T04, T05:
- DC
- 60 kW
- 4.000 đồng/kWh

7. CHỨC NĂNG
1. Tạo phiên sạc
2. Hiển thị danh sách trụ
3. Hiển thị danh sách phiên
4. Kết thúc phiên
5. Hủy/xóa phiên
6. Tìm kiếm
7. Sắp xếp
8. Tính phí
9. Xuất hóa đơn
10. Thống kê
11. Lưu TXT
12. Đọc TXT

8. CẤU TRÚC FILE
main.py      : chương trình chính
data.txt     : dữ liệu mẫu
hoa_don/     : nơi lưu hóa đơn
README.txt   : hướng dẫn

9. CÁCH CHẠY
Cài Python 3, sau đó mở Terminal/CMD tại thư mục chương trình:

    python main.py

10. GIẢ ĐỊNH MÔ PHỎNG
Trong thực tế, điện năng nạp phải được lấy từ công tơ/trụ sạc
và hệ thống quản lý sạc. Công thức SOC ở đây là mô hình đơn giản
phù hợp với mục đích học tập và thuyết trình bài tập lớn.
