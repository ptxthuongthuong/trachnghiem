from flask import Flask, render_template_string, request, jsonify
import random

app = Flask(__name__)


disallowed_items = {
    "Hàng vi phạm bản quyền": "Các sản phẩm nhái, giả mạo nhãn hiệu hoặc bản quyền",
    "Thiết bị, trang phục quân đội": "Trang phục, phù hiệu và thiết bị của lực lượng vũ trang",
    "Tài liệu phản động & Thông tin xâm phạm đến An ninh quốc gia": "Nội dung chống phá, xuyên tạc",
    "Dịch vụ bất hợp pháp": "Dịch vụ trái phép như hack, mua bán điểm/tài khoản",
    "Súng, vũ khí và các sản phẩm có hình dạng giống vũ khí": "Súng, dao, các loại vũ khí",
    "Chất cấm, chất kích thích, chất gây nghiện, ma tuý": "Các loại ma tuý, chất cấm",
    "Thuốc lá": "Thuốc lá, thuốc lá điện tử, vape và phụ kiện",
    "Sản phẩm dành cho người lớn": "Sản phẩm người lớn, nội dung khiêu dâm",
    "Thiết bị xâm nhập": "Thiết bị phá khoá, công cụ xâm nhập",
    "Hóa chất nguy hiểm và dễ gây cháy, nổ": "Hóa chất độc hại, chất nổ",
    "Bộ phận cơ thể người và hài cốt": "Các bộ phận cơ thể người",
    "Sản phẩm gây hại cho sức khỏe": "Sản phẩm có hại cho sức khỏe",
    "Thuốc, vắc xin các loại": "Thuốc kê đơn, vắc-xin không được phép",
    "Thực vật và động vật": "Động vật hoang dã, thực vật quý hiếm",
    "Đồ cổ và tạo tác nghệ thuật": "Đồ cổ, hiện vật văn hóa",
    "Tiền giả, con dấu giả": "Tiền giả, con dấu giả mạo",
    "Thẻ tín dụng và thẻ ghi nợ": "Thẻ tín dụng, thẻ ngân hàng",
    "Tiền tệ": "Hoạt động đổi tiền không được cấp phép",
    "Thiết bị giám sát điện tử": "Thiết bị ghi âm, quay lén",
    "Các mặt hàng bị cấm vận": "Các mặt hàng bị cấm nhập khẩu",
    "Thực phẩm không tuân thủ quy định": "Thực phẩm không rõ nguồn gốc",
    "Bảo mật và quyền riêng tư": "Dịch vụ xâm phạm quyền riêng tư",
    "Sản phẩm vi phạm pháp luật": "Các sản phẩm vi phạm pháp luật",
    "Mã giảm giá Shopee": "Mua bán các mã giảm giá",
    "Sản phẩm chứa yếu tố tôn giáo, mê tín": "Vật phẩm mê tín, bùa ngải",
    "Sản phẩm kỹ thuật số": "Tài khoản game, thẻ game bất hợp pháp",
    "Thiết bị không đạt quy chuẩn": "Thiết bị không đạt chuẩn"
}

