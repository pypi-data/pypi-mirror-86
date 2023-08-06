from DatasetGeneratorAI.App.src.label import Label

class labelService:
    def __init__(self):
        self.labels = []

        self.labels.append(Label('cat', 'Data/manual/train/cat', 'Data/automatic/train/cat', 12500))
        self.labels.append(Label('dog', 'Data/manual/train/dog', 'Data/automatic/train/dog', 12500))
    
    def read(self, labelName):
        if(labelName == ''):
            return self.labels

        iterator = filter(lambda label: label.labelName == labelName, self.labels)
        return list(iterator)[0]