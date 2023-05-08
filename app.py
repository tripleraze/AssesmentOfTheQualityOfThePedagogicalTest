from flask import Flask, render_template
import TestAssesment


TestResults = TestAssesment.pd.read_csv('TestResults.csv')


app = Flask(__name__)


@app.route('/TestAssesment', methods=['GET'])
def TestAssesmentPage():
    NumberOfQuestions = TestAssesment.NumberOfQuestionsCalculate(TestResults)
    NumberOfAttempts = len(TestResults.index)
    DifficultyIndexes = TestAssesment.DifficultyIndexOfQuestion(TestResults)
    Count = len(DifficultyIndexes.index)
    AverageResult = TestAssesment.AverageResult(TestResults)
    CountOfQuestions = TestAssesment.CountOfQuestions(TestResults)
    Count1 = len(CountOfQuestions.index)
    HardQuestions = TestAssesment.FindHardQuestions(DifficultyIndexes)
    Count2 = len(HardQuestions.index)
    EazyQuestions = TestAssesment.FindEazyQuestions(DifficultyIndexes)
    Count3 = len(EazyQuestions.index)
    return render_template("TestAssesment.html", NumberOfQuestions=NumberOfQuestions, DifficultyIndexes=DifficultyIndexes,
                           Count=Count, AverageResult=AverageResult,
                           CountOfQuestions=CountOfQuestions, Count1=Count1,
                           HardQuestions=HardQuestions, Count2=Count2,
                           EazyQuestions=EazyQuestions, Count3=Count3,
                           NumberOfAttempts=NumberOfAttempts)


if __name__ == "__main__":
    app.run()