from argparse import Namespace
from flask import Flask, render_template, request, redirect, session
import enchant

app = Flask(__name__)
app.secret_key = b'dgeogjeokpeylrrekgepgjkeogje'
d = enchant.Dict("en_US")


def generate_args():
    args = Namespace(position_target="w",  # "w"=word, "t"=text.
                     number_of_times_file="num_file/of_times.txt",
                     start_position_file="num_file/start_position_prob.txt",
                     IDnum_file="num_file/IDnum.txt",
                     Nof_ex_prob_for_person="5",
                     ex_prob_file="ex_input/problems.tsv",
                     ex_question_file="ex_input/questions.tsv",
                     ex_output_A="ex_output/outputA.tsv",
                     ex_output_B="ex_output/outputB.tsv",
                     max_prob="60",
                     Nof_people_in_group=6,
                     Nof_groups=3,
                     input_problems_file_list="input/probA.tsv,"
                                              "input/probB.tsv,"
                                              "input/probC.tsv",
                                             #"input/probD.tsv",
                     input_question_file="input/questions.tsv",
                     output_before_commentary="output/not_commentary.tsv",
                     output_after_commentary="output/in_commentary.tsv")
    return args


class Question:
    """
This is question for user.
input :
file(str) : file name.
    """
    def __init__(self, file):
        self.load_file(file)

# ---------------------------------------#
    def load_file(self, file):
        with open(file, "r", encoding="UTF-8") as f:
            for line in f:
                line = line.rstrip()
                self.questions = line.split("\t")

    def get_questions(self):
        """
        :return:
        questions(list) : Print message list.
        """
        return self.questions


class Problem:
    """
    This is problem for user. English, comments, position,etc...
    input:
    file(str) : File name.
    """
    def __init__(self, file):
        self.load_file(file)

# -----------------------------------------------#
    def load_file(self, file):
        self.problems = []
        self.positions = []
        with open(file, "r", encoding="UTF-8") as f:
            for line in f:
                line = line.rstrip()
                problems = line.split("\t")
                self.problems.append(problems)

    def get_problems(self):
        """
        :return:
        problems : Print message list.
        """
        return self.problems

    def parse_position(self, problem_num):
        """
        Parse position object and make positions.
        :param problem_num(str): Problem number
        :return:
        positions(str) : position<"2:5"> -> positions<[2,5]>
        """
        position = self.problems[problem_num][3]
        self.positions = position.split(":")

    def get_positions(self):
        return self.positions


def load_userID(num_file):
    """
    Load to labeling number.
    num_file(text): It is ".txt" file written labelling number.
    return: number(int):Labeling number.
    """
    with open(num_file, "r", encoding="utf-8") as f:
        r_num = f.readline()
        r_num = r_num.rstrip()
        userID = int(r_num)

    with open(num_file, "w", encoding="utf-8") as f:
        w_num = userID + 1
        f.write(str(w_num))
    return userID


def write_start_position(file):
    """
    Write new start position. If new user, contact this function.
    """
    with open(file, "a", encoding="utf-8") as f:
        f.write("0\n")


def load_start_position(file, userID) :
    """
    Return number to start position.
    :param file(str): Name of "start position file".
    :param userID(int or str): UserID.
    :return
    start_position(str): Number of problem to start.
    """
    with open(file, "r", encoding="utf-8") as f:
        for i, num in enumerate(f):
            if i == int(userID):
                num = num.rstrip()
                start_position = num
                break
    return start_position


def rewrite_start_position(file, userID, Nof_prob):
    """
    Rewrite start position of the user.
    :param file(str): Name of "start position file".
    :param userID(int or str): UserID.
    :param Nof_prob(int or str): Number the user finished number of problems.
    """
    start_positions = []
    with open(file, "r", encoding="utf-8") as f:
        for i, num in enumerate(f):
            num = num.rstrip()
            if i == int(userID):
                num = str(Nof_prob)
            start_positions.append(num)
    with open(file, "w", encoding="utf-8") as f:
        for num in start_positions:
            f.write(num + "\n")


