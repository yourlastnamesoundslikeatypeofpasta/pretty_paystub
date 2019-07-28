import PyPDF2
import os
import re


def get_hours_grosspay(page):
    """
    Parses page and retrieves the amount of hours the user has worked and their gross pay for the pay period
    :param page: page number to parse
    :return: a tuple (hours, grosspay)
    """
    # find the hours worked and gross pay of pay period, and year to date pay
    gross_reg = re.compile(r'(?:Gross)(\d{2}.\d{2})(\d{0,4}.\d{2})')
    gross_mo = gross_reg.findall(page)
    # gross_mo will be one string containing hours, gross pay and YTD pay
    gross_mo = gross_mo[0] # ex of string: 71.131619.1321822.44
    hours, grosspay = gross_mo[0], gross_mo[1]
    return (hours, grosspay)


def get_netpay(page):
    """
    Parses page and retrieves the users netpay for the pay period
    :param page: page number to parse
    :return: an integer that equals the users netpay
    """
    # find net pay
    netpay_reg = re.compile(r'(?:Net Pay)(\d{2,4}.\d{2})')
    netpay_mo = netpay_reg.findall(page)

    netpay = netpay_mo[0]
    return netpay


def pay_period(page):
    """
    Parges page and retrieves the pay period dates ex. '06/29/2019 - 7/12/2019'
    :param page: page number to parse
    :return: a string of the pay period dates
    """
    # find the period start date
    period_start_reg = re.compile(r'(?:Period Start:\s)(\d{2}/\d{2}/\d{4})')
    period_start_mo = period_start_reg.findall(page)
    period_start = period_start_mo[0]

    # find the period end date
    period_end_reg = re.compile(r'(?:Period End:\s)(\d{2}/\d{2}/\d{4})')
    period_end_mo = period_end_reg.findall(page)
    period_end = period_end_mo[0]

    # return pay period dates
    pay_period_dates = f'{period_start}-{period_end}'
    return pay_period_dates


if __name__ == '__main__':
    # set up PyPDF2 object
    os.chdir('pdf\\')
    pdfFile = open('paystubs2019.pdf', 'rb')
    reader = PyPDF2.PdfFileReader(pdfFile, strict=False)

    # get number of pages in PDF
    num_pages = reader.numPages

    for page in range(num_pages):
        if page % 2 != 0:
            continue
        # set up page number
        page_num = reader.getPage(page)
        page_text = page_num.extractText()

        # get pay period dates
        pay_period_dates = pay_period(page_text)

        # get hours and gross pay
        hour_grosspay = get_hours_grosspay(page_text)
        hours, grosspay = hour_grosspay[0], hour_grosspay[1]

        # get net pay
        netpay = get_netpay(page_text)

        # print hours, gross pay and net pay
        print('-' * 22)
        print(pay_period_dates)
        print(f'Hours: ${hours}')
        print(f'Gross Pay: ${grosspay}')
        print(f'Net Pay: ${netpay}')

    pdfFile.close()
# that's all folks
