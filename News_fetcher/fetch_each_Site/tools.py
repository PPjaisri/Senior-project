import re
from dateutil.parser import parse

class tools(object):

    def return_month(month_str):
        thai_abb_month = [
            'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.',
        ]

        thai_full_month = [
            'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'คุลาคม', 'พฤศจิกายน', 'ธันวาคม',
        ]

        eng_month = [
            'january', 'febuary', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'
        ]

        index = 0
        ans = False

        if len(month_str) < 3:
            return str(-1)

        for i in range(12):
            if re.search(month_str.lower(), thai_abb_month[i]):
                index = i
                ans = True
                break
            elif re.search(month_str.lower(), thai_full_month[i]):
                index = i
                ans = True
                break
            elif re.search(month_str.lower(), eng_month[i]):
                index = i
                ans = True
                break

        if ans:
            return str(index + 1)
        else:
            return str(-1)

    def time_format(time_str):
        return parse(time_str).strftime('%d/%m/%Y')
