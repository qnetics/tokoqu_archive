from math import ceil 

from flask import render_template, jsonify
from flask.helpers import url_for

from werkzeug.utils import redirect

from src.models.repositories import (

    customer_repo,
    integration_repo,
    admin_and_operators_repo,
    authentication_and_authorization_repo

)

from src.apis.security import password_hashing
from src.apis.price_convert import ( rupiah_format, rupiah_str_to_int )






class customer_controller(customer_repo, integration_repo) :


    def __init__(self) -> None:

        super().__init__()


    def landing_page_controller(self) -> None :

        landing_data_products = self.landing_products()

        return render_template(

            "page/index.html",
            products = landing_data_products,
            recommendation_length = len(landing_data_products["recommendations"])

        )


    def products_page_controller(self) -> None :

        landing_data_products = self.landing_products()

        return render_template(

            "page/index.html",
            products = landing_data_products

        )


    def specific_product_page_controller(self, route) -> None :

        request_product_by_route = self.specific_and_order_form_product( route = route )

        # sorting variant images
        variant_images    = []
        length_of_variant = len(request_product_by_route["single"]["variant_images"])


        if length_of_variant < 1 :

            pass

        else :

            start_index = 0
            end_index   = 4

            for index_variant in range(ceil(length_of_variant/4)) :

                sorting = request_product_by_route["single"]["variant_images"][start_index:end_index]

                variant_images.append(sorting)

                start_index += end_index
                end_index   += end_index


        return render_template(

            "page/detail.html",

            single_product = request_product_by_route["single"],

            length_single_images = len(request_product_by_route["single"]["product_images"]),

            variant_images = variant_images,
            length_variant_images = len(variant_images),

            recommendation_products = request_product_by_route["recommendations"],
            length_recommendation = len(request_product_by_route["recommendations"])

        )


    def order_product_page_controller(self, route, method, data) -> None :

        request_product_by_route = self.specific_and_order_form_product( route = route )

        if method == "POST" :

            order_data = {

                "id"       : request_product_by_route["single"]["id"],
                "name"     : data["name"],
                "tel_num"  : data["tel_num"],
                "jl"       : data["jl"],
                "rt"       : data["rt"],
                "rw"       : data["rw"],
                "kel"      : data["kel"],
                "kec"      : data["kec"],
                "city"     : data["city"],
                "prov"     : data["prov"],
                "no"       : data["no"],
                "postal"   : data["postal"],
                "quantity" : data["quantity"],
                "desc"     : data["desc"]

            }

            queue_code = self.purchace_queue_order( payload = order_data )

            data_meta = {

                "pixel_id" : self.show_id_integration_fb_ads(),
                "price_value" : queue_code["price_value"],
                "content_name" : queue_code["content_name"]

            }

            return render_template(

                "page/queue-code.html",
                data_meta = data_meta,
                order_queue = queue_code["queue"]

            )

        else :

            data_meta = {

                "pixel_id" : self.show_id_integration_fb_ads(),
                "price_value" : rupiah_str_to_int(request_product_by_route["single"]["price"]),
                "content_name" : request_product_by_route["single"]["name"]

            }

            return render_template(

                "page/checkout-order.html",
                data_meta = data_meta,
                single_product =  request_product_by_route["single"]

            )


    def specific_order_product_page_controller(self, queue_code) -> None :

        request_product_by_queue = self.purchace_order(

            queue_code = queue_code

        )

        if request_product_by_queue["status"] == "found" :

            return render_template(

                "page/detail-order.html",

                single_product = request_product_by_queue["product_data"],

                length_single_images = len(request_product_by_queue["product_data"]["product_images"]),

                variant_images = request_product_by_queue["product_data"]["variant_images"],
                length_variant_images = len(request_product_by_queue["product_data"]["variant_images"]),

                customer_data = request_product_by_queue["customer_data"],

                order_data = request_product_by_queue["order_data"]

            )

        else : 

            return render_template("page/404.html", queue_code = queue_code)



