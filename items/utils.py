import stripe


def check_discounts_and_tax(order):
    coupon = []
    tax_percent = []
    if order.tax:
        tax_percent = stripe.TaxRate.create(
            display_name=order.tax.name if order.tax else "Discount Tax",
            percentage=order.tax.percent,
            inclusive=False, )
        tax_percent = [tax_percent.id]

    if order.discount:
        coupon = stripe.Coupon.create(
            percent_off=order.discount.percent,
            duration="once",
        )
        coupon = [{'coupon': coupon.id}]



    return coupon, tax_percent