def check_word(text="I am man."):
    """
    Check spelling of word.
    :param text(str): sentence in english.
    :return
    miss(boolean): If there is miss , "miss" is True.
    miss_words(list): List of words are in spelling miss.
    """
    miss = False
    miss_words = []
    words = text.split(" ")
    for word in words:
        if d.check(word) is False:
            miss = True
            miss_words.append(word)
    return miss, miss_words


def add_under(english, positions, target="w"):
    """
    Add under line in english.
    :param english(str): sentence in english.
    :param positions(list): number for position adding under line.
    :param target(str): 'w'= per word, or 't'= per text.
    :return:
    english added under line.
    """
    english = english.strip()
    if "w" in target:
        english = english.split(" ")
    eng = ""
    for i, word in enumerate(english):
        if i == int(positions[0]):
            eng = eng + "<span class='under'>"
        eng = eng + word
        if i == int(positions[1]):
            eng = eng + "</span>"
        if "w" in target:
            eng = eng + " "
    return eng


def decide_problem_file(userID):
    args = generate_args()
    n = int(userID) / args.Nof_people_in_group
    while True:
        if n >= args.Nof_groups:
            n = n - args.Nof_groups
        else:
            break
    file = None

    file_list = args.input_problems_file_list.split(",")
    for i, path in enumerate(file_list):
        if i == int(n):
            file = path
    return file


@app.route("/")
def go_index():
    url = "/index"
    return redirect(url)


@app.route("/index")
def contact_index():
    """
    Push the button("初めて") -> go to page("/ready")
    Push the button("2回目以降") -> go to page("/input_useID")
    Push the button("例題へ") -> go to page("/ex/one") and start example mode.
    """
    session["ex_count"] = 0
    return render_template("index.html")


# Start example problem mode.
@app.route("/ex/one", methods=["GET"])
def start_ex_problem():
    """
    Phase one is asking user about "Is there error in english?"
    :return
    english(str): sentence of english.
    id(str): User id. (When example mode, auto setting.)
    num(str): Number What question now.
    p_id(str): Problem id.
    question(str): Sentence asking user "Is there error in english.
    """
    args = generate_args()
    session["ex_count"] += 1
    n = session["ex_count"]
    ex_p = Problem(args.ex_prob_file)
    ex_q = Question(args.ex_question_file)
    problems= ex_p.get_problems()
    ex_p.parse_position(n-1)
    posions = ex_p.get_positions()
    questions = ex_q.get_questions()
    p_id = problems[n-1][0]
    english = problems[n-1][1]
    english = add_under(english, posions, "w")
    question = questions[0]
    id = 1234
    num = "例題" + str(n)
    return render_template("one.html",
                           english=english,
                           id=id,
                           num=num,
                           p_id=p_id,
                           question=question)


@app.route("/ex/one", methods=["POST"])
def post_ex_one():
    """
    If user answers error, go phase two.
    else go phase three.
    :return:
    url(str): Path of next method.
    """
    judge = request.form.get("grammatically")
    if "error" in judge:
        url = "/ex/two"
    else:
        url = "/ex/three"
    return redirect(url)


@app.route("/ex/two", methods=["GET"])
def contact_ex_two():
    """
    Phase two is asking for user "Please answer current phrase.
    :return:
    All same as phase one.
    """
    args = generate_args()
    n = session["ex_count"]
    ex_p = Problem(args.ex_prob_file)
    ex_q = Question(args.ex_question_file)
    problems = ex_p.get_problems()
    ex_p.parse_position(n-1)
    posions = ex_p.get_positions()
    questions = ex_q.get_questions()
    question = questions[1]
    p_id = problems[n-1][0]
    english = problems[n-1][1]
    english = add_under(english, posions, "w")
    num = "例題" + str(n)
    return render_template("two.html",
                           english=english,
                           num=num,
                           p_id=p_id,
                           question=question)


