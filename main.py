from flask import Flask, render_template, send_file, request, redirect, url_for
import io
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import random
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


def make_text(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "lxml", from_encoding='utf-8')
        soup_text = soup.select_one('#welcome-to-flask').get_text()
        return soup_text
    else:
        print(response.status_code)

# 커스텀 색상 함수
def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = ["#2A8C82", "#41BFB3", "#91F2E9", "#275950"]
    return random.choice(colors)

# 텍스트 데이터
# text = make_text('https://flask.palletsprojects.com/en/3.0.x/')
text = open('./src/alice.txt').read()

# 이미지를 ndarray로 변환
mask = np.array(Image.open('./src/alice_mask.png'))

# 워드클라우드

# percentage = wordcloud.words_ # 객체 비율 정보 반환

@app.route('/url_input', methods=['POST'])
def url_input():
    global text
    link = request.form['link']
    text = make_text(link)
    print(text)

    return redirect(url_for('index'))

@app.route('/wordcloud.png')
def plot_png():
    global text
    wordcloud = WordCloud(max_words=300, stopwords=STOPWORDS, mask=mask, background_color='black',color_func=custom_color_func, font_path='./src/NotoSansKR-Bold.ttf').generate(text)


    # 이미지를 바이트 스트림으로 저장
    output = io.BytesIO()
    plt.figure(figsize=(10,10), frameon=False)
    plt.imshow(wordcloud)
    plt.axis('off') # 눈금 삭제
    plt.savefig(output, format='png', bbox_inches="tight", pad_inches = 0, dpi=300)
    output.seek(0)

    # 바이트 스트림을 이용해 이미지 전송
    return send_file(output, mimetype='image/png')

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)