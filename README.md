# QLKS_python_flask

Project Website Quản lý Khách sạn phát triển với Python Flask và sử dụng CSDL MySQL.

  - Đặt phòng: Khách hàng được phép thực hiên đặt phòng trực tuyến hoặc đến gặp nhân viên khách sạn để đặt phòng. Hệ thống yêu cầu hỗ trợ tìm kiếm phòng theo nhiều tiêu chí(tên, giá, ngày). Thời điểm nhận phòng không quá 28 ngày kể từ thời điểm đặt phòng.
  - Lập phiếu thuê phòng: Nhân viên lập phiếu thuê phòng khi khách hàng đến thuê hoặc đến nhận phòng đã đặt. Có 2 loại khách (nội địa và nước ngoài), mỗi phòng được ở tối đa 3 khách.
  - Thanh toán tiền phòng: Yêu cầu nhân viên thanh toán tiền phòng cho khách hàng. Đơn giá phòng dành cho 2 khách, nếu khách thứ 3 phụ thu thêm 25%. Nếu phòng có khách nước ngoài thì nhân hệ số 1.5.
  - Thống kê, báo cáo: Người quản trị được phép xem các thống kê sau theo dạng bảng và biểu đồ (sử dụng chartjs để vẽ).
    + Thống kê báo cáo về doanh thu từng tháng được chọn.
    + Thống kê tần suất sử dụng phòng theo tháng.
  - Thay đổi quy định: Người quản trị được phép
    + Thay đổi số lượng và đơn giá các loại phòng.
    + Thay đổi số lượng và hệ số các loại khách, số lượng khách tối đa trong phòng.
    + Thay đổi tỷ lệ phụ thu.
    + Người quản trị quản lý danh sách phòng (thêm/xoá/sửa/tìm kiếm phòng)
