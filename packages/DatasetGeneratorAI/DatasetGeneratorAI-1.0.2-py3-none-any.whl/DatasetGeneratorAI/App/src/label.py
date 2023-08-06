class Label:
    def __init__(self, labelName, automaticFolder, quantity, manualFolder = ''):
        self.labelName = labelName
        self.manualFolder = manualFolder
        self.automaticFolder = automaticFolder
        self.quantity = quantity