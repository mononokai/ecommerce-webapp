full_product_query = """
    select user_id as user, 
    concat(first_name, ' ', last_name) as name, 
    vendor_prod_id as vend, 
    prod_var_id as prod_var, 
    product_id as prod, 
    color_id as col_id, 
    color_name as color, 
    size_id, 
    size_name as size,
    product.name as prod_name, 
    price, 
    inventory as inv, 
    img_url as img, 
    description as descr, 
    disc_price as d_price, 
    disc_end_date as disc_end
    from product_variant 
    natural join vendor_product 
    natural join product 
    natural join user
    natural join color
    natural join size
    natural join role;
"""

product_query = """

"""