@app.route("/ex/two", methods=["POST"])
def post_ex_two():
    args = generate_args()
    answer = request.form.get("answer")
    n = session["ex_count"] - 1
    with open(args.ex_output_A, "a", encoding="utf-8") as f:
        f.write(str(n))
        f.write("\t" + answer + "\n")
    url = "/ex/three"
    return redirect(url)


@app.route("/ex/three", methods=["GET"])
def contact_ex_three():
    """
    Phase three is asking user "Is there error in commentary."
    :return:
    commentary(str): Sentence commenting error in english.
    Others same as phase one.
    """
    args = generate_args()
    n = session["ex_count"]
    ex_p = Problem(args.ex_prob_file)
    ex_q = Question(args.ex_question_file)
    problems = ex_p.get_problems()
    ex_p.parse_position(n-1)
    posions = ex_p.get_positions()
    questions = ex_q.get_questions()
    question = questions[2]
    p_id = problems[n-1][0]
    english = problems[n-1][1]
    english = add_under(english, posions, "w")
    comm = problems[n-1][2]
    num = "例題" + str(n)
    return render_template("three.html",
                           english=english,
                           num=num,
                           p_id=p_id,
                           question=question,
                           commentary=comm)


@app.route("/ex/three", methods=["POST"])
def post_ex_three():
    """
    If answer "Right", go to phase four,
    else next problem or end("/ex/end").
    :return:
    url(str): Path of next method.
    """
    judge = request.form.get("commentary")
    if "right" in judge:
        url = "/ex/four"
    else:
        args = generate_args()
        if session["ex_count"] == int(args.Nof_ex_prob_for_person):
            return redirect("/ex/end")
        return redirect("/ex/one")
    return redirect(url)


@app.route("/ex/four", methods=["GET"])
def contact_ex_four():
    """
    Phase four is asking user "Is there error in english"
    after seeing the commentary.
    :return:
    All same as phase three.
    """
    args = generate_args()
    n = session["ex_count"]
    ex_p = Problem(args.ex_prob_file)
    ex_q = Question(args.ex_question_file)
    problems = ex_p.get_problems()
    ex_p.parse_position(n-1)
    posions = ex_p.get_positions()
    questions = ex_q.get_questions()
    question = questions[3]
    p_id = problems[n-1][0]
    english = problems[n-1][1]
    english = add_under(english, posions, "w")
    comm = problems[n-1][2]
    num = "例題" + str(n)
    return render_template("four.html",
                           english=english,
                           num=num,
                           p_id=p_id,
                           question=question,
                           commentary=comm)


@app.route("/ex/four", methods=["POST"])
def post_ex_four():
    """
    If answer error, go to phase five,
    else next problem or end("/ex/end").
    :return:
    url(str): Path of next method.
    """
    judge = request.form.get("grammatically")
    if "error" in judge:
        url = "/ex/five"
    else:
        args = generate_args()
        if session["ex_count"] == int(args.Nof_ex_prob_for_person):
            return redirect("/ex/end")
        return redirect("/ex/one")
    return redirect(url)


@app.route("/ex/five", methods=["GET"])
def contact_ex_five():
    """
    Phase five is asking user "Please answer current phrase"
    after seeing the commentary.
    :return:
    All same as phase three.
    """
    args = generate_args()
    n = session["ex_count"]
    ex_p = Problem(args.ex_prob_file)
    ex_q = Question(args.ex_question_file)
    problems = ex_p.get_problems()
    ex_p.parse_position(n-1)
    posions = ex_p.get_positions()
    questions = ex_q.get_questions()
    question = questions[4]
    p_id = problems[n-1][0]
    english = problems[n-1][1]
    english = add_under(english, posions, "w")
    comm = problems[n-1][2]
    num = "例題" + str(n)
    return render_template("five.html",
                           english=english,
                           num=num,
                           p_id=p_id,
                           question=question,
                           commentary=comm)


