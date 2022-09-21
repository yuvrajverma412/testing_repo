from abc import ABC, abstractmethod


class RawDataProcessor(ABC):
    pass




class RawDataProcessorExpression(RawDataProcessor):
    
    @abstractmethod
    def processExpressionData(self):
        pass





class RawDataProcessorMutation(RawDataProcessor):

    @abstractmethod
    def processMutationData(self):
        pass





class RawDataProcessorClinical(RawDataProcessor):

    @abstractmethod
    def processClinicalData(self):
        pass




class RawDataProcessorEMC(RawDataProcessorExpression, RawDataProcessorMutation, RawDataProcessorClinical):
    pass



class RawDataProcessorEC(RawDataProcessorExpression, RawDataProcessorClinical):
    pass



class RawDataProcessorMC(RawDataProcessorMutation, RawDataProcessorClinical):
    pass