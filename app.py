from flask import Flask, render_template, request, session, stream_with_context
import os
import dotenv
import json
import google.generativeai as genai

dotenv.load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

gemini_key = os.environ.get("GEMINI_API_KEY")

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/quiz", methods=["POST", "GET"])
def submit():
    if (request.method == "POST"):
        print(request.form)

        topic = request.form['topic']
        questions = request.form['questions']
        choices = request.form['choices']
        difficulty = request.form['difficulty']

        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Generate a quiz on the topic '{topic}' with {questions} questions. "
            f"Each question should have {choices} choices and the difficulty level should be '{difficulty}'. "
            "The response should be a JSON object with the following format:\n"
            "{\n"
            "  \"topic\": \"<topic>\",\n"
            "  \"questions\": [\n"
            "    {\n"
            "      \"question\": \"<question>\",\n"
            "      \"choices\": [\"<choice1>\", \"<choice2>\", \"<choice3>\"],\n"
            "      \"answer\": \"<answer>\"\n"
            "    },\n"
            "    ...\n"
            "  ]\n"
            "}"
        )
        response = model.generate_content(prompt)
        print(response)

        quiz_content = response.candidates[0].content.parts[0].text

        quiz_content = quiz_content.strip("```json\n").strip("\n```")

        print("cleaned" + quiz_content)

        if quiz_content:
            response_json = json.loads(quiz_content)
            session['response'] = response_json


            def generate():
                yield render_template("quiz.html", content=response_json)
            return app.response_class(stream_with_context(generate()))
        
        else:
            return "Error: quiz_content is empty and invalid..."
        

    if (request.method == "GET"):
        # print(request.args)
        score = 0
        actual_answers = []
        given_answers = list(request.args.values()) or []
        res = session.get('response', None)
        for ans in res["questions"]:
            actual_answers.append(ans["answer"])

        print(actual_answers)
        print(given_answers)
        if (len(given_answers) != 0):
            for i in range(len(actual_answers)):
                if (actual_answers[i] == given_answers[i]):
                    score += 1
        return render_template("score.html", score=score, correct_answers=actual_answers, given_answers=given_answers)


# @app.route("/quiz/<topic>")
# def quiz(topic):
#     res = session.get('response', None)
#     new_topic = topic.split("%20")[0]
#     print(new_topic)
#     # quiz_url = f"http://localhost:5000/quiz/{new_topic}"
#     quiz_url = f"https://ai-quiz-app.onrender.com/quiz/{new_topic}"
#     return render_template("quizDynamic.html", topic=topic, content=res, url=quiz_url)

if __name__ == "__main__":
    app.run()

