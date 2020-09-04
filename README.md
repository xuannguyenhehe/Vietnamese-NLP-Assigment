BÀI TẬP LỚN XỬ LÝ NGÔN NGỮ TỰ NHIÊN
TÊN: PHẠM NGUYỄN XUÂN NGUYÊN
MSSV: 1712393

Xây dựng hệ thống hỏi đáp đơn giản về các chuyến xe bus liên tỉnh bằng Quan hệ văn phạm

Cho cơ sở dữ liệu của các chuyến xe bus:
(BUS B1) (BUS B3)
(BUS B2) (BUS B4)
(ATIME B1 HUE 22:00HR) (DTIME B1 HCMC 10:00HR)
(ATIME B2 HUE 22:30HR) (DTIME B2 HCMC 12:30HR)
(ATIME B3 HCMC 05:00HR) (DTIME B3 DANANG 19:00HR)
(ATIME B4 HCMC 5:30HR) (DTIME B4 DANANG 17:30HR)
(ATIME B5 DANANG 13:30HR) (DTIME B5 HUE 8:30HR)
(ATIME B6 DANANG 9:30HR) (DTIME B6 HUE 5:30HR)
(ATIME B7 HCMC 20:30HR) (DTIME B7 HUE 8:30HR)
(RUN-TIME B1 HCMC HUE 12:00 HR) (RUN-TIME B5 DANANG HUE 5:00 HR)
(RUN-TIME B2 HCMC HUE 10:00 HR) (RUN-TIME B6 DANANG HUE 4:00 HR)
(RUN-TIME B3 DANANG HMC 14:00 HR) (RUN-TIME B7 HCMC HUE 12:00 HR)
(RUN-TIME B4 HCMC DANANG 12:00 HR)

1. Yêu cầu:
a) Dựa vào văn phạm phụ thuộc xây dựng quan hệ văn phạm để biểu diễn dạng luận lý cho các
câu truy vấn về các chuyến xe giữa thành phố Hồ Chí Minh, Huế và Đà Nẵng với cơ sở dữ liệu
đã cho ở trên.
Hiện thực chương trình cho các câu truy vấn:
Xe bus nào đến thành phố Huế lúc 20:00HR ?
Thời gian xe bus B3 từ Đà Nẵng đến Huế ?
Xe bus nào đến thành phố Hồ Chí Minh ?
Những xe bus nào đi đến Huế ?.Những xe nào xuất phát từ thành phố Hồ Chí Minh ?.
Những xe nào đi từ Đà nẵng đến thành phố Hồ Chí Minh ?.
b) Tạo dạng luận lý cho câu truy vấn trên.
c) Tạo ngữ nghĩa thủ tục từ dạng luận lý ở b).
d) Truy xuất dữ liệu để tìm thông tin trả lời cho các câu truy vấn.

2. Yêu cầu khi thực thi:
a. Ngôn ngữ sử dụng: Python 3.5
b. Cấu trúc files:
Có 2 file python như là 2 module:
- main.py: Điểm bắt đầu của chương trình, sử dụng optparse để parse các input và output
- vietnammeseNLP.py: module thực hiện parser để parse cấu trúc logical tới dạng procedure senmantic
Folder:
- inputs chứa các file input cho các câu hỏi đầu vào của bài toán
- outputs chứa các file output kết quả thực thi của mỗi câu hỏi, output của yêu cầu trước sẽ là input của yêu cầu sau
- models: các lớp hoặc các module con thực thi bài toán

3. Cài đặt
Cài đặt thư viện:
pip install pymongo
pip install pymongo[srv]
sử dụng lệnh : python main.py --model=[model file name] --input=[input name file] để chạy chương trình
Ví dụ: sử dụng lệnh: python main.py --model=model01.txt --input=input01.txt
kết quả in ra terminal là:
det_wh(Xe bus,nào)
nsubj(đến,Xe bus)
nobj(đến,Huế)
pobj(đến,20:00HR)
nmod(Huế,thành phố)
pmod(20:00HR,lúc)

(WH-QUERY s1)
(ĐẾN s1)
(PRES s1)
(AGENT s1 (XE BUS))
(TO-LOC s1 (NAME H1 HUẾ))
(AT-TIME s1 (NAME 21 20:00HR))

(WH-QUERY(ĐẾN s1 PRES) s1 [AGENT s1 XE BUS][TO-LOC s1 NAME H1 HUẾ][AT-TIME s1 NAME 21 20:00HR])
(PRINT-ALL ?b (BUS ?b)(ATIME ?b (NAME H1 HUẾ))(ATIME ?b (NAME 21 20:00HR)))
Không tìm được dữ liệu

