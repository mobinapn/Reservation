import re

irmci_pattern = r'(^(091|\+9891|009891|91|9891)\d{8}$)|(^(099|\+9899|009899|99|9899)[0-4]\d{7}$)'
taliya_pattern = r'^(0932|\+98932|0098932|932|98932)\d{7}$'
mtnirancell_pattern = r'(^(093|\+9893|009893|93|9893|090|\+9890|009890|90|9890)[^1,4]\d{7}$)|(^(0941|\+98941|0098941|941|98941))\d{7}$'
rightel_pattern = r'^(092|\+9892|009892|92|9892)[0-2]\d{7}$'
mtce_pattern = r'^(09|\+989|00989|9|989)(31)\d{7}$'
telekish_pattern = r'^(09|\+989|00989|9|989)(34)\d{7}$'
aptel_pattern = r'^(09|\+989|00989|9|989)(991)[0,1,3]\d{5}$'
azartel_pattern = r'^(09|\+989|00989|9|989)(991)(4)\d{5}$'
samantel_pattern = r'^(0|\+98|0098|9|98)(9999)[6-9]\d{5}$'
lotustel_pattern = r'^(0|\+98|0098|9|98)(9990)\d{6}$'
shatel_pattern = r'^(0|\+98|0098|9|98)(9981)[0-5]\d{5}$'
ariantel_pattern = r'^(0|\+98|0098|9|98)(9998)\d{6}$'
anarestan_pattern = r'^(0|\+98|0098|9|98)(994)\d{7}$'

""" valid_tel_pattern_list = [irmci_pattern, taliya_pattern, mtnirancell_pattern, rightel_pattern, mtce_pattern, telekish_pattern, aptel_pattern, 
azartel_pattern, samantel_pattern, lotustel_pattern, shatel_pattern, ariantel_pattern, anarestan_pattern] """

valid_tel_pattern_dict = {'irmci' : irmci_pattern, 'taliya' : taliya_pattern, 'mtnirancell' : mtnirancell_pattern, 'rightel' : rightel_pattern, 
'mtce' : mtce_pattern, 'telekish' : telekish_pattern, 'aptel' : aptel_pattern, 'azartel' : azartel_pattern, 
'samantel' : samantel_pattern, 'lotustel' : lotustel_pattern, 'shatel' : shatel_pattern, 'ariantel' : ariantel_pattern, 'anarestan' : anarestan_pattern}

operator = None

def is_valid(tel_number):
    """ 
    this function check if number is real and belong to iranian operators and return True or False
    for more information about number use anouther functions
    """
    global operator

    """ check if strip of input number has valid length """
    tel_number = tel_number.strip()
    if(len(tel_number) > 14 or len(tel_number) < 10):
        return False

    """ check if all character of input number are digit """
    if(not tel_number.isdigit()):
        return False

    """ check if input number belong to known operators """
    for pattern in valid_tel_pattern_dict:
        if(re.search(valid_tel_pattern_dict[pattern], tel_number) != None):
            operator = pattern
            return True

    """ if no operator found return False """
    return False

def tel_operator(tel_number):
    """ 
    return the operator of input phone number, if number is not valid return 'None' 
    """
    tel_number = tel_number.strip()
    if (is_valid(tel_number)):
        return operator
    else:
        return None


def tel_information(tel_number):
    """ 
    check and return a dictionary that has element of validation and operator of number
    if number is not valid it return validation = 'False' and operator = 'None'
    """
    validation = is_valid(tel_number)
    operator = tel_operator(tel_number)
    info_dict = {'validation' : validation, 'operator' : operator}

    return (info_dict)
