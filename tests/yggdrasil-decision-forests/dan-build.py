from dan.cxx import Executable

class YdfLearn(Executable):
    name = 'ydf-learn'
    dependencies = [
        'ydf-learner',
    ]
    sources = [
        'learn.cpp'
    ]

class YdfPredict(Executable):
    name = 'ydf-predict'
    dependencies = [
        'ydf-model',
    ]
    sources = [
        'predict.cpp'
    ]