detailed_explanations = {
    "Hàng vi phạm bản quyền": "Hàng nhái, hàng giả, bản sao trái phép của một sản phẩm hay hiện vật có thể vi phạm quyền tác giả, quyền thương hiệu, hoặc các quyền sở hữu trí tuệ khác của các bên thứ ba.",
    "Thiết bị, trang phục quân đội, lực lượng thi hành pháp luật và chính phủ": "Các vật phẩm và thiết bị cấp bởi chính phủ, công an hoặc quân đội, bao gồm trang phục và các vật dụng có chứa hình ảnh quốc huy.",
    "Tài liệu phản động & Thông tin xâm phạm đến An ninh quốc gia": "Sản phẩm liên quan đến khủng bố, các tổ chức khủng bố, chiến dịch chính trị, bầu cử, các vấn đề tranh luận công khai, hoặc sản phẩm có yếu tố ủng hộ hoặc chống lại chính trị gia hoặc đảng phái chính trị.",
    "Dịch vụ bất hợp pháp": "Bao gồm các dịch vụ liên quan đến tiền giả, cổ phiếu, chứng khoán, máy chơi cờ bạc, sản phẩm may rủi, và các dịch vụ bất hợp pháp như mại dâm, tuyển dụng phi pháp, bảo hiểm lừa đảo.",
    "Súng, vũ khí và các sản phẩm có hình dạng giống vũ khí": "Bao gồm súng, vũ khí, đồ chơi có hình dáng giống vũ khí, kiếm, mác, dao găm, tay đấm gấu, và các bộ phận súng, dao có thể gây thương tích.",
    "Chất cấm, chất kích thích, chất gây nghiện, ma tuý và dụng cụ cho ma tuý bất hợp pháp": "Các chất ma túy, steroid, bóng cười, thuốc lắc, và các dụng cụ sản xuất, chế tạo hoặc tiêu thụ ma túy như ống thủy tinh, bình hóa hơi.",
    "Thuốc lá": "Thuốc lá, xì gà, thuốc lá điện tử, thuốc lá không khói, và các nguyên liệu làm thuốc lá chứa nicotine và các thiết bị hút thuốc.",
    "Sản phẩm dành cho người lớn": "Các sản phẩm liên quan đến đồ chơi tình dục, bạo dâm, sản phẩm mô tả quan hệ tình dục không hợp pháp, và các nội dung 18+ như phim, game bạo lực hoặc tình dục.",
    "Thiết bị xâm nhập": "Các thiết bị giám sát, thiết bị chia cáp, phá sóng, cắt/phá khóa, thiết bị gian lận tiết kiệm điện, thiết bị điều khiển tín hiệu giao thông và các thiết bị ghi âm, quay lén.",
    "Hóa chất nguy hiểm và dễ gây cháy, nổ": "Các loại pháo nổ, hóa chất chế tạo chất nổ, xăng, dầu, gas, bật lửa và thuốc trừ sâu, đều bị cấm bán và có thể gây nguy hiểm nghiêm trọng.",
    "Bộ phận cơ thể người và hài cốt": "Các bộ phận cơ thể người, chất thải cơ thể, dịch cơ thể, hài cốt, và các dịch vụ liên quan đến việc mua bán tinh trùng, tế bào trứng, hoặc mang thai hộ.",
    "Sản phẩm gây hại cho sức khỏe người dùng": "Các sản phẩm thực phẩm độc hại, mỹ phẩm không có chứng nhận an toàn, hoặc các sản phẩm có nguy cơ gây hại cho sức khỏe người tiêu dùng.",
    "Thuốc, vắc xin các loại": "Thuốc kê đơn, thuốc không kê đơn hạn chế, dung dịch tiêm như botox, filler, và các loại vắc-xin không đạt tiêu chuẩn.",
    "Thực vật và động vật": "Buôn bán động vật hoang dã, sản phẩm từ động vật như ngà voi, sừng tê giác, da, lông động vật, và các sản phẩm gỗ trong danh sách cấm.",
    "Đồ cổ và các tạo tác nghệ thuật": "Các hiện vật văn hóa và đồ cổ, những sản phẩm liên quan đến di sản văn hóa quốc gia bị cấm mua bán mà không có giấy phép.",
    "Tiền giả, con dấu giả": "Sản xuất và buôn bán tiền giả, con dấu giả, là tội phạm nghiêm trọng và có thể bị truy tố hình sự.",
    "Thẻ tín dụng và thẻ ghi nợ": "Buôn bán thẻ tín dụng hoặc thẻ ghi nợ đã kích hoạt liên quan đến hoạt động lừa đảo tài chính và đánh cắp danh tính.",
    "Tiền tệ": "Việc buôn bán tiền tệ phải tuân theo quy định của Ngân hàng Nhà nước và không được cấp phép có thể liên quan đến rửa tiền.",
    "Thiết bị giám sát điện tử": "Các thiết bị giám sát và các thiết bị điện tử khác có thể xâm phạm quyền riêng tư của người khác và có thể bị sử dụng cho mục đích theo dõi, quấy rối hoặc trộm cắp thông tin.",
    "Các mặt hàng bị cấm vận": "Các mặt hàng bị cấm theo quy định của pháp luật quốc tế hoặc luật Việt Nam vì lý do an ninh, chính trị hoặc các quy định thương mại.",
    "Thực phẩm không tuân thủ quy định": "Thực phẩm không rõ nguồn gốc, hết hạn hoặc không có nhãn mác đầy đủ có thể gây ngộ độc hoặc các vấn đề sức khỏe khác.",
    "Bảo mật và quyền riêng tư": "Sản phẩm và dịch vụ liên quan đến đánh cắp thông tin cá nhân, như phần mềm lừa đảo, thẻ căn cước, thẻ an sinh xã hội, và các thiết bị để thu thập thông tin cá nhân bất hợp pháp.",
    "Sản phẩm vi phạm pháp luật": "Bất kỳ sản phẩm nào vi phạm pháp luật Việt Nam hoặc có khả năng gây hại cho sức khỏe hoặc an ninh quốc gia đều bị cấm kinh doanh.",
    "Mã giảm giá Shopee": "Việc mua bán mã giảm giá vi phạm điều khoản sử dụng của Shopee, thường không có giá trị hoặc bị thu hồi khi phát hiện vi phạm.",
    "Sản phẩm chứa yếu tố tôn giáo, mê tín": "Các sản phẩm lợi dụng niềm tin tôn giáo hoặc mê tín dị đoan để trục lợi hoặc gây ảnh hưởng tiêu cực đến xã hội.",
    "Sản phẩm kỹ thuật số": "Buôn bán các sản phẩm kỹ thuật số không được cấp phép có thể vi phạm bản quyền hoặc điều khoản sử dụng của nhà phát hành.",
    "Thiết bị không đạt quy chuẩn": "Các thiết bị không đáp ứng tiêu chuẩn kỹ thuật quốc gia, có thể gây ra các vấn đề về an toàn, nhiễu sóng hoặc không tương thích với hạ tầng viễn thông."
}




