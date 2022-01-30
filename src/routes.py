import random

from flask import Flask, render_template, redirect, request
from flask.helpers import url_for

from src.controllers import (
    auth_controller,
    customer_controller,
    officers_controller
)

app = Flask(__name__)

officers       = officers_controller()
customers      = customer_controller()
authentication = auth_controller()




"""
        ========================= product routes ===============================

"""
@app.route("/", methods = ["GET"] )
def index() -> None :

    return customers.landing_page_controller()


@app.route("/products", methods = ["GET"])
def products() :

    """
        ke halaman semua produk

    """

    return render_template('page/index.html')


@app.route("/product/<route>", methods = ["GET"] )
def product_detail(route) -> None :

    """
        ke halaman spesifik produk

    """

    return customers.specific_product_page_controller(
        route = route
    )


@app.route("/order/<route>", methods = ["GET", "POST"] )
def order_detail(route) -> None :

    """
        ke halaman form pemesanan produk spesifik 

    """
    return customers.order_product_page_controller(

        route  = route,
        method = request.method,
        data   = request.form
    )


@app.route("/order/purchace/<queue_code>", methods = ["GET"] )
def order_purchace(queue_code) -> None :

    """
        ke halaman pembayaran sesuai kode antrian

        - rekening (static)
        - wa (dynamic) -> kirim bukti pembayaran

    """

    return customers.specific_order_product_page_controller(

        queue_code = queue_code

    )


@app.route("/order/search", methods = ["GET"] )
def order_search() -> None :



    return render_template("page/queue_search.html")



@app.route("/order/tanya-ongkir")
def about_shipping() :

    """
        lempar ke telegram

    """

    return render_template("coming-soon.html")


"""
=================================================================================================
=================================================================================================
"""













"""
        ============================== admin routes =============================

"""

@app.route("/login", methods = ["GET","POST"])
def officers_login() :

    # redirect to login admin
    return authentication.login_officers(

        method = request.method,
        data   = request.form

    )

@app.route("/dashboard/<token>", methods = ["GET"])
def officers_dashboard(token) :

    # redirect to dashboard
    return officers.access_dashboard(token = token)




# product route

@app.route("/add_product/<token>", methods = ["GET","POST"])
def officers_add_product(token) :

    print(request.method)

    # redirect to add product form
    return officers.access_form_add_product(
        
        token  = token,
        method = request.method,

        data   = request.form
        
    )


@app.route("/view_products/<token>", methods = ["GET","POST"])
def officers_view_product(token) :

    # redirect to view products
    return officers.access_show_products( token = token )


@app.route("/edit_product/<token>/<product_id>", methods = ["GET","POST"])
def officers_edit_product(token, product_id) :

    # redirect to detail product
    return officers.access_detail_and_update_product(

        token = token,
        method = request.method,
        product_id = product_id,
        data = request.form
        
    )


@app.route("/delete_product/<product_id>/<token>")
def officers_delete_product(product_id, token) :

    # redirect to detail product
    return 0


@app.route("/order_views/<token>", methods = ["GET"])
def officers_view_order(token) :

    # redirect to detail product
    return officers.access_show_orders( token = token )


@app.route("/order/detail/<token>/<order_id>", methods = ["GET","POST"] )
def officers_detail_order(token, order_id) :

    return officers.access_detail_order(

        token = token,
        method = request.method,
        order_id = order_id,
        data = request.form
        
    )


@app.route("/order/delete/<token>/<product_id>")
def officers_delete_order(token, product_id) :

    return 0


@app.route("/order/follow/<token>/<product_id>")
def officers_follow_up_order(token, product_id) :

    return 0


@app.route("/integration/fb/<token>", methods = ["GET","POST"])
def officers_integration_fb(token) :

    return officers.access_fb_integration(

        token  = token,
        method = request.method,
        data   = request.form

    )



@app.route("/order_notification/<token>", methods = ["GET","POST"])
def officers_order_notif(token) :

    return officers.access_api_notification( token = token )


@app.route("/coming_soon")
def coming_soon() :

    """
        lempar ke telegram

    """

    return render_template("coming-soon.html")

    


# @app.route("/admin/orders/<token>")
# def admin_orders(product_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman semua pesanan.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0

# @app.route("/admin/detail/<order_id>/<token>")
# def admin_detail_order(product_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman detail pemesan.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0

# @app.route("/admin/edit/<order_id>/<token>")
# def admin_edit_order(product_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman edit pesanan.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0


# @app.route("/admin/delete/<order_id>/<token>")
# def admin_delete_order(product_id, token) :

