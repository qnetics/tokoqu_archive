from hashlib import sha256


def password_hashing(plaintext) -> str :

    return sha256(plaintext.encode("utf8")).hexdigest()



# accurate hour and day for expired token authentication
def time_processing(now_time, expired_time, option) -> int : 

    # [ hour ]
    if option == "hour" :

        if now_time[0] == "0" :

            if int(now_time[1]) >= expired_time : 

                # expired every 2 hours
                return int(now_time[1]) + 2 

            else :

                # expired every 2 hours
                return int(now_time[1]) 

        else :

            if int(now_time) >= expired_time :

                if int(now_time) >= 23 :
                
                    # expired every 2 hours
                    return (int(now_time) - 23) + 2

                else :

                    return int(now_time) + 2

            else :

                return int(now_time)


    # [ days ]
    else :

        if now_time[0] == "0" :

            if int(now_time[1]) >= expired_time : 

                # expired every 1 day
                return int(now_time[1]) + 1 

            else :

                # expired every 1 day
                return int(now_time[1]) 

        else :

            if int(now_time) >= expired_time :

                if int(now_time) >= 30 :
                
                    # expired every 1 day
                    return (int(now_time) - 30) + 1

                else :

                    return int(now_time) + 1

            else :

                return int(now_time)

