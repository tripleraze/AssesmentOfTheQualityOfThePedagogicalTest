import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt


#TestResults = pd.read_csv('TestResults.csv')


def NumberOfQuestionsCalculate(TestResults):
    NumberOfQuestions = 0
    for column in TestResults:
        if column.find("Вопрос") != -1:
            NumberOfQuestions += 1
    return NumberOfQuestions


def AverageResult(TestResults):
    TestResults['Оценка/100,0'] =[x.replace(',', '.') for x in TestResults['Оценка/100,0']]
    average = TestResults['Оценка/100,0'].astype(float).sum()/len(TestResults.index)
    return round(average, 2)


def CountOfQuestions(TestResults):
    i = 1
    for column in TestResults:
        if column == f"Вопрос {i}":
            if i == 1:
                Count = (TestResults[column].value_counts())
                i += 1
            else:
                Count = Count._append(TestResults[column].value_counts())
                i += 1
    Count.to_excel('Questions.xlsx')
    Count = pd.read_excel('Questions.xlsx')
    Count.columns = ['Question', 'Count']
    return Count


def DifficultyIndexOfQuestion(TestResults):
    DifficultyIndexes = pd.DataFrame(columns=['NumberOfQuestion','Question','Count', 'CountSuccesfully', 'DifficultyIndex'])
    i = 1
    count = 0
    for column in TestResults:
        if column == f'Вопрос {i}':
            RightAnswers = 0
            Buffer = TestResults[column].unique()
            for q in Buffer:
                j = 0
                while j < len(TestResults.index):
                    if q == TestResults.iloc[j][f'Вопрос {i}'] and TestResults.iloc[j][f'Ответ {i}'] == TestResults.iloc[j][f'Правильный ответ: {i}']:
                        RightAnswers += 1
                    if q == TestResults.iloc[j][f'Вопрос {i}']:
                        count += 1
                    j += 1
                DifficultyIndex = round(100*(1-RightAnswers/count), 2)
                DifficultyIndexes.loc[len(DifficultyIndexes.index)] = [f'Вопрос {i}', q, count, RightAnswers, DifficultyIndex]
                RightAnswers -= RightAnswers
                j -= j
                count -= count
            i += 1
    return DifficultyIndexes


def FindHardQuestions(DifficultyIndexOfQuestion):
    i = 0
    HardQuestions = pd.DataFrame(columns=['Question'])
    while i < len(DifficultyIndexOfQuestion.index):
        if DifficultyIndexOfQuestion.iloc[i]['Count'] >= 5 and DifficultyIndexOfQuestion.iloc[i]['DifficultyIndex'] >= 80:
            HardQuestions.loc[len(HardQuestions.index)] = [DifficultyIndexOfQuestion.iloc[i]['Question']]
        i += 1
    return HardQuestions


def FindEazyQuestions(DifficultyIndexOfQuestion):
    i = 0
    EazyQuestions = pd.DataFrame(columns=['Question'])
    while i < len(DifficultyIndexOfQuestion.index):
        if DifficultyIndexOfQuestion.iloc[i]['Count'] >= 5 and DifficultyIndexOfQuestion.iloc[i]['DifficultyIndex'] <=10:
            EazyQuestions.loc[len(EazyQuestions.index)] = [DifficultyIndexOfQuestion.iloc[i]['Question']]
        i += 1
    return EazyQuestions


def AverageResultPerCategory(DifficultyIndexes, NumberOfAttempts):
    AverageResultsPerCategory = []
    buffer = 0
    count = 0
    j = 1
    for i in range(NumberOfAttempts):
        if DifficultyIndexes.iloc[i]['NumberOfQuestion'] == f"Вопрос {j}":
            buffer += DifficultyIndexes.iloc[i]['DifficultyIndex']
            count += 1
        else:
            AverageResultsPerCategory.append(round(buffer/count,2))
            j += 1
            count -= count
            buffer -= buffer
    AverageResultsPerCategory.append(round(buffer/count, 2))
    return AverageResultsPerCategory

def CreateDiagram(AverageResultsPerCategory, NumberOfQuestions):
    i = 1
    buffer = []
    while i <= NumberOfQuestions:
        buffer.append(f"Вопрос {i}")
        i += 1
    objects = tuple(buffer)
    y_pos = np.arange(len(objects))
    performance = AverageResultsPerCategory

    plt.figure(figsize=(7, 8.5))
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects, rotation=45)
    plt.ylabel('Индекс трудности')
    plt.xlabel('Категория вопроса')
    plt.title('График трудности вопросов по категориям')
    plt.savefig('static/img/diagram.png')


def ConvertToDataFrame(AVG):
    DataFrame = pd.DataFrame(columns=['Category', 'AVG'])
    for i in range(len(AVG)):
        DataFrame.loc[len(DataFrame.index)] = [f'Вопрос {i+1}', AVG[i]]
    return DataFrame



#print("Общее количество попыток выполнения теста: " + str(len(TestResults.index)))
#NumberOfQuestions = NumberOfQuestionsCalculate(TestResults)
#print ("Количество вопросов в тесте: " + str(NumberOfQuestions))
#print("Средний балл прохождения теста: " + str(AverageResult(TestResults)))
#print ("Количество раз, сколько встретился каждый вопрос в тесте: ")
#print(CountOfQuestions(TestResults))
#print(DifficultyIndexOfQuestion(TestResults))
#print("Сложные вопросы: ")
#print(FindHardQuestions(DifficultyIndexOfQuestion(TestResults)))
#print("Лёгкие вопросы: ")
#print(FindEazyQuestions(DifficultyIndexOfQuestion(TestResults)))
#AVG = AverageResultPerCategory(DifficultyIndexOfQuestion(TestResults), len(DifficultyIndexOfQuestion(TestResults).index))
#print(AVG)
#CreateDiagram(AVG, NumberOfQuestionsCalculate(TestResults))
#df = ConvertToDataFrame(AVG)
#print(df)