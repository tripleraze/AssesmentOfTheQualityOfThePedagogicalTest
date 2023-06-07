from flask import Flask, render_template, request, redirect, url_for
import TestAssesment
import os


#TestResults = TestAssesment.pd.read_csv('TestResults.csv')

if os.path.exists('D:/AssesmentOfTheQualityOfThePedagogicalTest/TestResults.csv'):
    os.remove('D:/AssesmentOfTheQualityOfThePedagogicalTest/TestResults.csv')

    
UPLOAD_FOLDER = 'D:/AssesmentOfTheQualityOfThePedagogicalTest'
ALLOWED_EXTENSIONS = ['csv']


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def AllowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST', "GET"])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and AllowedFile(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'TestResults.csv'))
            return redirect('TestAssesment')
        else: return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def MainPage():
        return render_template('index.html')


@app.route('/TestAssesment', methods=['GET'])
def TestAssesmentPage():
    if os.path.exists('D:/AssesmentOfTheQualityOfThePedagogicalTest/TestResults.csv'):
        TestResults = TestAssesment.pd.read_csv('TestResults.csv')
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
        AVG = TestAssesment.AverageResultPerCategory(TestAssesment.DifficultyIndexOfQuestion(TestResults),
                                                 len(TestAssesment.DifficultyIndexOfQuestion(TestResults).index))
        AVGDataFrame = TestAssesment.ConvertToDataFrame(AVG)
        Count4 = len(AVGDataFrame.index)
        TestAssesment.CreateDiagram(AVG, NumberOfQuestions)
        return render_template("TestAssesment.html", NumberOfQuestions=NumberOfQuestions,
                           DifficultyIndexes=DifficultyIndexes,
                           Count=Count, AverageResult=AverageResult,
                           CountOfQuestions=CountOfQuestions, Count1=Count1,
                           HardQuestions=HardQuestions, Count2=Count2,
                           EazyQuestions=EazyQuestions, Count3=Count3,
                           NumberOfAttempts=NumberOfAttempts, AVGDataFrame=AVGDataFrame,
                           Count4=Count4)
    else: return redirect('/')


if __name__ == "__main__":
    app.run()