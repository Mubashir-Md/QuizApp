from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/submit", methods=["POST", "GET"])
def submit():
    if(request.method == "POST"):
        print(request.form)

        topic = request.form['topic']
        questions = request.form['questions']
        choices = request.form['choices']
        difficulty = request.form['difficulty']

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"Hey chat gpt prepare a quick quiz on this topic: {topic} and prepare {questions} number of questions and for each of them keep {choices} number of choices, also keep the difficulty level {difficulty}"
                }
            ],
            temperature=0.7
        )

        # print(response)
        # test_content = "Sure! Here's a quick quiz on recognizing animals. \
        # The difficulty level is easy.\n\nQuestion 1: Which animal is known for having a long trunk?\na) Giraffe\nb) Elephant\nc) Lion\nd) bro\n\nQuestion 2: Which animal is known for its black and white stripes?\na) Zebra\nb) Kangaroo\nc) Penguin\nd) bro\n\nQuestion 3: Which animal is known for its loud roar?\na) Tiger\nb) Dolphin\nc) Gorilla\nd) bro\n\nQuestion 4: Which animal is known for its humps?\na) Camel\nb) Cheetah\nc) Hippopotamus\nd) bro\n\nQuestion 5: Which animal is known for its large antlers?\na) Moose\nb) Penguin\nc) Kangaroo\nd) bro"
        # Extracting the quiz content from the response
        quiz_content = response["choices"][0]["message"]["content"]

        
        return render_template("submit.html", content=quiz_content, choices=choices)


app.run(debug=True)
