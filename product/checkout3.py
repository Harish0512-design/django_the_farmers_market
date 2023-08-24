class CheckOutClass:
    """ this class will implement the discount functionality for codes
        'MKCH', 'APPL', 'APOM', 'BOGO'
    """

    def __init__(self, products_in_cart, discounts):
        self.products_in_cart = products_in_cart
        self.discounts = discounts
        self.bogo_dp = 0
        self.appl_dp = 0
        self.chmk_dp = 0
        self.apom_dp = 0
        self.product_codes_list_in_cart = []
        self.unique_prods_info_in_cart = []
        self.total_price = 0
        self.total_discount = 0
        self.count = 0

    def get_product_codes_in_cart(self):
        if self.count == 0:
            for p in self.products_in_cart:
                self.product_codes_list_in_cart.append(p.get('product_code'))
            self.count += 1
        return self.product_codes_list_in_cart

    def initialize_dps(self):
        """ this method assigns discount prices for discounts """
        for d in self.discounts:
            if d.get('discount_code') == "BOGO":
                self.bogo_dp = float(d.get('discount_price'))

            elif d.get('discount_code') == "APPL":
                self.appl_dp = float(d.get('discount_price'))

            elif d.get('discount_code') == "CHMK":
                self.chmk_dp = float(d.get('discount_price'))

            elif d.get('discount_code') == "APOM":
                self.apom_dp = float(d.get('discount_price'))

    def get_unique_prods_info_in_cart(self):
        """ this method returns unique product information for the products present in cart"""
        pcl = self.get_product_codes_in_cart()
        unique_prod_codes_in_cart = set(pcl)
        self.unique_prods_info_in_cart = []
        for upc in unique_prod_codes_in_cart:
            for p in self.products_in_cart:
                if upc == p.get('product_code'):
                    d = {
                        'product_code': p.get('product_code'),
                        'price': p.get('price'),
                    }
                    self.unique_prods_info_in_cart.append(d)
                    break
        return self.unique_prods_info_in_cart

    def get_final_price_and_discount(self):
        """ this method returns a tuple contains final_price and total_discount """
        self.initialize_dps()
        pcl = self.get_product_codes_in_cart()
        unique_prods_in_carts = self.get_unique_prods_info_in_cart()
        for p in unique_prods_in_carts:
            # applying APPL coupon
            if p.get('product_code') == 'AP1':
                count = pcl.count('AP1')
                if count >= 3:
                    self.total_price += count * self.appl_dp
                    self.total_discount += (p.get('price') - self.appl_dp) * count
                else:
                    self.total_price += count * p.get('price')

            # applying BOGO coupon
            elif p.get('product_code') == 'CF1':
                count = pcl.count('CF1')
                self.total_price += count * self.bogo_dp
                self.total_discount += self.bogo_dp * count

            # applying CHMK coupon
            elif p.get('product_code') == 'CH1':
                ch1count = pcl.count('CH1')
                if 'MK1' in pcl:
                    mk1count = pcl.count('MK1')
                    if ch1count == mk1count:
                        self.total_price += ch1count * p.get('price')
                        self.total_discount += \
                            [up.get('price') for up in unique_prods_in_carts if up.get('product_code') == 'MK1'][
                                0] * mk1count
                        while 'MK1' in pcl:
                            pcl.remove('MK1')
                    elif ch1count > mk1count:
                        self.total_price += ch1count * p.get('price')
                        self.total_discount += \
                            [up.get('price') for up in unique_prods_in_carts if up.get('product_code') == 'MK1'][
                                0] * mk1count
                        while 'MK1' in pcl:
                            pcl.remove('MK1')
                    elif ch1count < mk1count:
                        self.total_price += ch1count * p.get('price') + (mk1count - ch1count) * \
                                            [up.get('price') for up in unique_prods_in_carts if
                                             up.get('product_code') == 'MK1'][
                                                0]
                        self.total_discount = (mk1count - ch1count) * \
                                              [up.get('price') for up in unique_prods_in_carts if
                                               up.get('product_code') == 'CH1'][
                                                  0]
                        while 'MK1' in pcl:
                            pcl.remove('MK1')
                else:
                    ch1count = pcl.count('CH1')
                    self.total_price += ch1count * p.get('price')

            # appling CHMK coupon
            elif p.get('product_code') == 'MK1':
                mk1count = pcl.count('MK1')
                if 'CH1' in pcl:
                    ch1count = pcl.count('CH1')
                    if ch1count == mk1count:
                        self.total_price += ch1count * p.get('price')
                        self.total_discount += \
                            [up.get('price') for up in unique_prods_in_carts if up.get('product_code') == 'MK1'][
                                0] * mk1count
                        unique_prods_in_carts.remove('MK1')
                    elif ch1count > mk1count:
                        self.total_price += ch1count * p.get('price')
                        self.total_discount += \
                            [up.get('price') for up in unique_prods_in_carts if up.get('product_code') == 'MK1'][
                                0] * mk1count
                        while 'CH1' in pcl:
                            pcl.remove('CH1')
                    elif ch1count < mk1count:
                        self.total_price += ch1count * p.get('price') + (mk1count - ch1count) * \
                                            [up.get('price') for up in unique_prods_in_carts if
                                             up.get('product_code') == 'MK1'][
                                                0]
                        self.total_discount = (mk1count - ch1count) * \
                                              [up.get('price') for up in unique_prods_in_carts if
                                               up.get('product_code') == 'CH1'][
                                                  0]
                        while 'CH1' in pcl:
                            pcl.remove('CH1')
                else:
                    mk1count = pcl.count('MK1')
                    self.total_price += mk1count * p.get('price')

        return self.total_price, self.total_discount

# p_c = [{'product_code': 'AP1', 'price': 6.0}, {'product_code': 'AP1', 'price': 6.0},
#        {'product_code': 'CF1', 'price': 11.73}, {'product_code': 'CF1', 'price': 11.73}]
# d_c = [{'discount_code': 'BOGO', 'discount_price': 5.61}, {'discount_code': 'APPL', 'discount_price': 4.59},
#        {'discount_code': 'CHMK', 'discount_price': 3.11}, {'discount_code': 'APOM', 'discount_price': 3.00}]
# co = CheckOut(p_c, d_c)
# print(co.get_final_price_and_discount())
