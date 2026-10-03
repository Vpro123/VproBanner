# Đổi mẫu tên và biểu tượng VPro

Từ APK R33 trở lên, tên và icon mở app trong launcher đổi theo mẫu đã đóng gói. Chỉ cần sửa **launcher_template** trong [branding.json](branding.json), rồi bấm **Commit changes**.

| Giá trị launcher_template | Tên hiển thị | Mẫu |
| --- | --- | --- |
| `vpro_red` | VPro | ![VPro](branding/vpro_red.svg) |
| `vpro_gps` | VPro GPS | ![VPro GPS](branding/vpro_gps.svg) |
| `vpro_maps` | VPro Maps | ![VPro Maps](branding/vpro_maps.svg) |
| `vpro_go` | VPro Go | ![VPro Go](branding/vpro_go.svg) |

Ví dụ chuyển sang VPro Maps: sửa thành `"launcher_template": "vpro_maps"`. Giữ nguyên các trường khác.

- Khách cần cài APK hỗ trợ tính năng này một lần. Bản cũ chưa có các mẫu không tự có thêm khả năng đổi launcher.
- App kiểm tra khoảng một phút/lần khi mở bản đồ và có Internet; có tác vụ nền khoảng 15 phút do Android sắp lịch. Mất mạng, tiết kiệm pin, buộc dừng hoặc bộ nhớ đệm launcher có thể làm chậm; không phải mọi máy đổi đúng cùng một giây.
- Khi đang chạy GPS, app chờ dừng GPS rồi đồng bộ lại để đổi mẫu.
- Có thể vào bánh răng → **Biểu tượng ứng dụng** → **Đồng bộ biểu tượng** để kiểm tra ngay.
- Tên/icon trong Cài đặt Android, tên gói, chữ ký, key và các điểm đã lưu không đổi.
- Một số launcher bỏ hoặc giữ icon cũ trên màn hình chính khi chuyển alias. Khi đó kéo icon mới từ danh sách ứng dụng ra, hoặc dùng **Thêm lối tắt màn hình chính**. Lối tắt VPro đã ghim bằng chức năng này cũng được đồng bộ.
- Chỉ bốn mã trong bảng có hiệu lực. Mã sai hoặc tệp lỗi sẽ không xóa biểu tượng đang dùng.
- Các SVG ở thư mục branding là ảnh xem trước của bộ đóng gói. Thay ảnh SVG hoặc nhập tên tùy ý trên GitHub **không** thay tài nguyên bên trong APK. Muốn thêm ảnh/tên khác, cần cập nhật APK với mẫu mới; sau đó tiếp tục chọn mẫu từ xa.

## Dành cho bản chỉ hỗ trợ lối tắt (R31–R32)

Các trường `name` và `icon_url` vẫn được giữ để tương thích bản cũ. Với bản này, sửa name và tải PNG vuông qua icon_url chỉ đổi lối tắt do VPro tạo, không đổi icon trong danh sách ứng dụng. Chức năng có ở bánh răng → Biểu tượng màn hình chính.
