import string
import random
 
class generate_queue :

    def queue_generate( self ):

        ascii_digits = string.ascii_letters + string.digits
        generate_result = "".join( [random.choice(ascii_digits) for i in range(16)] )

        stripe_generate_result = ""

        for stripe_generate in range( len(generate_result) ):

            if ((stripe_generate == 4)|(stripe_generate == 8)|(stripe_generate == 12)) :

                stripe_generate_result += "-"
                stripe_generate_result += generate_result[stripe_generate]

            else :

                stripe_generate_result += generate_result[stripe_generate]

        return stripe_generate_result