@app.route("/ex/five", methods=["POST"])
def post_ex_five():
    """
    Go to end("/ex/end") or phrase one.
    :return:
    url(str): Path of next phrase.
    """
    args = generate_args()
    answer = request.form.get("answer")
    n = session["ex_count"] - 1
    with open(args.ex_output_B, "a", encoding="utf-8") as f:
        f.write(str(n))
        f.write("\t" + answer + "\n")
    if session["ex_count"] == int(args.Nof_ex_prob_for_person):
        return redirect("/ex/end")
    return redirect("/ex/one")


@app.route("/ex/end")
def end_ex():
    return render_template("ex_end.html")
# End example problem mode.


@app.route("/ready")
def contact_ready():
    """
    If push the button("開始"), go to get_newID("/get_userID")
    :return:
    """
    return render_template("ready.html")


@app.route("/get_userID")
def get_newID():
    """
    Get new userID and start_position, and rewrite (number_of_times_file).
    :return:
    url(str): Same.
    """
    args = generate_args()
    userID = load_userID(args.IDnum_file)
    session["times"] = 1
    write_start_position(args.start_position_file)
    with open(args.number_of_times_file, "a") as f:
        f.write("1\n")
    url = str(userID) + "/one/1"
    return redirect(url)


@app.route("/input_userID", methods=["GET"])
def input_userID():
    return render_template("input_userID.html")


@app.route("/input_userID", methods=["POST"])
def post_userID():
    """
    Post userID written by user, and rewrite (number_of_times_file).
    :return:
    url(str): Same.
    """
    args = generate_args()
    userID = request.form.get("userID")
    number_of_times = []
    with open(args.number_of_times_file, "r", encoding="utf-8") as f:
        for n, line in enumerate(f):
            line = line.rstrip()
            number_of_times.append(line)
            if int(userID) == n:
                l = n

    number_of_times[l] = int(number_of_times[l]) + 1
    times = number_of_times[l]
    number_of_times[l] = str(number_of_times[l])
    with open(args.number_of_times_file, "w", encoding="utf-8") as f:
        for num in number_of_times:
            f.write(num + "\n")

    session["times"] = times
    start_position = \
        load_start_position(args.start_position_file, userID)
    prob_num = int(start_position) + 1
    url = userID + "/one/" + str(prob_num)
    return redirect(url)


@app.route("/<userID>/one/<Nof_prob>", methods=["GET"])
def contact_one(userID, Nof_prob):
    """
    Phase one is asking user about "Is there error in english?"
    :param userID(str): UserID
    :param Nof_prob(str): Problem number.
    :return:
    english(str): Sentence of english.
    id(str): UserID.
    num(str): Number What question now.
    p_id(str): Problem id.
    question(str): Sentence asking user "Is there error in english.
    """
    session["miss"] = False
    args = generate_args()
    prob_file = decide_problem_file(userID)
    prob_n = int(Nof_prob) - 1

    ques = Question(args.input_question_file)
    prob = Problem(prob_file)
    questions = ques.get_questions()
    problems = prob.get_problems()
    prob.parse_position(prob_n)
    positions = prob.get_positions()

    id = None
    if Nof_prob == "1":
        id = userID
    question = questions[0]
    num = Nof_prob + "問目"
    p_id = problems[prob_n][0]
    session["label_num"] = p_id
    english = problems[prob_n][1]
    english = add_under(english, positions, args.position_target)
    return render_template("one.html",
                           p_id=p_id,
                           id=id,
                           question=question,
                           english=english,
                           num=num)


@app.route("/<userID>/one/<Nof_prob>", methods=["POST"])
def post_one(userID, Nof_prob):
    """
    If user answers error, go phase two,
    else go phase three.
    """
    args = generate_args()
    judge = request.form.get("grammatically")
    if judge:
        if judge == "error":
            url = "/" + userID + "/two/" + Nof_prob
        else:
            times = str(session["times"])
            with open(args.output_before_commentary, "a", encoding="UTF-8") as f:
                f.write(userID + "\t" + times + "\t" +
                        session["label_num"] + "\t" + judge + "\tNone\tNone\n"
                        )
            url = "/" + userID + "/three/" + Nof_prob
    else:
        url = "/" + userID + "/one/" + Nof_prob
    return redirect(url)


