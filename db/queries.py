full_product_select = """
    select user_id, 
    email, 
    first_name, 
    last_name, 
    concat(first_name, ' ', last_name) as full_name, 
    vendor_prod_id, 
    prod_var_id, 
    product_id, 
    color_id, 
    color_name, 
    size_id, 
    size_name, 
    product.name, 
    price, 
    inventory, 
    category, 
    rating, 
    img_url, 
    description, 
    disc_price,
    disc_end_date 
    from product_variant 
    natural join vendor_product 
    natural join product 
    natural join user 
    natural join color 
    natural join size 
    natural join role
"""

product_query = """

"""