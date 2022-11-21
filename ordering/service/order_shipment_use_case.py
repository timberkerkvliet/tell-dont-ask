from ordering.domain.order_status import OrderStatus
from ordering.repository.OrderRepository import OrderRepository
from ordering.service.shipment_service import ShipmentService
from ordering.api.OrderCannotBeShippedError import OrderCannotBeShippedError
from ordering.api.OrderCannotBeShippedTwiceError import OrderCannotBeShippedTwiceError
from ordering.api.OrderShipmentRequest import OrderShipmentRequest


class OrderShipmentUseCase(object):
    def __init__(self, order_repository: OrderRepository, shipment_service: ShipmentService):
        self.order_repository = order_repository
        self.shipment_service = shipment_service

    def run(self, request: OrderShipmentRequest):
        order = self.order_repository.get_by_id(request.get_order_id())

        if order.get_status() is OrderStatus.CREATED or order.get_status() is OrderStatus.REJECTED:
            raise OrderCannotBeShippedError()

        if order.get_status() is OrderStatus.SHIPPED:
            raise OrderCannotBeShippedTwiceError()

        self.shipment_service.ship(order)

        order.set_status(OrderStatus.SHIPPED)
        self.order_repository.save(order)