@app.route("/<userID>/two/<Nof_prob>", methods=["GET"])
def contact_two(userID, Nof_prob):
    """
    Phase two is asking for user "Please answer current phrase.
    :return:
    All same as phase one.
    """
    args = generate_args()
    prob_file = decide_problem_file(userID)
    prob_n = int(Nof_prob) - 1

    ques = Question(args.input_question_file)
    prob = Problem(prob_file)
    questions = ques.get_questions()
    problems = prob.get_problems()
    prob.parse_position(prob_n)
    positions = prob.get_positions()

    miss = session.get("miss", False)
    miss_words = session.get("miss_words", None)

    question = questions[1]
    num = Nof_prob + "問目"
    p_id = problems[prob_n][0]
    english = problems[prob_n][1]
    english = add_under(english, positions, args.position_target)
    return render_template("two.html",
                           question=question,
                           english=english,
                           num=num,
                           p_id=p_id,
                           miss=miss,
                           miss_words=miss_words,)


@app.route("/<userID>/two/<Nof_prob>", methods=["POST"])
def post_two(userID, Nof_prob):
    """
    Post
    :param userID:
    :param Nof_prob:
    :return:
    """
    args = generate_args()
    session["miss"] = False

    answer = request.form.get("answer")
    answer_extra = request.form.get("answer_extra")
    if answer:
        session["miss"], session["miss_words"] = check_word(answer)
        if session["miss"] is True:
            url = "/" + userID + "/two/" + Nof_prob
            return redirect(url)
    times = str(session["times"])
    with open(args.output_before_commentary, "a", encoding="UTF-8") as f:
        f.write(userID + "\t" + times + "\t" + session["label_num"] +
                "\terror\t" + str(answer) + "\t" + str(answer_extra) + "\n"
                )
    url = "/" + userID + "/three/" + Nof_prob
    return redirect(url)


@app.route("/<userID>/three/<Nof_prob>", methods=["GET"])
def contact_three(userID, Nof_prob):
    args = generate_args()
    session["miss"] = False

    prob_file = decide_problem_file(userID)
    prob_n = int(Nof_prob) - 1

    ques = Question(args.input_question_file)
    prob = Problem(prob_file)
    questions = ques.get_questions()
    problems = prob.get_problems()
    prob.parse_position(prob_n)
    positions = prob.get_positions()

    question = questions[2]
    num = Nof_prob + "問目"
    p_id = problems[prob_n][0]
    english = problems[prob_n][1]
    english = add_under(english, positions, args.position_target)
    commentary = problems[prob_n][2]
    return render_template("three.html",
                           question=question,
                           num=num,
                           p_id=p_id,
                           english=english,
                           commentary=commentary)


@app.route("/<userID>/three/<Nof_prob>", methods=["POST"])
def post_three(userID, Nof_prob):
    args = generate_args()
    ans_comm = request.form.get("commentary")
    if ans_comm:
        if ans_comm in "error":
            times = str(session["times"])
            with open(args.output_after_commentary, "a", encoding="UTF-8") as f:
                f.write(userID + "\t" + times + "\t" +
                        session["label_num"] + "\terror\tNone\tNone\tNone\n"
                        )

            if Nof_prob == args.max_prob:
                url = "/end"
            else:
                Nof_prob_int = int(Nof_prob) + 1
                url = "/" + userID + "/one/" + str(Nof_prob_int)
                rewrite_start_position(args.start_position_file,
                                       userID, Nof_prob)
        else:
            url = "/" + userID + "/four/" + Nof_prob
    else:
        url = "/" + userID + "/three/" + Nof_prob
    return redirect(url)


