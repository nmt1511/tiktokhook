from flask import Flask, request, render_template
import google.generativeai as genai

# Khởi tạo Flask app
app = Flask(__name__)

# Cấu hình API Key
genai.configure(api_key="AIzaSyCOPZ6_ENfEDECYGiFftiDhli_MSsk0HGk")

# Tạo cấu hình cho model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Tạo mô hình mặc định
model_name = "gemini-1.5-flash"  # model mặc định

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    # Lấy dữ liệu từ form
    input_content = request.form['input_content']
    model_choice = request.form['model_choice']  # Lấy model đã chọn từ dropdown
    
    # Cập nhật model dựa trên lựa chọn
    global model_name
    model_name = model_choice

    # Xây dựng prompt cho AI (chỉ nhắc nhở mô hình xử lý thông tin nhập vào)
    prompt = f"""
    Bạn là một nhà sáng tạo nội dung. Bạn hãy xây dựng 2 kịch bản khác nhau cho video bán hàng tiktok với nội dung được nhập vào bằng Tiếng Việt Nam như sau:
    {input_content}
    
    Yêu cầu:

    Kịch bản được chia thành 3 phần rõ ràng, mỗi phần có tiêu đề và thời gian phù hợp:
    
    - Phần 1:
    Mục tiêu là đoạn mở đầu video phải thu hút người xem tiktok trong 3 giây đầu 
    Một câu giới thiệu ngắn gọn, thu hút sự chú ý của người xem, nhấn mạnh lợi ích hoặc vấn đề mà sản phẩm giải quyết. 
    bạn có thể sử dụng ngẫu nhiên các từ gợi ý sau để mở đầu tuy nhiên phải phù hợp với sản phẩm:
    Tại sao các bạn không thử dùng/mua… (sản phẩm)?
    Đã bao giờ bạn tự hỏi (một câu hỏi) chưa?
    Làm thế nào để…?
    Tin sốc bạn đã biết chưa?
    Điều gì sẽ giúp bạn giỏi về…?
    Bạn có gặp rắc rối với … không?
    Tại sao … không dành cho bạn?
    Khám phá sự thật về… ?
    Bí mật đằng sau câu chuyện…?
    Bật mí những điều bạn chưa biết về…?
    Một số vấn đề khi dùng/mua… (sản phẩm) các bạn có giống mình không?
    Đây là sản phẩm tốt nhất mà mình từng dùng.
    Mình không thể thiếu sản phẩm này bởi vì…(các lý do).
    Cùng mình trải nghiệm… (sản phẩm/dịch vụ/hoạt động).
    Trước và sau khi sử dụng…(sản phẩm/dịch vụ).
    Cùng test thử… (sản phẩm/dịch vụ) với mình nhé.
    Vì sao (hoạt động/sản phẩm) … khiến tôi trở nên tốt hơn?
    
    - Phần 2:
    Trình bày Mô tả ngắn gọn sản phẩm với các thông tin cụ thể: 
    giá, đặc điểm nổi bật, lợi ích thực tế mà sản phẩm mang lại. 
    Nếu có thông tin về lượt bán hoặc đánh giá, hãy chèn vào để tăng độ tin cậy. 
    Không đề cập tới giá nếu không có

    - Phần 3:
    Kêu gọi người xem đặt hàng ngay ở góc trái màn hình
    ví dụ:
    Nhanh tay đặt mua ngay [tên sản phẩm] ở góc trái màn hình!  Đừng bỏ lỡ!
    
    - Sử dụng phong cách ngôn ngữ gần gũi, dễ hiểu và nhấn mạnh các lợi ích thực tế.
    - Đảm bảo thời lượng mỗi phần phù hợp.
    - Chỉ cần viết giọng đọc không cần những yếu tố khác
    - Định dạng kết quả trả về như sau:
    ---- kịch bản 1 (phong cách kịch bản) ----
    
    * Phần 1: *
    
    nội dung
    
    và cứ thế tiếp tục cho 2 và 3
    không viết gì thêm
    """

    # Tạo mô hình mới theo lựa chọn của người dùng
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )

    # Gửi prompt đến API của Google Generative AI để lấy kịch bản
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)

    # Trả về kịch bản đã tạo
    return render_template('result.html', script=response.text)

if __name__ == '__main__':
    app.run(debug=True)
