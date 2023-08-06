from utils import Url, getPaginatedResults

def url():
    return Url().topic('college-university')

class IPEDS:
    @staticmethod
    def url():
        return url().source('ipeds')

class Scorecard:
    @staticmethod
    def url():
        return url().source('scorecard')

class NHGIS:
    @staticmethod
    def url():
        return url().source('nhgis')

class FSA:
    @staticmethod
    def url():
        return url().source('fsa')