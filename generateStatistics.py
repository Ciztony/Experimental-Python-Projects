from sys import exit
from statistics import mean, median
import sigfig

class Statistics:
    def eradicateAnomalies(self, data, bounds=[], anomalousStrings=[]):
        '''
        Eradicate data anomalies within a specified inclusive range.

        @param data - list of numbers
        @param bounds - optional: list of bounds if numerical
        @param anomalousStrings - optional: list of anomalousStrings
        @return list of values without specified anomalies
        '''
        try:
            data = [element for element in data if element not in anomalousStrings]

            if bounds:
                
                if all(not isinstance(element,(int,float)) for element in data):
                    print("Bounds not possible. All values in the list are strings")
                    return data


            return data

        except Exception as e:
            exit(f"The error: {e} occurred.")

    def __mode(self, data):
        count = {}
        for element in data:
            count[element] = count.get(element, 0) + 1

        maxCount = max(count.values(), default=0)

        if maxCount == 1:
            return None

        modes = [k for k, v in count.items() if v == maxCount]
        return modes[0] if len(modes) == 1 else f"Multiple modes: {modes}"
    
    def __roundOff(self,result,sf,dp,callback):
        if isinstance(result,(int,float)):
            if sf:
                result = sigfig.round(result, sigfigs=sf)
            elif dp is not None:
                result = round(result, dp)
        else:
            print(f"Unable to round a non-numerical {callback}. Proceed to print output.")

        return result
        

        

    def calculateStatistic(self, data, callback, sf=None, dp=None):
        '''
        Calculate the requested statistic (mean, median, mode).

        @param data - list of numbers
        @param callback - name of the statistic
        @param sf - optional: significant figures
        @param dp - optional: decimal places
        @return string describing the statistic
        '''
        callbacks = {
            "mean": mean,
            "median": median,
            "mode": self.__mode
        }

        callback = callback.strip().lower()

        if callback not in callbacks:
            exit(f"The statistic '{callback}' is invalid. Please choose from: {', '.join(callbacks)}")

        if sf and dp:
            exit("Cannot use both significant figures (sf) and decimal places (dp) together.")

        if not data:
            return f"The data provided is empty. The {callback} is undefined."

        try:
            result = callbacks[callback](data)

            if result != None:
                result = self.__roundOff(result,sf,dp,callback)
            else:
                result = "There is no mode. Every value only occurs once"

            return f"{callback.capitalize()}: {result}"
        except Exception as e:
            exit(f"The error: {e} occurred.")

