import unittest

from ordering.domain.order import Order
from ordering.domain.order_status import OrderStatus
from ordering.api.errors import OrderCannotBeShippedError, OrderCannotBeShippedTwiceError
from ordering.api.order_shipment_request import OrderShipmentRequest
from ordering.service.order_shipment_use_case import OrderShipmentUseCase
from test.doubles.TestOrderRepository import TestOrderRepository
from test.doubles.TestShipmentService import TestShipmentService


class TestOrderShipmentUseCase(unittest.TestCase):
    def setUp(self):
        self.order_repository = TestOrderRepository()
        self.shipment_service = TestShipmentService()
        self.use_case = OrderShipmentUseCase(self.order_repository, self.shipment_service)

    def test_ship_approved_order(self):
        initial_order = Order()
        initial_order.set_id(1)
        initial_order.set_status(OrderStatus.APPROVED)
        self.order_repository.add_order(initial_order)

        request = OrderShipmentRequest()
        request.set_order_id(1)

        self.use_case.run(request)

        self.assertEqual(
            OrderStatus.SHIPPED,
            self.order_repository.get_saved_order().get_status()
        )

        self.assertEqual(
            initial_order,
            self.shipment_service.get_shipped_order()
        )

    def test_created_orders_cannot_be_shipped(self):
        initialOrder = Order()
        initialOrder.set_id(1)
        initialOrder.set_status(OrderStatus.CREATED)
        self.order_repository.add_order(initialOrder)

        request = OrderShipmentRequest()
        request.set_order_id(1)

        with self.assertRaises(OrderCannotBeShippedError):
            self.use_case.run(request)

        self.assertIsNone(self.shipment_service.get_shipped_order())

    def test_rejected_orders_cannot_be_shipped(self):
        initialOrder = Order()
        initialOrder.set_id(1)
        initialOrder.set_status(OrderStatus.REJECTED)
        self.order_repository.add_order(initialOrder)

        request = OrderShipmentRequest()
        request.set_order_id(1)

        with self.assertRaises(OrderCannotBeShippedError):
            self.use_case.run(request)

        self.assertIsNone(self.order_repository.get_saved_order())
        self.assertIsNone(self.shipment_service.get_shipped_order())

    def test_shipped_orders_cannot_be_shipped_again(self):
        initialOrder = Order()
        initialOrder.set_id(1)
        initialOrder.set_status(OrderStatus.SHIPPED)
        self.order_repository.add_order(initialOrder)

        request = OrderShipmentRequest()
        request.set_order_id(1)

        with self.assertRaises(OrderCannotBeShippedTwiceError):
            self.use_case.run(request)

        self.assertIsNone(self.order_repository.get_saved_order())
        self.assertIsNone(self.shipment_service.get_shipped_order())
