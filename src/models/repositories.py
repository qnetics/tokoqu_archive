from random import randint
from datetime import datetime

from src.models.helpers import helpers

from src.apis.id import generate_id
from src.apis.queue import generate_queue
from src.apis.token import generate_token
from src.apis.security import time_processing

from src.apis.price_convert import (

    rupiah_format,
    rupiah_str_to_int

)



 
"""
        ============================== customer beaviours =============================

"""

class customer_repo(helpers, generate_id, generate_queue) :


    def __init__(self) -> None :

        super().__init__()

        self.__order_connection   = self.connection_orders()
        self.__product_connection = self.connection_products()
        self.__notification_connection = self.connection_admins_operators_and_auth(option = "notification")

        self.__order   = "order_collections"
        self.__product = "product_collections"
        self.__notification = "notification_collections"


    # show product
    def landing_products(self) -> dict :

        # landing products
        limit_products = 20
        product_datas  =  [ products for products in self.__product_connection[self.__product].find() ]


        # recommendation products

        recommendation_datas = [ 
        
            [
                product_datas[randint(0,len(product_datas)-1)] for _2 in range(3)
                
            ] for _1 in range(10)
        
        ]

        return {

            "products" : product_datas[0:limit_products],
            "recommendations" : recommendation_datas

        }


    def products(self)  -> list :

        # for all products

        return [ products for products in self.__product_connection[self.__product].find() ]



    def specific_and_order_form_product(self, route) -> dict :

        # single product

        single_product = self.__product_connection[self.__product].find_one({

            "route" : route

        })

        # recommendation products
        product_datas  =  [ products for products in self.__product_connection[self.__product].find() ]

        recommendation_datas = [ 
        
            [
                product_datas[randint(0,len(product_datas)-1)] for _2 in range(3)
                
            ] for _1 in range(10)
        
        ]

        return {

            "single" : single_product,
            "recommendations" : recommendation_datas

        }



    def purchace_queue_order(self, payload) -> dict :

        date = datetime.now().strftime("%H:%M:%S - %d/%b/%Y")

        # generate queue order
        while True :

            queue = self.queue_generate()

            if self.__order_connection[self.__order].find_one({ "queue" : queue }) == None :

                queue_code = queue

                break


            else :

                pass


        # generate id order
        while True :

            id = self.id_generate()

            if self.__order_connection[self.__order].find_one({ "id" : id }) == None :

                order_id = id

                break

            else :

                pass

        product = self.__product_connection[self.__product].find_one({ "id" : payload['id'] })

        self.__order_connection[self.__order].insert_one({

            "id"    : order_id,
            "queue" : queue_code,

            "product_detail" : {

                "product_id"       : product["id"],
                "product_name"     : product["name"],
                "product_image"    : product["product_images"][0],
                "product_quantity" : payload['quantity'],
                "product_desc"     : payload['desc'],
                "total_price"      : rupiah_format( int(payload['quantity']) * rupiah_str_to_int(product['price']), True)

            },

            "customer_detail" : {

                "name"    : payload["name"],
                "tel_num" : payload["tel_num"],
                "address" : {

                    "jl"     : payload["jl"],
                    "rt"     : payload["rt"],
                    "rw"     : payload["rw"],
                    "kel"    : payload["kel"],
                    "kec"    : payload["kec"],
                    "city"   : payload["city"],
                    "prov"   : payload["prov"],
                    "no"     : payload["no"],
                    "postal" : payload["postal"]

                }
            },

            "date" : date,

            "status" : "pesanan sedang di proses"
            
        })

        self.__notification_connection[self.__notification].insert_one({

            "id"            : order_id,
            "date"          : date,
            "name_costumer" : payload["name"],
            "name_product"  : product["name"],
            "quantity_product" : payload['quantity']

        })

        return {

            "queue" : queue_code,
            "price_value"  : rupiah_str_to_int(product['price']), 
            "content_name" : product['name']

        }



    def purchace_order(self, queue_code) -> dict :

        queue_data = self.__order_connection[self.__order].find_one({ "queue" : queue_code })

        if queue_data != None :

            order_data = self.__product_connection[self.__product].find_one({

                "id" : queue_data["product_detail"]["product_id"]

            })

            # total price
            total_price = int(queue_data["product_detail"]["product_quantity"]) * rupiah_str_to_int(order_data["price"])


            return {

                "product_data" : {

                    "name"  : order_data["name"],
                    "price" : order_data["price"],
                    "desc"  : order_data["desc"],
                    "product_images" : order_data["product_images"],
                    "variant_images" : order_data["variant_images"]

                },

                "customer_data" : {

                    "name" : queue_data["customer_detail"]["name"],
                    "tel_num" : queue_data["customer_detail"]["tel_num"],
                    "jl" : queue_data["customer_detail"]["address"]["jl"],
                    "rt" : queue_data["customer_detail"]["address"]["rt"],
                    "rw" : queue_data["customer_detail"]["address"]["rw"],
                    "kel" : queue_data["customer_detail"]["address"]["kel"],
                    "kec" : queue_data["customer_detail"]["address"]["kec"],
                    "city" : queue_data["customer_detail"]["address"]["city"],
                    "prov" : queue_data["customer_detail"]["address"]["prov"],
                    "no"   : queue_data["customer_detail"]["address"]["no"],
                    "postal" : queue_data["customer_detail"]["address"]["postal"],
                    "status" : queue_data["status"]

                },

                "order_data" : {

                    "queue_code" : queue_data["queue"],
                    "quantity" : queue_data["product_detail"]["product_quantity"],
                    "desc"     : queue_data["product_detail"]["product_desc"],
                    "total"    : rupiah_format(total_price, True)

                },

                "status" : "found"

            }


        else :

            return {

                "status" : "not found"

            }








