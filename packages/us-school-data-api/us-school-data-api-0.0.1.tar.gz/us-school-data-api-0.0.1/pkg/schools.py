from utils import Url, getPaginatedResults

def url():
    return Url().topic('schools')

class CCD:
    @staticmethod
    def url():
        return url().source('ccd')

    @staticmethod
    def directory(year, filters={}):
        if not year:
            return False
        url = CCD.url().endpoint('directory').year(year).filters(filters)
        return getPaginatedResults(url)

    @staticmethod
    def enrollment(year, grade, disaggregations=[], filters={}):
        if not year or not grade:
            return False
        url = CCD.url().endpoint('enrollment').year(year).grade(grade).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)

class CRDC:
    @staticmethod
    def url():
        return url().source('crdc')

    @staticmethod
    def directory(year, filters={}):
        url = CRDC.url().endpoint('directory').year(year).filters(filters)
        return getPaginatedResults(url)
    
    @staticmethod
    def enrollment(year, disaggregations=['race', 'sex'], filters={}):
        if len(disaggregations) < 2:
            return False
        url = CRDC.url().endpoint('enrollment').year(year).disaggregations(disaggregations).filters(filters)
        print(url)
        return getPaginatedResults(url)

    @staticmethod
    def discipline(year, disaggregations=['race', 'sex'], filters={}):
        if len(disaggregations) < 2:
            return false
        url = CRDC.url().endpoint('discipline').year(year).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)
    
    @staticmethod
    def harassment_or_bullying_allegations(year, filters={}):
        url = CRDC.url().endpoint('harassment-or-bullying').year(year).endpoint('allegations').filters(filters)
        return getPaginatedResults(url)
    
    @staticmethod
    def harassment_or_bullying(year, disaggregations=['race', 'sex'], filters={}):
        if len(disaggregations) < 2:
            return False
        url = CRDC.url().endpoint('harassment-or-bullying').year(year).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)

    @staticmethod
    def chronic_absenteeism(year, disaggregations=[], filters={}):
        url = CRDC.url().endpoint('chronic-absenteeism').year(year).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)

    @staticmethod
    def ap_ib_enrollment(year, disaggregations=['race', 'sex'], filters={}):
        if len(disaggregations) < 2:
            return false
        url = CRDC.url().endpoint('ap_ib_enrollment').year(year).disaggregations(disaggregations).filters(filters)

    @staticmethod
    def restraint_and_seclusion_instances(year, filters={}):
        url = CRDC.url().endpoint('restraint-and-seclusion').year(year).endpoint('instances').filters(filters)
        return getPaginatedResults(url)

    @staticmethod
    def restraint_and_seclusion(year, disaggregations=[], filters={}):
        url = CRDC.url().endpoint('restraint-and-seclusion').year(year).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)

    @staticmethod
    def ap_exams(year, disaggregations=['race', 'sex'], filters={}):
        if len(disaggregations) < 2:
            return False
        url = CRDC.url().endpoint('ap-exams').year(year).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)
    
    @staticmethod
    def sat_act_participation(year, disaggregations=['race', 'sex'], filters={}):
        if len(disaggregations) < 2:
            return False
        url = CRDC.url().endpoint('sat-act-participation').year(year).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)

class EDFacts:
    @staticmethod
    def url():
        return url().source('edfacts')

    @staticmethod
    def state_assessments(year, grade, disaggregations=[], filters={}):
        url = EDFacts.url().endpoint('assessments').year(year).grade(grade).disaggregations(disaggregations).filters(filters)
        return getPaginatedResults(url)

class NHGIS:
    @staticmethod
    def url():
        return url().source('nhgis')

    @staticmethod
    def geographic_variables(census_year, year=2016, filters={}):
        file = 'census-' + census_year
        url = NHGIS.url().endpoint(file).year(year).filters(filters)
        return getPaginatedResults(url)