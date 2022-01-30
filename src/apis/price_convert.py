import locale

def rupiah_format(angka, with_prefix) -> str :

    desimal = 2

    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format("%.*f", (desimal, angka), True)

    if with_prefix:

        return "Rp. {}".format(rupiah)
        
    return rupiah



def rupiah_str_to_int(rupiah_format) -> int :

    decimal_sort = rupiah_format[0:len(rupiah_format)-3]

    int_format = ""

    for index_int_format in range( len(decimal_sort) ) :

        try :

            convert_int = int( decimal_sort[index_int_format] )
            int_format += str( convert_int )

        except ValueError :

            pass

    return int( int_format )