"""
        ============================== admin routes =============================

"""

class admin_and_operators_repo(helpers, generate_token, generate_id) :

    def __init__(self) -> None:

        super().__init__()

        self.__auth_connection    = self.connection_admins_operators_and_auth(option = "auth")
        self.__admin_connection   = self.connection_admins_operators_and_auth(option = "officer")
        self.__notification_connection = self.connection_admins_operators_and_auth(option = "notification")

        self.__product_connection = self.connection_products()
        self.__order_connection   = self.connection_orders()

        self.__token = "token_collections"
        self.__admin = "officer_collections"

        self.__order   = "order_collections"
        self.__product = "product_collections"

        self.__notification = "notification_collections"


    # repo dashboard

    def repo_dashboard(self, token) -> dict :

        token_checking = self.__auth_connection[self.__token].find_one({"latest_token" : token})

        if token_checking != None :

            user_checking  = self.__admin_connection[self.__admin].find_one({"id" : token_checking["user_id"]})

            if user_checking != None :

                return {

                    "response" : "found",
                    "status"   : user_checking["status"],
                    "nickname" : user_checking["details"]["nickname"],
                    "fullname" : user_checking["details"]["fullname"]

                }

            else :

                return {

                    "response" : "not found"

                }

        else :

            return {

                "response" : "not found"

            }
            


    # repo form add product

    def repo_form_add_product(self, data) :

        while True :

            generate = self.id_generate()

            if self.__product_connection[self.__product].find_one({"id" : generate}) == None :


                self.__product_connection[self.__product].insert_one(
                    {
                        "id"    : generate,
                        "route" : data["route"],
                        "name"  : data["name"],
                        "price" : data["price"],
                        "desc"  : data["desc"],
                        "product_images" : data["product_images"],
                        "variant_images" : data["variant_images"],
                    }
                )
            
                response = True

                break

        return response


    
    def repo_show_products(self) -> list :

        data_sorting  = []

        for index_sorting in [ products for products in self.__product_connection[self.__product].find() ] :

            data_sorting.append({

                "id"    : index_sorting["id"],
                "route" : index_sorting["route"],
                "name"  : index_sorting["name"],
                "price" : index_sorting["price"],
                "image" : index_sorting["product_images"][0]

            })

        return data_sorting


    def repo_single_product(self, product_id) -> dict :

        return self.__product_connection[self.__product].find_one({"id" : product_id})




    def repo_edit_product(self, product_id, new_payload) -> dict :

        oldest_product = self.__product_connection[self.__product].find_one({"id" : product_id})

        new_payload.update({

            "id" : product_id

        })

        self.__product_connection[self.__product].update_one(

                {"_id" : oldest_product["_id"]},

                { "$set" : new_payload },

                upsert = False


        )

        return self.__product_connection[self.__product].find_one({"id" : product_id})


    def repo_show_orders(self) -> dict :

        return [ show for show in self.__order_connection[self.__order].find() ]

    
    def repo_specific_order(self, order_id) :

        return self.__order_connection[self.__order].find_one({ "id" : order_id })


    def repo_update_order(self, order_id, payload) -> dict :

        find_order_by_id = self.__order_connection[self.__order].find_one({ "id" : order_id })

        product_data = self.__product_connection[self.__product].find_one({

            "id" : find_order_by_id["product_detail"]["product_id"]

        })

        if find_order_by_id != None :

            payload = {

                "id"    : order_id,
                "queue" : find_order_by_id["queue"],

                "product_detail" : {

                    "product_id"       : find_order_by_id["product_detail"]["product_id"],
                    "product_name"     : find_order_by_id["product_detail"]["product_name"],
                    "product_image"    : find_order_by_id["product_detail"]["product_image"],
                    "product_quantity" : payload['quantity'],
                    "product_desc"     : payload['desc'],
                    "total_price"      : rupiah_format( int(payload['quantity']) * rupiah_str_to_int(product_data['price']), True)

                },

                "customer_detail" : {

                    "name"    : payload["name"],
                    "tel_num" : payload["tel_num"],
                    "address" : {

                        "jl"     : payload["jl"],
                        "rt"     : payload["rt"],
                        "rw"     : payload["rw"],
                        "kel"    : payload["kel"],
                        "kec"    : payload["kec"],
                        "city"   : payload["city"],
                        "prov"   : payload["prov"],
                        "no"     : payload["no"],
                        "postal" : payload["postal"]

                    }
                },

                "status" : payload["status"]
                
            }

            self.__order_connection[self.__order].update_one(

                    {"_id" : find_order_by_id["_id"]},

                    { "$set" : payload },

                    upsert = False

            )

        else :

            pass



    def repo_delete_order(self, order_id) -> bool :

        self.__order_connection[self.__order].delete_one({ "id" : order_id })

        return True

    def repo_notification(self) -> dict :

        order_data = [ index_order for index_order in self.__notification_connection[self.__notification].find() ]

        # sorting order data 
        sorting_order_data = [ ]

        for index_newest in range( len(order_data)) :

            del order_data[len(order_data) - (index_newest + 1) ]["_id"]

            sorting_order_data.append(
                order_data[len(order_data) - (index_newest + 1) ]
            )

        return {

            "notif_length"  : len(order_data),
            "notifications" : sorting_order_data
        }





