from pymongo import MongoClient

class helpers : 

    def connection_products(self) -> None :

        database  = "products"
        srv_url   = f"mongodb+srv://tokoqu-products:gasel237@tokoqu-products.nibu9.mongodb.net/{database}?retryWrites=true&w=majority"

        client = MongoClient(f"{srv_url}&ssl=true&ssl_cert_reqs=CERT_NONE")

        return client[database]

    def connection_orders(self) -> None :

        database  = "orders"
        srv_url   = f"mongodb+srv://tokoqu-orders:gasel237@tokoqu-orders.civ2d.mongodb.net/{database}?retryWrites=true&w=majority"

        client = MongoClient(f"{srv_url}&ssl=true&ssl_cert_reqs=CERT_NONE")

        return client[database]

    def connection_admins_operators_and_auth(self, option) -> None :

        options = [

            {
                "option"   : "officer",
                "database" : "db_admin",
                "srv_url"  : f"mongodb+srv://tokoqu:gasel237@cluster0.oqrql.mongodb.net/db_admin?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
            },

            {
                "option"   : "auth",
                "database" : "db_auth",
                "srv_url"  : f"mongodb+srv://tokoqu:gasel237@cluster0.oqrql.mongodb.net/db_auth?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
            },

            {
                "option"   : "integration",
                "database" : "db_integration",
                "srv_url"  : f"mongodb+srv://tokoqu:gasel237@cluster0.oqrql.mongodb.net/db_integration?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
            },

            {
                "option"   : "notification",
                "database" : "db_notification",
                "srv_url"  : f"mongodb+srv://tokoqu:gasel237@cluster0.oqrql.mongodb.net/db_notification?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
            }

        ]

        for index_option in options :

            if option == index_option["option"] :

                client = MongoClient(index_option["srv_url"])

                return client[index_option["database"]]

            else :

                pass


    def connection_costumers(self) -> None :

        database  = "costumers"
        srv_url   = f"mongodb+srv://tokoqu-customers:gasel237@tokoqu-customers.mx1on.mongodb.net/{database}?retryWrites=true&w=majority"

        client = MongoClient(f"{srv_url}&ssl=true&ssl_cert_reqs=CERT_NONE")

        return client[database]

