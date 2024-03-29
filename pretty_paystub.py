from statistics import mean
from tkinter import filedialog
import tkinter
import PyPDF2
import os
import re
import sys


def search_file_path():
    """
    Opens a file dialog window that asks the user to pick the PDF file they'd like to process
    :return: a string of the direct file path
    """
    while True:
        # set up tkinter object
        root = tkinter.Tk()
        root.withdraw() # used to hide the tkinter window

        # bring up the dialog window
        curr_dir = os.getcwd()
        pdf_path = filedialog.askopenfilename(parent=root, initialdir=curr_dir, title='Please Select Pay Stub PDF')

        # get file name and extension and check if the file is a PDF, but quit the application if user clicks cancel
        try:
            pdf_name = os.path.split(pdf_path)[1]
            pdf_extension = os.path.splitext(pdf_path)[1]
        except TypeError:
            print('Dialog Window Cancelled: Quitting Application.')
            sys.exit()
        if len(pdf_path) > 0 and pdf_extension == '.pdf':
            print(f'Processing {pdf_name}')
            break
        else:
            print("File selected isn't a PDF or you didn't select a file")
    return pdf_path


def get_hours_grosspay(page):
    """
    Parses page and retrieves the amount of hours the user has worked and their gross pay for the pay period
    :param page: page number to parse
    :return: a tuple (hours, grosspay)
    """
    # find the hours worked and gross pay of pay period, and year to date pay
    gross_reg = re.compile(r'(?:Gross)(\d{2,3}.\d{2})(\d{0,4}.\d{2})')
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
    Parses page and retrieves the pay period dates ex. '06/29/2019 - 7/12/2019'
    :param page: page number to parse
    :return: a string of the pay period dates
    """
    # find the period start date
    period_start_reg = re.compile(r'(?:Period Start:\s)(\d{2}/\d{2}/\d{4})')
    period_start_mo = period_start_reg.findall(page)
    try:
        period_start = period_start_mo[0]
    except IndexError:
        period_start = 'No Start Date Listed'

    # find the period end date
    period_end_reg = re.compile(r'(?:Period End:\s)(\d{2}/\d{2}/\d{4})')
    period_end_mo = period_end_reg.findall(page)
    try:
        period_end = period_end_mo[0]
    except IndexError:
        period_end = 'No End Date Listed'

    # return pay period dates
    pay_period_dates = f'{period_start}-{period_end}'
    return pay_period_dates


def print_sauce(pay_period_dates, hours, grosspay, netpay):
    """
    Prints out pay period dates, gross, hourly, and net pay
    :param pay_period_dates: the dates of the pay period
    :param hours: hours worked
    :param grosspay: self
    :param netpay: self
    :return:
    """
    hourly_pay = float(grosspay) / float(hours)
    print('-' * len(pay_period_dates))
    print(pay_period_dates)
    print(f'Hours: {hours}')
    print(f'Gross Pay: ${grosspay}')
    print(f'Hourly Pay: ${hourly_pay:.2f}/hour')
    print(f'Net Pay: ${netpay}')


def print_average_sauce(average_grosspay, average_netpay, average_hours, average_hourly, num_pages):
    """
    Prints out the gross, net, hourly pay and average hours worked
    :param average_grosspay: self
    :param average_netpay: self
    :param average_hours: self
    :param average_hourly: self
    :return: None
    """
    # print out YTD averages
    print('*' * 50)
    print(f'Average of All {round(num_pages / 2)} Pay Stubs Processed')
    print('-' * 50)
    print(f'Average Hours Worked: {average_hours:.2f}')
    print(f'Average Gross Pay: ${average_grosspay:.2f}')
    print(f'Average Hourly Pay: ${average_hourly:.2f}')
    print(f'Average Net Pay: ${average_netpay:.2f}')
    print('*' * 50)


def are_we_printing():
    """
    Asks the user if they would like to pretty print each individual pay stub
    :return: a 0 or a 1 depending on the users answer (0 == False, 1 == True)
    """
    do_you_wanna = input('Would you like to pretty print each pay stub? [y/n]\n> ')
    if do_you_wanna.lower() == 'y' or do_you_wanna.lower() == 'yes':
        print_the_sauce = True
        return print_the_sauce
    else:
        print_the_sauce = False
        print('Only printing out the averages!')
        return print_the_sauce


if __name__ == '__main__':
    # set up PyPDF2 object and get PDF file path
    pdf_file_path = search_file_path()
    pdf_file = open(pdf_file_path, 'rb')
    reader = PyPDF2.PdfFileReader(pdf_file, strict=False)

    # get number of pages in PDF
    num_pages = reader.numPages

    # collection of lists for YTD
    grosspay_list = []
    hour_list = []
    netpay_list = []

    # ask the user if they'd like to print out a pretty print pay stub for each pay stub
    do_you_wanna = are_we_printing()

    for page in range(num_pages):
        # set up page number & get text from PDF page number
        page_num = reader.getPage(page)
        page_text = page_num.extractText()

        # check if page is a picture of a pay stub and skip this page if it is
        paystub_reg = re.compile(r'For Record Purposes Only')
        paystub_mo = paystub_reg.findall(page_text)
        if paystub_mo:
            continue

        # get pay period dates
        pay_period_dates = pay_period(page_text)

        # get hours and gross pay
        hour_grosspay = get_hours_grosspay(page_text)
        hours, grosspay = hour_grosspay[0], hour_grosspay[1]
        grosspay_list.append(float(grosspay))
        hour_list.append(float(hours))

        # get net pay
        netpay = get_netpay(page_text)
        netpay_list.append(float(netpay))

        # print hours, gross pay and net pay
        if do_you_wanna:
            print_sauce(pay_period_dates, hours, grosspay, netpay)

    # get averages for gross, net, and hourly pay
    average_grosspay = mean(grosspay_list)
    average_netpay = mean(netpay_list)
    average_hours = mean(hour_list)
    average_hourly = mean([pay/hours for pay, hours in zip(grosspay_list, hour_list)])

    print_average_sauce(average_grosspay, average_netpay, average_hours,
                        average_hourly, num_pages)

    pdf_file.close()
# that's all folks