"""
        ============================== admin routes =============================

"""

class authentication_and_authorization_repo(helpers, generate_token) :

    def __init__(self) -> None:

        super().__init__()

        self.__auth_connection  = self.connection_admins_operators_and_auth(option = "auth")
        self.__admin_connection = self.connection_admins_operators_and_auth(option = "officer")

        self.__admin = "officer_collections"
        self.__token = "token_collections"


    # validate access token
    def validate_token(self, token) -> bool :

        token_checking = self.__auth_connection[self.__token].find_one({"latest_token" : token})

        if token_checking != None :

            user_checking = self.__admin_connection[self.__admin].find_one(

                {
                    "id" : token_checking["user_id"]
                }

            )

            if user_checking != None :

                return {

                    "response" : "found",
                    "status"   : user_checking["status"]

                }

        else :

            return {

                "response" : "not found"

            }




    def generate_token_expire(self, old_token) -> str :

        return 0




    #user login repo
    def login_user(self, payloads) -> dict :

        user_checking = self.__admin_connection[self.__admin].find_one(payloads)

        if user_checking != None :

            token_checking = self.__auth_connection[self.__token].find_one({"user_id" : user_checking["id"]})


            if token_checking == None :

                while True :

                    #generate token
                    generate = self.token_generate()

                    if self.__auth_connection[self.__token].find_one({"latest_token" : generate}) == None :

                        # time
                        hour = datetime.now().strftime("%H")
                        day  = datetime.now().strftime("%d")

                        request_payloads = {

                            "oldest_token" : "",
                            "latest_token" : generate,
                            "user_id"      : user_checking["id"],
                            "expired" : {
                                "hour" : int(hour[1])+1 if hour[0] == "0" else (int(hour)-23) if int(hour) >= 23 else int(hour) + 1,
                                "day"  : int(day[1]) if day[0] == "0" else (int(day)-30) if int(day) > 30 else int(day) + 1
                            }

                        }

                        self.__auth_connection[self.__token].insert_one(request_payloads)


                        token = generate

                        break
                
                return {
                    "token"  : token,
                    "status" : user_checking["status"]
                }

                    


            elif token_checking != None :

                while True :
                    
                    #generate token
                    generate = self.token_generate()

                    if self.__auth_connection[self.__token].find_one({"latest_token" : generate}) == None :

                        oldest_payloads = self.__auth_connection[self.__token].find_one({"user_id" : user_checking["id"]}) 

                        print(oldest_payloads)

                        latest_payloads = oldest_payloads

                        hour = datetime.now().strftime("%H")
                        day  = datetime.now().strftime("%d")
                            
                        latest_payloads.update(
                            {
                                "oldest_token" : oldest_payloads["latest_token"],
                                "latest_token" : generate,
                                "user_id" : oldest_payloads["user_id"],
                                "expired" : {
                                    'hour' : time_processing(hour, oldest_payloads["expired"]["hour"], "hour"),
                                    "day"  : time_processing(day, oldest_payloads["expired"]["day"], "day")
                                }
                            }
                        )

                        del oldest_payloads["_id"]

                        self.__auth_connection[self.__token].delete_one(

                            {
                                "user_id" : oldest_payloads["user_id"],
                                "latest_token" : oldest_payloads["oldest_token"]
                            }

                        )


                        self.__auth_connection[self.__token].update_one(

                            oldest_payloads,

                            { "$set" : latest_payloads },

                            upsert = True
                        )

                        token = generate

                        break

                return {
                    "token"  : token,
                    "status" : user_checking["status"]
                }

        else :

            return {
                "status" : "failed"
            }








"""
        ============================== admin routes =============================

"""

class integration_repo(helpers) :

    def __init__(self) -> None:

        self.__integration_connection = self.connection_admins_operators_and_auth(option = "integration")

        self.__integration = "integration_collections"

    def add_and_update_integration_fb_ads(self, id) -> dict :

        is_exist = self.__integration_connection[self.__integration].find_one(
            { "type" : "fb" }
        )

        if is_exist != None :

            new_payload = is_exist

            new_payload.update({"id" : id})

            self.__integration_connection[self.__integration].update_one(

                {"_id" : is_exist["_id"]},

                { "$set" : new_payload },

                upsert = False


            )

            return self.__integration_connection[self.__integration].find_one(

                { "type" : "fb" }

            )["id"]

        else :
            
            self.__integration_connection[self.__integration].insert_one(

                {
                    "type" : "fb",
                    "id"   : id
                }

            )

            return self.__integration_connection[self.__integration].find_one(

                { "type" : "fb" }

            )["id"]

    
    def show_id_integration_fb_ads(self) -> dict :

        return self.__integration_connection[self.__integration].find_one(

                { "type" : "fb" }

        )["id"]


    def integration_tiktok_ads(self, id) :

        return 0

    def integration_google_ads(self, id) :

        return 0