@app.route("/<userID>/four/<Nof_prob>", methods=["GET"])
def contact_four(userID, Nof_prob):
    args = generate_args()
    session["miss"] = False

    prob_file = decide_problem_file(userID)
    prob_n = int(Nof_prob) - 1

    ques = Question(args.input_question_file)
    prob = Problem(prob_file)
    questions = ques.get_questions()
    problems = prob.get_problems()
    prob.parse_position(prob_n)
    positions = prob.get_positions()

    question = questions[3]
    num = Nof_prob + "問目"
    p_id = problems[prob_n][0]
    english = problems[prob_n][1]
    english = add_under(english, positions, args.position_target)
    commentary = problems[prob_n][2]
    return render_template("four.html",
                           question=question,
                           num=num,
                           p_id=p_id,
                           english=english,
                           commentary=commentary)


@app.route("/<userID>/four/<Nof_prob>", methods=["POST"])
def post_four(userID, Nof_prob):
    args = generate_args()
    judge = request.form.get("grammatically")
    if judge:
        if judge == "error":
            url = "/" + userID + "/five/" + Nof_prob
        else:
            times = str(session["times"])
            with open(args.output_after_commentary, "a", encoding="UTF-8") as f:
                f.write(userID + "\t" + times + "\t" + session["label_num"] +
                        "\tright\t" + str(judge) + "\tNone\tNone\n"
                        )
            rewrite_start_position(args.start_position_file, userID, Nof_prob)
            if Nof_prob == args.max_prob:
                url = "/end"
            else:
                Nof_prob_int = int(Nof_prob) + 1
                url = "/" + userID + "/one/" + str(Nof_prob_int)
    else:
        url = "/" + userID + "/four/" + Nof_prob
    return redirect(url)

@app.route("/<userID>/five/<Nof_prob>", methods=["GET"])
def contact_five(userID, Nof_prob):
    args = generate_args()
    prob_file = decide_problem_file(userID)
    prob_n = int(Nof_prob) - 1

    ques = Question(args.input_question_file)
    prob = Problem(prob_file)
    questions = ques.get_questions()
    problems = prob.get_problems()
    prob.parse_position(prob_n)
    positions = prob.get_positions()

    miss = session.get("miss", False)
    miss_words = session.get("miss_words", None)

    question = questions[4]
    num = Nof_prob + "問目"
    p_id = problems[prob_n][0]
    english = problems[prob_n][1]
    english = add_under(english, positions, args.position_target)
    commentary = problems[prob_n][2]
    return render_template("five.html",
                           question=question,
                           num=num,
                           p_id=p_id,
                           english=english,
                           commentary=commentary,
                           miss=miss,
                           miss_words=miss_words)


@app.route("/<userID>/five/<Nof_prob>", methods=["POST"])
def post_five(userID, Nof_prob):
    session["miss"] = False
    args = generate_args()
    answer = request.form.get("answer")
    answer_extra = request.form.get("answer_extra")
    if answer:
        session["miss"], session["miss_words"] = check_word(answer)
        if session["miss"] is True:
            url = "/" + userID + "/five/" + Nof_prob
            return redirect(url)
    times = str(session["times"])
    with open(args.output_after_commentary, "a", encoding="UTF-8") as f:
        f.write(userID + "\t" + times + "\t" + session["label_num"] +
                "\tright\terror\t" + str(answer) +
                "\t" + str(answer_extra) + "\n"
                )
    rewrite_start_position(args.start_position_file, userID, Nof_prob)
    if Nof_prob == args.max_prob:
        url = "/end"
    else:
        Nof_prob_int = int(Nof_prob) + 1
        url = "/" + userID + "/one/" + str(Nof_prob_int)
    return redirect(url)


@app.route("/end")
def end():
    return render_template("thanks.html")


if __name__ == "__main__":
    app.run(debug=True, port="5000")
    # host="0.0.0.0" -> Can access outside.
