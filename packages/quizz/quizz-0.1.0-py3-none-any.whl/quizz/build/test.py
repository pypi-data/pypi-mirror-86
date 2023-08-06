from quizz import (
    Quiz,
    MultipleChoiceQuestion,
    Question,
    Next,
    Previous,
    Jump,
    Help,
    Scheme,
    Finish,
    Option,
    opcodes,
)


my_scheme = Scheme(
    commands=[Next, Previous, Jump, Help, Finish],
    choices=["domates", "yo", 1],
    display="vertical",
)


# print(my_scheme)
# my_scheme = EmptyScheme(commands=[Next, Previous, Jump, Help, Finish])


questions = [
    MultipleChoiceQuestion(
        "What is full form of ARPANET?",
        choices=[
            "Advanced Radioactive Projects Agency",
            "Advanced Research Projects Agency Network",
            "Advanced Research Practice Agency Network",
            "None of these",
        ],
        correct_answers=["d"],
    ),
    MultipleChoiceQuestion(
        "What is full form of USB ?",
        choices=[
            "Universal serial bus",
            "Ultra serial bus",
            "Uniform serial bus",
            "None of the above",
        ],
        correct_answers=["a"],
    ),
    MultipleChoiceQuestion(
        "What is full form of ROM?",
        choices=[
            "Read other memcache",
            "Read only memory",
            "Read other memory",
            "Read only memcache",
        ],
        correct_answers=["c"],
    ),
    Question("Final thoughts?", required=False),
]

my_quiz = Quiz(questions, scheme=my_scheme)

my_quiz.start()

score = sum([33.33333 for q in my_quiz.questions if q.has_correct_answer])
print(score)

for quest in my_quiz.questions:
    print(quest.answer)

# from quizz import (
#     Question,
#     ValidationError,
#     Option,
#     MultipleChoiceQuestion,
#     Quiz,
#     Scheme,
#     Command,
# )
#
# from quizz import (
#     Skip,
#     Quit,
#     Help,
#     Next,
#     Previous,
#     Finish,
#     Jump,
#     Answers,
# )
#
#
# class StupidCommand(Command):
#     expression = "hey"
#
#     def execute(self, question: Question, *args):
#         print(123)
#         print(question.required)
#
#
# cmdset = [
#     Skip,
#     Quit,
#     Help,
#     Next,
#     Previous,
#     Finish,
#     Jump,
#     Answers,
#     StupidCommand,
# ]
#
# a = Option(value="1", expression="Domates")
# b = Option(value="2", expression="Çilek")
# #
# q = Question(
#     "Best fruit?",
#     append_column=True,
#     options=[a, b],
#     commands=cmdset,
#     required=False,
# )
#
# q.ask()
# print(q.answer)
#
# q1 = Question(
#     "Best thingy??",
#     append_column=True,
#     options=[a, b],
#     commands=cmdset,
#     extra={"domates": 2}
#     # required=True,
# )
#
#
# q2 = MultipleChoiceQuestion(
#     "Bilgisayar ingilizcesi?",
#     choices=["Tree", "Shoe", "Computer", "Glass"],
#     style="letter",
#     append_column=True,
#     correct_answers=["a"],
#     # required=True,
#     commands=cmdset,
# )
#
#
# # myquiz = Quiz([q, q1, q2])
#
#
# # myquiz.start()
