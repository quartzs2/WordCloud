from flask import Flask, render_template, send_file
import io
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import random

app = Flask(__name__)

# 불용어 추가
STOPWORDS.add('불용어')

# 이미지를 ndarray로 변환
mask = np.array(Image.open('./src/alice_mask.png'))

# 텍스트 데이터
text = open('./src/alice.txt').read()

# 커스텀 색상 함수
def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = ["#2A8C82", "#41BFB3", "#91F2E9", "#275950"]
    return random.choice(colors)

wordcloud = WordCloud(max_words=200, stopwords=STOPWORDS, mask=mask, background_color='#260101',color_func=custom_color_func, font_path='./src/NotoSansKR-Bold.ttf').generate(text)

percentage = wordcloud.words_ # 객체 비율 정보 반환




@app.route('/wordcloud.png')
def plot_png():
    # 이미지를 바이트 스트림으로 저장
    output = io.BytesIO()
    plt.figure(figsize=(15,10))
    plt.imshow(wordcloud)
    plt.axis('off') # 눈금 삭제
    plt.savefig(output, format='png')
    output.seek(0)

    # 바이트 스트림을 이용해 이미지 전송
    return send_file(output, mimetype='image/png')

@app.route("/")
def hello():
    return render_template('index.html', stopwords = STOPWORDS)

if __name__ == "__main__":
    app.run(debug=True)