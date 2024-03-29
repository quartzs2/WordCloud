from flask import Flask, render_template, send_file, request, redirect, url_for, g
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
        soup = BeautifulSoup(html, "lxml")
        soup_text = soup.select_one('#welcome-to-flask').get_text()
        return soup_text
    else:
        pass

# 커스텀 색상 함수
def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    colors = ["#2A8C82", "#41BFB3", "#91F2E9", "#275950"]
    return random.choice(colors)

@app.before_request
def load_initial_text():
    if 'text' not in g:
        g.text = open('./static/src/alice.txt').read()

# 이미지를 ndarray로 변환
mask = np.array(Image.open('./static/src/alice_mask.png'))


@app.route('/generate_image', methods=['POST'])
def generate_image():
    link = request.form['link']
    text = make_text(link)

    wordcloud = WordCloud(max_words=300, stopwords=STOPWORDS, mask=mask, background_color='black', color_func=custom_color_func, font_path='./static/src/NotoSansKR-Bold.ttf').generate(text)

    plt.figure(figsize=(10,10), frameon=False)
    plt.imshow(wordcloud)
    plt.axis('off') # 눈금 삭제
    plt.savefig('./static/src/wordcloud.png', format='png', bbox_inches="tight", pad_inches = 0, dpi=300)

    return redirect(url_for('index'))



@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)