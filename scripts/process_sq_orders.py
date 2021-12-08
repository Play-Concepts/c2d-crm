import pandas as pd

from app.apis.utils.random import random_string

from app.apis.utils.transformer import concat

orders_file = 'orders.csv'
df = pd.read_csv(orders_file)

placeholder_image_url = 'https://images.squarespace-cdn.com/content/v1/611386630a0d433d1854d656/1633288429020-RAJHS2AFJD941OZB1AYV/1FAE1105-E04D-4B51-B0BE-4B826DF326A2?format=500whttps://images.squarespace-cdn.com/content/v1/611386630a0d433d1854d656/1633288429020-RAJHS2AFJD941OZB1AYV/1FAE1105-E04D-4B51-B0BE-4B826DF326A2?format=500w'

NEW_USER_SQL = """
    insert into users(email, hashed_password, is_active, is_verified, is_superuser, is_supplier)
    values('{}', crypt(uuid_generate_v4()::text, gen_salt('bf',10)), true, false, false, false)
    RETURNING id;
"""
NEW_MERCHANT_SQL = """
    INSERT INTO merchants(first_name, last_name, company_name, trade_name, address, email, phone_number, logo_url, password_change_token, terms_agreed)
    VALUES('{first_name}', '{last_name}', '{company_name}', '{trade_name}', '{address}', '{email}', '{phone_number}', '{logo_url}', '{password_change_token}', true)
    RETURNING id;
"""
NEW_MECHANT_PERK_SQL = """
    INSERT INTO merchant_offers(merchant_id, title, details, start_date, end_date, offer_url, logo_url, offer_image_url)
    VALUES('{merchant_id}', '{title}', '{details}', '{start_date}', '{end_date}', '{offer_url}', '{logo_url}', '{offer_image_url}')
    RETURNING id
"""

for index, row in df.iterrows():
    if row['Fulfillment Status'] == 'pending':
        print(NEW_USER_SQL.format(row['Email']))
        
        names = row["Billing Name"].split()
        last_name = names.pop()
        first_name = " ".join(names)
        address_row = concat(
            row["Billing Address1"],
            row["Billing Address2"],
            row["Billing City"],
            str(row["Billing Zip"]),
            row["Billing Province"],
            row["Billing Country"],
            separator = " ",
            map_fn = lambda x: " ".join(elem.capitalize() for elem in str(x).split()),
            filter_fn = lambda x: x is not None and x != 'nan',
        )
        trade_name = row['Checkout Form: Business Name']
        #logo_url = placeholder_image_url
        logo_url = row["Checkout Form: Logo"]
        
        print(NEW_MERCHANT_SQL.format(first_name=first_name,
                                      last_name=last_name,
                                      company_name=trade_name,
                                      trade_name=trade_name,
                                      address=address_row,
                                      email=row['Email'],
                                      phone_number=row['Billing Phone'],
                                      logo_url=logo_url,
                                      password_change_token=random_string(40),
                                      ))
        
        title = row["Checkout Form: Name of Offer"]
        details = row["Checkout Form: Offer details"]
        raw_start = '11/1/2021' if pd.isna(row["Checkout Form: Start date of Offer"]) else row["Checkout Form: Start date of Offer"]
        raw_end = '1/31/2022' if pd.isna(row["Checkout Form: Expiry date of Offer"]) else row["Checkout Form: Expiry date of Offer"]
        m, d, year = map(lambda x: x.rjust(2, '0'), raw_start.split("/"))
        start_date = "{}-{}-{}".format(year, m, d)
        m, d, year = map(lambda x: x.rjust(2, '0'), raw_end.split("/"))
        end_date = "{}-{}-{}".format(year, m, d)
        
        offer_url = row["Checkout Form: Website"]
        
        
        #offer_image_url = placeholder_image_url
        offer_image_url = row["Checkout Form: Image of your offer"]
                
        print(NEW_MECHANT_PERK_SQL.format(merchant_id='<fill_me_up>',
                                          title=title,
                                          details=details,
                                          start_date=start_date,
                                          end_date=end_date,
                                          offer_url=offer_url,
                                          logo_url=logo_url,
                                          offer_image_url=offer_image_url,
                                          ))
        