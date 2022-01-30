import string
import random

class generate_id :

    def id_generate( self ):

        ascii_digits    = string.ascii_letters + string.digits
        generate_result = "".join( [random.choice(ascii_digits) for _ in range(32)] )

        return generate_result