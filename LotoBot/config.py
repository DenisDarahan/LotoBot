TOKEN = '410155776:AAH76CmFQ05PUUgtLTaFKKMW3GiPCe2TUsQ'
TOKEN_QIWI = '3e02bd71a2923305048c559a9495954b'

DB_NAME = 'data.db'

admin_id = 386360043
admin_qiwi = 380662807162


PAY_LINK = ('https://qiwi.com/payment/form/99?'
            'extra%5B%27account%27%5D=' + str(admin_qiwi) +        # Телефон
            '&amountInteger={}'                                    # Рубли
            '&amountFraction={}'                                   # Копейки
            '&extra%5B%27comment%27%5D={}'                         # Комментарий
            '&currency=643')

headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'Authorization': 'Bearer {}'.format(TOKEN_QIWI)}
url = 'https://edge.qiwi.com/sinap/api/v2/terms/99/payments'
url_get_history_payed = 'https://edge.qiwi.com/payment-history/v2/persons/{}/payments'.format(admin_qiwi)
