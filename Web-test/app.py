from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
import logging
from results_data import results_text

app = Flask(__name__)
app.secret_key = 'secret-key'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app.config.update(
    MAIL_SERVER='smtp.yandex.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='your_email@yandex.ru', #почта
    MAIL_PASSWORD='your_password', #пароль приложений почты
    MAIL_DEFAULT_SENDER='your_email@yandex.ru' #почта
)
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start-test', methods=['POST'])
def start_test():
    session['user_name'] = request.form.get('user_name', '').strip()
    session['answers'] = {}
    return redirect(url_for('test_question', q_num=1))

@app.route('/testq<int:q_num>', methods=['GET', 'POST'])
def test_question(q_num):
    if q_num not in range(1, 11):
        flash('Такого вопроса не существует!', 'error')
        return redirect(url_for('index'))

    if 'answers' not in session:
        session['answers'] = {}

    if request.method == 'POST':
        if q_num == 10:
            comm = int(request.form.get('communication', 5))
            answer = (
                "Фундаментальная информатика и ИТ" if 1 <= comm <= 3 else
                "Программная инженерия" if 4 <= comm <= 6 else
                "Прикладная информатика" if 7 <= comm <= 8 else
                "Бизнес-информатика"
            )
        else:
            answer = request.form.get('answer')

        if not answer:
            flash('Пожалуйста, выбери ответ!', 'error')
            return render_template(f'testq{q_num}.html')

        session['answers'][f'q{q_num}'] = answer
        session.modified = True
        logger.debug(f"Ответ на q{q_num}: {answer}")

        if q_num < 10:
            scores = {}
            for q in range(1, q_num + 1):
                ans = session['answers'].get(f'q{q}')
                if ans:
                    scores[ans] = scores.get(ans, 0) + 1
            logger.debug(f"Текущий счёт после q{q_num}: {scores}")
            return redirect(url_for('test_question', q_num=q_num + 1))

        scores = {}
        for q in range(1, 10):
            ans = session['answers'].get(f'q{q}')
            if ans:
                scores[ans] = scores.get(ans, 0) + 1

        q10_answer = session['answers'].get('q10')
        if q10_answer:
            scores[q10_answer] = scores.get(q10_answer, 0) + 1

        if scores:
            session['top_direction'] = max(scores.items(), key=lambda x: x[1])[0]
        else:
            session['top_direction'] = "Прикладная информатика"
        session.modified = True
        logger.debug(f"Финальный результат: {session['top_direction']} (счёт: {scores})")
        return redirect(url_for('result'))

    return render_template(f'testq{q_num}.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if 'top_direction' not in session:
        return redirect(url_for('index'))

    top_direction = session['top_direction']

    if request.method == 'POST':
        if 'finish' in request.form:
            session.clear()
            return redirect(url_for('index'))

        user_email = request.form.get('user_email')
        if user_email:
            email_content = results_text[top_direction]["email_content"].replace('[Имя]',
                                                                                 session.get('user_name', 'Абитуриент'))
            msg = Message("Твой результат теста ПрофНавигатор", recipients=[user_email])
            msg.html = render_template('email_template.html', content=email_content)
            try:
                mail.send(msg)
                flash('Письмо успешно отправлено на твой email!', 'success')
            except Exception:
                flash('Не удалось отправить письмо. Проверь email и попробуй снова!', 'error')
        else:
            flash('Пожалуйста, введи свой email!', 'error')
        return redirect(url_for('result'))

    return render_template('result.html', direction=top_direction,
                           description=results_text[top_direction]["description"],
                           email_prompt=results_text[top_direction]["email_prompt"])

if __name__ == "__main__":
    app.run(debug=True)
