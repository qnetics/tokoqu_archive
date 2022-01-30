import string
import random
 
class generate_token :

    def token_generate( self ):

        ascii_digits = string.ascii_letters + string.digits
        generate_result = "".join( [random.choice(ascii_digits) for i in range(64)] )

        return generate_result