class officers_controller(admin_and_operators_repo, authentication_and_authorization_repo, integration_repo) :

    def __init__(self) -> None:

        super().__init__()


    # personal

    def access_show_personal(self) -> None :

        return 0

    def access_delete_personal(self) -> None :

        return 0



    # for admin and operator


    # ----------------- [ access_form_add_product ] ---------------------

    # """ to dashboard access """
    def access_dashboard(self, token) -> None :

        user_datas = self.repo_dashboard( token = token )

        if user_datas["response"] == "found" :

            if user_datas["status"] == "admin" :

                show_order_data = self.repo_show_orders()

                # sort total product and order

                total_product = len( self.repo_show_products() )

                total_order   = len( show_order_data ) 

                # sort newest order

                show_order_data = [ show_order_data[len(show_order_data) - (index_newest + 1) ] for index_newest in range( len(show_order_data)) ]

                return render_template(
                    
                    f"dashboard/{user_datas['status']}/dashboard_{user_datas['status']}.html",

                    user_datas = user_datas,

                    token = token,

                    order_datas = show_order_data,
                    length_order_datas = len(show_order_data),

                    total_product = total_product,
                    total_order   = total_order

                )

            elif user_datas["status"] == "operator" :

                show_order_data = self.repo_show_orders()

                return render_template(f"dashboard/{user_datas['status']}/dashboard_{user_datas['status']}.html", user_datas = user_datas, token = token)

            else :

                return redirect(url_for("officers_login"))

        else :

            return redirect(url_for("officers_login"))




    # ----------------- [ access_form_add_product ] ---------------------

    """ to form add product access """
    def access_form_add_product(self, token, method, data) -> None :

        token_checking = self.validate_token( token = token )

        # generate route for name
        def route_generator(name) -> str :

            return "".join(

                [ "-" if name[strnames] == " " else name[strnames] for strnames in range(len(name)) ]
            )

        # sort product image column
        def product_images(data) -> list :

            # product images
            product_images = []

            for images in range(5) :

                if data[f"image{images}"] != "" :

                    product_images.append(data[f"image{images}"])

                else :

                    pass
            
            return product_images


        # sort variant image column
        def variant_images(data) -> list :

            # variant images
            variant_images = []

            for variants in range(8) :

                if data[f"variant{variants}"] != "" :

                    variant_images.append(data[f"variant{variants}"])

                else :

                    pass

            return variant_images


        # token identification
        if token_checking["response"] == "found" :

            # method identification
            if method == "POST" :

                # send data to database
                product_datas = {

                    "name"  : data["name"],
                    "price" : rupiah_format(angka=int(data["price"]), with_prefix=True),
                    "desc"  : data["desc"],
                    "route" : route_generator(name=data["name"]),
                    "product_images" : product_images(data=data),
                    "variant_images" : variant_images(data=data)

                }

                user_datas = self.repo_form_add_product( data = product_datas )

                if user_datas :

                    return redirect(url_for("officers_view_product", token = token))
                


            else :

                # redirect to form
                return render_template(f"dashboard/{token_checking['status']}/form_add_product_admin.html", token = token)

        else :

            return redirect(url_for("officers_login"))



    # """ access show products """
    def access_show_products(self, token) -> None :

        token_checking = self.validate_token( token = token )

        if token_checking["response"] == "found" : 

            request_products = self.repo_show_products()

            request_products = [ request_products[len(request_products) - (index_newest + 1) ] for index_newest in range( len(request_products) ) ]

            return render_template(f"dashboard/{token_checking['status']}/product_{token_checking['status']}.html",
                                   token = token, 
                                   data_products = request_products 
            )

        else :

            return redirect(url_for("officers_login"))



    # """ access detail and update product """
    def access_detail_and_update_product(self, token, method, product_id, data) -> None :

        token_checking = self.validate_token( token = token )

        if token_checking["response"] == "found" : 

            # "POST" method
            if method == "POST" :

                product_payload = {

                    "name"  : data["name"],
                    "price" : rupiah_str_to_int(data["price"]),
                    "desc"  : data["desc"],
                    "product_images" : [ data[f"image{image}"] for image in range(4) ],
                    "variant_images" : [ data[f"variant{variant}"] for variant in range(7) ]

                }

                new_data = self.repo_edit_product(product_id = product_id, new_payload = product_payload)

                return render_template(f"dashboard/{token_checking['status']}/form_edit_product_{token_checking['status']}.html",
                                   token = token, 
                                   data_products = new_data,
                                   images_len  = len(new_data["product_images"]),
                                   variant_len = len(new_data["variant_images"]) 
                )

            # "GET" method
            else :

                get_data_product = self.repo_single_product( product_id = product_id )

                # sort product images
                product_images = []

                for index_product_images in range( len(get_data_product["product_images"]) + (5-len(get_data_product["product_images"])) ) :

                    try :

                        product_images.append( get_data_product["product_images"][index_product_images] )

                    except IndexError :

                        product_images.append("")

                get_data_product.update(

                    { "product_images" : product_images }

                )


                # sort ariant images
                variant_images = []

                for index_variant_images in range( len(get_data_product["variant_images"]) + (8-len(get_data_product["variant_images"])) ) :

                    try :

                        variant_images.append( get_data_product["variant_images"][index_variant_images] )

                    except IndexError :

                        variant_images.append("")

                get_data_product.update(

                    { "variant_images" : variant_images }

                )

                return render_template(f"dashboard/{token_checking['status']}/form_edit_product_{token_checking['status']}.html",
                                   token = token, 
                                   data_products = get_data_product,
                                   images_len  = len(product_images),
                                   variant_len = len(variant_images) 
                )

        else :

            return redirect(url_for("officers_login"))


    def access_delete_product(self, token, product_id) -> None :

        return 0

    def access_show_orders(self, token) -> None :

        token_checking = self.validate_token( token = token )

        if token_checking["response"] == "found" :

            show_order_data = self.repo_show_orders()

            show_order_data = [ show_order_data[len(show_order_data) - (index_newest + 1) ] for index_newest in range( len(show_order_data)) ]

            return render_template(
                
                f"dashboard/{token_checking['status']}/show_order_{token_checking['status']}.html",
                token = token,
                order_datas = show_order_data,
                length_order_datas = len(show_order_data)
                
            )

        else :

             return redirect(url_for("officers_login"))


    def access_detail_order(self, token, order_id, method, data) -> None :

        # token checking

        token_checking = self.validate_token( token = token )

        if token_checking["response"] == "found" :

            # method checking

            if method == "POST" :

                self.repo_update_order( order_id = order_id, payload = data )

                return redirect( url_for("officers_view_order", token = token ) )

            else :

                specific_order_datas = self.repo_specific_order( order_id = order_id )

                return render_template(

                    f"dashboard/{token_checking['status']}/form_detail_order_{token_checking['status']}.html",
                    token = token,
                    order_data = specific_order_datas

                )


        else :

            return redirect(url_for("officers_login"))



    def access_delete_order(self, token, order_id) -> None :

        token_checking = self.validate_token( token = token )

        if token_checking["response"] == "found" :

            return 0

        else :

            return redirect(url_for("officers_login"))


    def access_follow_up_order(self, token, number_phone) -> None :

        token_checking = self.validate_token( token = token )

        if token_checking["response"] == "found" :

            whatapp_api = f""

            return 0

        else :

            return redirect(url_for("officers_login"))



    def access_api_notification( self, token ) :

        token_checking = self.validate_token( token = token )

        if token_checking["response"] == "found" :

            result = self.repo_notification()

            result.update({

                "status" : "success"
            })

            return jsonify( result ), 200

        else :

            return jsonify({

                "status" : "failed"

            }), 400



    # admin only access

    def access_add_admin(self) -> None :

        return 0

    def access_add_operators(self) -> None :

        return 0

    def access_detail_admin(self) -> None :

        return 0

    def access_detail_operator(self) -> None :

        return 0

    def access_delete_operator(self) -> None :

        return 0


    # +--------- integration ----------+

    def access_fb_integration(self, token, method, data) -> None :

        token_checking = self.validate_token( token = token )

        if token_checking["response"] == "found" : 


            if method == "POST" :

                insert_id_fb_ads = self.add_and_update_integration_fb_ads(id = data["pixel_id"])

                return render_template(
                
                    f"dashboard/admin/form_fb_integration.html",
                    token = token,
                    pixel_id = insert_id_fb_ads
                    
                )

            else :

                show_id_fb_ads = self.show_id_integration_fb_ads()

                if show_id_fb_ads != None :

                    return render_template(
                    
                        f"dashboard/admin/form_fb_integration.html",
                        token = token,
                        pixel_id = show_id_fb_ads
                        
                    )

                else :

                    return render_template(
                    
                        f"dashboard/admin/form_fb_integration.html",
                        token = token,
                        pixel_id = ""
                        
                    )

        else :

            0

        # create, read, update, delete
        return 0







class auth_controller(authentication_and_authorization_repo) :

    def __init__(self) -> None:

        super().__init__()

    def login_officers(self, method, data) :

        # POST method
        if method == "POST" :
            
            login_payloads = {

                "username" : data["username"],
                "password" : password_hashing(data["password"]),
                "pin"      : password_hashing(data["pin"]),
                "notelp"   : data["notelp"],
                "email"    : data["email"]

            }

            send_payloads = self.login_user(

                payloads = login_payloads

            )

            if send_payloads["status"] == "admin" :

                return redirect(url_for("officers_dashboard", token = send_payloads['token']))

            elif send_payloads["status"] == "operator" :

                return render_template('page/product.html', message = send_payloads["token"]+"-"+send_payloads["status"])

            else :

                return render_template("admin_dashboard/pages/login.html", value_datas = login_payloads, status = send_payloads["status"])

        # GET method
        else :

            return render_template("admin_dashboard/pages/login.html", value_datas = data)

