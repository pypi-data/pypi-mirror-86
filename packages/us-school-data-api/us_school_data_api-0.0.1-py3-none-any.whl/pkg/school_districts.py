from utils import Url, getPaginatedResults

def url():
    return Url().topic('school-districts')

class CCD:
    @staticmethod
    def url():
        return url().source('ccd')

    @staticmethod
    def directory(year, filters={}):
        url = CCD.url().endpoint('directory').year(year).filters(filters)
        return getPaginatedResults(url)

    @staticmethod
    def enrollment(year, grade, disaggregations=[], filters={}):
        url = CCD.url().endpoint('enrollment').year(year).grade(grade).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)

    @staticmethod
    def finance(year, filters={}):
        url = CCD.url().endpoint('finance').year(year).filters(filters)
        return getPaginatedResults(url)

class SAIPE:
    @staticmethod
    def url():
        return url().source('saipe')

    @staticmethod
    def poverty_estimates(year, filters={}):
        url = SAIPE.url().year(year).filters(filters)
        return getPaginatedResults(url)

class EDFacts: 
    @staticmethod
    def url():
        return url().source('edfacts')

    @staticmethod
    def state_assessments(year, grade, disaggregations=[], filters={}):
        url = EDFacts.url().endpoint('assessments').year(year).grade(grade).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)