#     """
#         jika token benar punya admin, hapus pesanan terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0


# @app.route("/admin/officers/<token>")
# def admin_show_officers(product_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman officers.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0



# @app.route("/admin/add-admin/<token>")
# def admin_add_admin(product_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman form tambah admin.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0


# @app.route("/admin/detail/<admin_id>/<token>")
# def admin_detail_admin(product_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman detail admin (sesuai token).
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0

# @app.route("/admin/add-operator/<token>")
# def admin_add_operator(product_id, token) :

#     """
#         jika token benar punya admin, hapus admin.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0


# @app.route("/admin/detail/<operator_id>/<token>")
# def admin_detail_operator(product_id, token) :

#     """
#         jika token benar punya admin, hapus admin.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0


# @app.route("/admin/edit/<operator_id>/<token>")
# def admin_edit_operator(product_id, token) :

#     """
#         jika token benar punya admin, hapus admin.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0


# @app.route("/admin/delete/<operator_id>/<token>")
# def admin_delete_operator(product_id, token) :

#     """
#         jika token benar punya admin, hapus admin.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return 0



# @app.route("/admin/import-orders/<file_name>/<token>")
# def admin_import_orders(product_id, token) :

#     filename = ["pdf", "csv", "xlxs", "docx"]

#     """
#         jika token benar punya admin, hapus pesanan terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return product_id, token


# @app.route("/admin/import-paid-orders/<file_name>/<token>")
# def admin_import_paid_orders(product_id, token) :

#     filename = ["pdf", "csv", "xlxs", "docx"]

#     """
#         jika token benar punya admin, hapus pesanan terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return product_id, token


# @app.route("/admin/import-nopaid-order/<file_name>/<token>")
# def admin_import_nopaid_orders(product_id, token) :

#     filename = ["pdf", "csv", "xlxs", "docx"]

#     """
#         jika token benar punya admin, hapus pesanan terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return product_id, token



# """
# =================================================================================================
# =================================================================================================
# """














# """
#     =============== operator routes ===================

# """

# @app.route("/operator/dashboard/<token>")
# def operator_dashboard(token) :

#     """
#         jika token benar punya operator, lempar ke halaman.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return token


# @app.route("/operator/products/<token>")
# def operator_products(token) :

#     """
#         jika token benar punya admin, lempar ke halaman form tambah produk.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return token


# @app.route("/operator/add-product/<token>")
# def operator_add_product(token) :

#     """
#         jika token benar punya admin, lempar ke halaman form tambah produk.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return token


# @app.route("/operator/detail/<product_id>/<token>")
# def operator_detail_product(token) :

#     """
#         jika token benar punya admin, lempar ke halaman form tambah produk.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return token


# @app.route("/operator/edit/<product_id>/<token>")
# def operator_edit_product(product_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman form edit produk.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return product_id, token


# @app.route("/operator/delete/<product_id>/<token>")
# def operator_delete_product(product_id, token) :

#     """
#         jika token benar punya admin, hapus produk terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return product_id, token


# @app.route("/operator/orders/<token>")
# def admin_orders(token) :

#     """
#         jika token benar punya admin, lempar ke halaman semua pesanan.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return token

# @app.route("/operator/detail/<order_id>/<token>")
# def admin_token(order_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman detail pemesan.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return order_id, token

# @app.route("/operator/edit/<order_id>/<token>")
# def admin_token(order_id, token) :

#     """
#         jika token benar punya admin, lempar ke halaman edit pesanan.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return order_id, token


# @app.route("/operator/delete/<order_id>/<token>")
# def admin_token(order_id, token) :

#     """
#         jika token benar punya admin, hapus pesanan terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return order_id, token


# @app.route("/operator/import-orders/<file_name>/<token>")
# def admin_token(file_name, token) :

#     filename = ["pdf", "csv", "xlxs", "docx"]

#     """
#         jika token benar punya admin, hapus pesanan terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return file_name, token


# @app.route("/admin/import-paid-orders/<file_name>/<token>")
# def admin_token(file_name, token) :

#     filename = ["pdf", "csv", "xlxs", "docx"]

#     """
#         jika token benar punya admin, hapus pesanan terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return file_name, token


# @app.route("/admin/import-nopaid-orders/<file_name>/<token>")
# def admin_token(file_name, token) :

#     filename = ["pdf", "csv", "xlxs", "docx"]

#     """
#         jika token benar punya admin, hapus pesanan terpilih.
#         kalau salah, lempar ke halaman login admin
    
#     """

#     return file_name, token








# """
#     customer routes

# """





# """
#     searching routes ( API )

# """