import unittest

from src.domain.Order import Order
from src.domain.OrderStatus import OrderStatus
from src.api.ApprovedOrderCannotBeRejectedError import ApprovedOrderCannotBeRejectedError
from src.api.OrderApprovalRequest import OrderApprovalRequest
from src.service.OrderApprovalUseCase import OrderApprovalUseCase
from src.api.RejectedOrderCannotBeApprovedError import RejectedOrderCannotBeApprovedError
from src.api.ShippedOrdersCannotBeChangedError import ShippedOrdersCannotBeChangedError
from test.doubles.TestOrderRepository import TestOrderRepository


class TestOrderApprovalUseCase(unittest.TestCase):
    def setUp(self):
        self.order_repository = TestOrderRepository()
        self.use_case = OrderApprovalUseCase(self.order_repository)

    def test_approved_existing_order(self):
        initial_order = Order()
        initial_order.set_status(OrderStatus.CREATED)
        initial_order.set_id(1)
        self.order_repository.add_order(initial_order)

        request = OrderApprovalRequest()
        request.set_order_id(1)
        request.set_approved(True)

        self.use_case.run(request)

        saved_order = self.order_repository.get_saved_order()

        self.assertEqual(
            OrderStatus.APPROVED,
            saved_order.get_status()
        )

    def test_rejected_existing_order(self):
        initial_order = Order()
        initial_order.set_status(OrderStatus.CREATED)
        initial_order.set_id(1)
        self.order_repository.add_order(initial_order)

        request = OrderApprovalRequest()
        request.set_order_id(1)
        request.set_approved(False)

        self.use_case.run(request)

        saved_order = self.order_repository.get_saved_order()

        self.assertEqual(
            OrderStatus.REJECTED,
            saved_order.get_status()
        )

    def test_cannot_approve_rejected_order(self):
        initial_order = Order()
        initial_order.set_status(OrderStatus.REJECTED)
        initial_order.set_id(1)
        self.order_repository.add_order(initial_order)

        request = OrderApprovalRequest()
        request.set_order_id(1)
        request.set_approved(True)

        with self.assertRaises(RejectedOrderCannotBeApprovedError):
            self.use_case.run(request)

        self.assertIsNone(self.order_repository.get_saved_order())

    def test_cannot_reject_approved_order(self):
        initial_order = Order()
        initial_order.set_status(OrderStatus.APPROVED)
        initial_order.set_id(1)
        self.order_repository.add_order(initial_order)

        request = OrderApprovalRequest()
        request.set_order_id(1)
        request.set_approved(False)

        with self.assertRaises(ApprovedOrderCannotBeRejectedError):
            self.use_case.run(request)

    def test_shipped_orders_cannot_be_approved(self):
        initial_order = Order()
        initial_order.set_status(OrderStatus.SHIPPED)
        initial_order.set_id(1)
        self.order_repository.add_order(initial_order)

        request = OrderApprovalRequest()
        request.set_order_id(1)
        request.set_approved(True)

        with self.assertRaises(ShippedOrdersCannotBeChangedError):
            self.use_case.run(request)

        self.assertIsNone(self.order_repository.get_saved_order())

    def test_shipped_orders_cannot_be_rejected(self):
        initial_order = Order()
        initial_order.set_status(OrderStatus.SHIPPED)
        initial_order.set_id(1)
        self.order_repository.add_order(initial_order)

        request = OrderApprovalRequest()
        request.set_order_id(1)
        request.set_approved(False)

        with self.assertRaises(ShippedOrdersCannotBeChangedError):
            self.use_case.run(request)

        self.assertIsNone(self.order_repository.get_saved_order())
