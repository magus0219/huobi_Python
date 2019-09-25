import gzip


from huobi.impl.utils.timeservice import convert_cst_in_millisecond_to_utc
from huobi.model import *


class OrderListRequest:
    """
    The order update received by subscription of order update.

    :member
        symbol: The symbol you subscribed.
        timestamp: The UNIX formatted timestamp generated by server in UTC.
        data: The order detail.

    """

    def __init__(self):
        self.symbol = ""
        self.timestamp = 0
        self.client_req_id = ""
        self.topic = ""
        self.order_list = list()

    @staticmethod
    def json_parse(json_data, account_type_map):
        req_obj = OrderListRequest()
        error_code = json_data.get_int("err-code")
        req_obj.timestamp = convert_cst_in_millisecond_to_utc(json_data.get_int("ts"))
        req_obj.client_req_id = json_data.get_string("cid")
        req_obj.topic = json_data.get_string("topic")
        req_obj.symbol = json_data.get_string_or_default("symbol", "")
        if error_code == 0:   # only get data for successful request
            order_list_json = json_data.get_array("data")

            order_list = list()
            for order_json in order_list_json.get_items():
                account_id = order_json.get_int("account-id")
                account_type = AccountType.INVALID
                if account_id in account_type_map:
                    account_type = account_type_map[account_id]
                order_obj = Order.json_parse(order_json, account_type)
                order_list.append(order_obj)
            req_obj.order_list = order_list

        return req_obj

    @staticmethod
    def update_symbol(req_obj: 'OrderListRequest', symbol=None):
        if symbol and len(symbol):
            req_obj.symbol = symbol   # update by setting value
        else:
            if len(req_obj.order_list):
                for order_obj in req_obj.order_list:
                    req_obj.symbol = order_obj.symbol   # update by order symbol
                    break

        return req_obj

    def print_object(self, format_data=""):
        from huobi.base.printobject import PrintBasic
        PrintBasic.print_basic(self.symbol, "Symbol")
        PrintBasic.print_basic(self.timestamp, "Timestamp")
        PrintBasic.print_basic(self.client_req_id, "Client Req ID")
        PrintBasic.print_basic(self.topic, "Topic")
        print("Order List as below : count " + str(len(self.order_list)))
        if len(self.order_list):
            for order_obj in self.order_list:
                order_obj.print_object("\t ")
                print()


if __name__ == "__main__":
    from huobi.impl.utils import parse_json_from_string
    from huobi.base.printobject import PrintBasic, PrintMix
    from huobi.constant.test import *
    from huobi import SubscriptionClient
    from huobi.impl.utils import parse_json_from_string
    from huobi.impl.accountinfomap import account_info_map

    sub_client = SubscriptionClient(api_key=g_api_key, secret_key=g_secret_key)
    #json_str = """{"op":"req","ts":1569307523736,"topic":"orders.list","err-code":0,"cid":true,"data":[{"id":48902976275,"symbol":"eosusdt","account-id":10057288,"amount":"10.000000000000000000","price":"0.0","created-at":1569033319999,"type":"sell-market","finished-at":1569033320090,"source":"spot-app","state":"filled","canceled-at":0,"filled-amount":"10.000000000000000000","filled-cash-amount":"40.583000000000000000","filled-fees":"0.081166000000000000"},{"id":48901052613,"symbol":"eosusdt","account-id":10057288,"amount":"10.000000000000000000","price":"4.017600000000000000","created-at":1569031956554,"type":"sell-limit","finished-at":1569032257190,"source":"spot-app","state":"filled","canceled-at":0,"filled-amount":"10.000000000000000000","filled-cash-amount":"40.176000000000000000","filled-fees":"0.080352000000000000"}]}"""
    json_str = """{"op":"req","ts":1569313176281,"topic":"orders.detail","err-code":0,"cid":"1569313176210","data":{"id":48902976275,"symbol":"eosusdt","account-id":10057288,"amount":"10.000000000000000000","price":"0.0","created-at":1569033319999,"type":"sell-market","finished-at":1569033320090,"source":"spot-app","state":"filled","canceled-at":0,"filled-amount":"10.000000000000000000","filled-cash-amount":"40.583000000000000000","filled-fees":"0.081166000000000000"}}"""
    json_bytes = bytes(json_str, encoding='utf8')
    json_wrapper = parse_json_from_string(json_bytes.decode("utf-8"))

    """
    #order_req_obj = OrderListRequest.json_parse_all(json_wrapper)
    order_req_obj = OrderListRequest.json_parse(json_wrapper)
    order_req_obj = OrderListRequest.update_symbol(order_req_obj)


    print("---- order list:  ----")
    PrintBasic.print_basic(order_req_obj.symbol, "Symbol")
    PrintBasic.print_basic(order_req_obj.timestamp, "Timestamp")
    PrintBasic.print_basic(order_req_obj.client_req_id, "Client Req ID")
    PrintBasic.print_basic(order_req_obj.topic, "Topic")
    print("Account List as below : count " + str(len(order_req_obj.order_list)))
    if len(order_req_obj.order_list):
        for order_obj in order_req_obj.order_list:
            PrintMix.print_data(order_obj)

            account_type = account_info_map.get_account_by_id(g_api_key,
                                               order_obj.account_type).account_type

            print("account type ============= " + account_type)
    print()
    """

