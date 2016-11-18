class Date:
    def __init__(self, string):
        """ string example:
        "2016-08-18T18:09:43"
        """
        date = string.split('T')[0].split('-')
        clock = string.split('T')[1].split(':')

        self.year = int(date[0])
        self.month = int(date[1])
        self.day = int(date[2])
        self.hour = int(clock[0])
        self.minute = int(clock[1])
        self.sec = int(clock[2])

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
        if self.minute >= 60:
            self.minute -= 60
            self.hour += 1
            assert self.hour < 24

        return self

if __name__ == "__main__":
    print("Tests de Date")


    date1 = Date("2015-06-07T10:51:37")
    date2 = Date("2016-06-07T10:51:37")
    date3 = Date("2016-06-07T10:60:67")
    date4 = Date("2015-07-10T10:51:37")
    date5 = Date("2015-07-10T10:40:37")
    date6 = Date("2015-06-07T10:51:37").sum_minutes(4)

    assert date1.compare_to(date2) < 0
    assert date2.compare_to(date3) < 0
    assert date3.compare_to(date2) > 0
    assert date4.compare_to(date5) > 0
    assert date1.compare_to(date1) == date2.compare_to(date2)
    assert date5.compare_to(date4) < 0
    assert date1.compare_to(date6) < 0
    print("Passed all")
    print("Example test")
    event_time = Date("2016-06-07T10:51:37")
    limit_date = Date("2016-06-07T10:51:37").sum_minutes(4) # "2016-06-07T10:55:37"
    tweet_date = Date("2016-06-07T10:57:53")
    assert tweet_date.compare_to(Date("2016-06-07T10:55:37")) == tweet_date.compare_to(limit_date)
    assert tweet_date.compare_to(limit_date) > 0
    print("Passed example test")
