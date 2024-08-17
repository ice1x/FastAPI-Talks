from schemas.orders import OrderCreate, OrderRead
from api.dependencies.grpc.call_grpc_responder import gRPBResponderClient


class RestaurantLogic:
    def __init__(self):

    def _get_grpc_responder_timestamp(self, dessert: str):
        return gRPBResponderClient().get_ts(order=dessert)

    def build_order(self, order_create: OrderCreate) -> OrderRead:
        drink = self._get_drink(order_create.drink)
        meal = self._get_meal(order_create.meal)
        dessert = self._get_dessert(order_create.dessert)

        return OrderRead(
            order_id=order_create.order_id,
            drink=drink["order_status"],
            meal=meal["order_status"],
            dessert=dessert["order_status"],
        )
