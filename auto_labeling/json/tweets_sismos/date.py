class Date:
    def __init__(self, string):
        """ string example:
        "2016-08-18T18:09:43"
        """
        date = string.split('T')[0].split('-')
        clock = string.split('T')[1].split(':')

        self.year = date[0]
        self.mon = date[1]
        self.day = date[2]
        self.hour = clock[0]
        self.minute = clock[1]
        self.sec = clock[2]

    def compare_to(self, other_date):
        ''' Devuelve 1 si esta instancia es mas vieja que la otra.
        0 si son iguales, y -1 si es mas joven
        '''

        if self.year > other_date.year:
            return 1
        elif self.year < other_date.year:
            return -1
        else:
            if self.month > other_date.month:
                return 1
            elif self.month < other_date.month:
                return -1
            else:
                if self.day > other_date.day:
                    return 1
                elif self.day < other_date.day:
                    return -1
                else:
                    if self.hour > other_date.hour:
                        return 1
                    elif self.hour < other_date.hour:
                        return -1
                    else:
                        if self.minute > other_date.minute:
                            return 1
                        elif self.minute < other_date.minute:
                            return -1
                        else:
                            if self.sec > other_date.sec:
                                return 1
                            elif self.sec < other_date.sec:
                                return -1
                            else:
                                return 0

    def sum_minutes(self, minutes):
        assert minutes < 60
        self.minute += minutes
        if not self.minute >= 60:
            self.minute -= 60
            self.hour += 1
            assert self.hour < 24

        return self