allowed_items = [
    "Sách", "Quần áo", "Đồ chơi trẻ em", "Thiết bị điện tử", "Nội thất", "Thực phẩm đóng gói",
    "Mỹ phẩm", "Dụng cụ thể thao", "Vật dụng nhà bếp", "Phụ kiện thời trang", "Dụng cụ học tập"
]

def generate_quiz():
    correct_answer = random.choice(list(disallowed_items.keys()))
    wrong_answers = random.sample(allowed_items, 3)
    options = [correct_answer] + wrong_answers
    random.shuffle(options)
    
    return {
        "question": "Mặt hàng nào sau đây bị cấm?", 
        "options": options, 
        "correct_answer": correct_answer, 
        "explanation": disallowed_items[correct_answer],
        "detailed_explanation": detailed_explanations[correct_answer]
    }

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Quiz Cấm Hàng</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; background-color: #8DA47E; margin: 0; padding: 20px; }
                h2 { color: #333; }
                .container { background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); display: inline-block; margin-top: 20px; max-width: 800px; width: 100%; }
                .option-btn { display: block; width: 100%; margin: 10px auto; padding: 10px 15px; font-size: 16px; cursor: pointer; border: none; border-radius: 5px; background-color: #E9BBB5; color: #333; text-align: left; }
                .option-btn:hover { background-color: #D69A94; }
                .option-btn:disabled { opacity: 0.7; cursor: not-allowed; }
                #nextBtn { background-color: #4CAF50; margin-top: 20px; display: none; width: auto; padding: 10px 20px; margin-left: auto; margin-right: auto; text-align: center; color: white; border: none; border-radius: 5px; font-size: 16px; cursor: pointer; }
                #nextBtn:hover { background-color: #45a049; }
                .score { margin-top: 10px; font-weight: bold; }
                #result-section { margin-top: 20px; text-align: left; display: none; }
                #basic-explanation { font-weight: bold; margin-bottom: 10px; }
                #detailed-info { 
                    background-color: #f9f9f9; 
                    border-left: 4px solid #4CAF50; 
                    padding: 10px; 
                    margin-top: 10px;
                    max-height: 150px;
                    overflow-y: auto;
                    text-align: left;
                }
                .info-title { font-weight: bold; margin-bottom: 5px; color: #333; }
                .correct { background-color: #4CAF50 !important; color: white !important; }
                .incorrect { background-color: #f44336 !important; color: white !important; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2 id="question"></h2>
                <div id="options"></div>
                
                <div id="result-section">
                    <p id="basic-explanation"></p>
                    <div id="detailed-info"></div>
                </div>
                
                <button id="nextBtn" onclick="loadQuestion()">Câu tiếp theo</button>
                <div id="score" class="score">Điểm số: 0/0</div>
            </div>

            <script>
                let score = 0;
                let totalQuestions = 0;
                let currentCorrectAnswer = "";
                
                function loadQuestion() {
                    fetch("/quiz")
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById("question").innerText = data.question;
                            let optionsHtml = "";
                            data.options.forEach((opt) => {
                                optionsHtml += `<button class="option-btn" onclick="checkAnswer(this, '${opt}', '${data.correct_answer}', \`${data.explanation.replace(/`/g, "\\`")}\`, \`${data.detailed_explanation.replace(/`/g, "\\`")}\`)">${opt}</button>`;
                            });
                            document.getElementById("options").innerHTML = optionsHtml;
                            document.getElementById("result-section").style.display = "none";
                            document.getElementById("nextBtn").style.display = "none";
                            
                            currentCorrectAnswer = data.correct_answer;
                            
                            // Tăng số câu hỏi đã hiển thị
                            totalQuestions++;
                            updateScore();
                        })
                        .catch(error => {
                            console.error("Lỗi khi tải câu hỏi:", error);
                            alert("Có lỗi xảy ra khi tải câu hỏi. Vui lòng thử lại.");
                        });
                }
                
                function checkAnswer(buttonElement, selected, correct, explanation, detailedExplanation) {
                    // Vô hiệu hóa tất cả các nút đáp án
                    let buttons = document.getElementById("options").getElementsByClassName("option-btn");
                    for (let i = 0; i < buttons.length; i++) {
                        buttons[i].disabled = true;
                        
                        // Đánh dấu đáp án đúng với màu xanh
                        if (buttons[i].innerText === correct) {
                            buttons[i].classList.add("correct");
                        }
                    }
                    
                    // Hiển thị kết quả
                    document.getElementById("result-section").style.display = "block";
                    
                    if (selected === correct) {
                        buttonElement.classList.add("correct");
                        document.getElementById("basic-explanation").innerText = "Chính xác! " + explanation;
                        document.getElementById("basic-explanation").style.color = "green";
                        score++; // Tăng điểm nếu trả lời đúng
                    } else {
                        buttonElement.classList.add("incorrect");
                        document.getElementById("basic-explanation").innerText = "Sai! Đáp án đúng là: " + correct + ". " + explanation;
                        document.getElementById("basic-explanation").style.color = "red";
                    }
                    
                    // Hiển thị thông tin chi tiết
                    document.getElementById("detailed-info").innerHTML = `
                        <div class="info-title">Thông tin chi tiết:</div>
                        <div>${detailedExplanation}</div>
                    `;
                    
                    // Hiện nút chuyển câu tiếp theo
                    document.getElementById("nextBtn").style.display = "block";
                    
                    // Cập nhật điểm số
                    updateScore();
                }
                
                function updateScore() {
                    document.getElementById("score").innerText = `Điểm số: ${score}/${totalQuestions}`;
                }
                
                // Tải câu hỏi khi trang web được tải
                window.onload = function() {
                    loadQuestion();
                };
            </script>
        </body>
        </html>
    ''')

@app.route('/quiz')
def quiz():
    return jsonify(generate_quiz())

if __name__ == '__main__':
    app.run(debug=True)