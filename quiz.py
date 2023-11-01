from flask import Flask, render_template, request, session
import openai
import os
import dotenv
import json

dotenv.load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/quiz", methods=["POST", "GET"])
def submit():
    if(request.method == "POST"):
        print(request.form)

        topic = request.form['topic']
        questions = request.form['questions']
        choices = request.form['choices']
        difficulty = request.form['difficulty']

        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": f"Hey chat gpt prepare a quick quiz on this topic: {topic} and prepare {questions} number of questions and for each of them keep {choices} number of choices, also keep the difficulty level {difficulty}, reply in the form of an object, make sure the response object contains topic, questions array containing question, choices and it's answer"
        #         }
        #     ],
        #     temperature=0.7
        # )

        # quiz_content = response["choices"][0]["message"]["content"]
        # print(quiz_content)
        # response = json.loads(quiz_content)

        response = {'topic': 'Computer Networks', 'questions': [{'question': 'Which protocol is used for email communication?', 'choices': ['SMTP', 'HTTP', 'FTP'], 'answer': 'SMTP'}, {'question': 'What is the purpose of a firewall in a computer network?', 'choices': ['To block viruses', 'To prevent unauthorized access', 'To increase network speed'], 'answer': 'To prevent unauthorized access'}]}
        session['response'] = response
        # print(response)
        return render_template("quiz.html", content=response)
    
    if(request.method == "GET"):
        # print(request.args)
        score = 0
        actual_answers = []
        given_answers = list(request.args.values())
        res = session.get('response', None)
        for ans in res["questions"]:
            actual_answers.append(ans["answer"])
            
        print(actual_answers)
        print(given_answers)
        for i in range(len(actual_answers)):
            if(actual_answers[i] == given_answers[i]):
                score += 1
        return render_template("score.html", score=score, correct_answers=actual_answers, given_answers=given_answers)


app.run(debug=True)
