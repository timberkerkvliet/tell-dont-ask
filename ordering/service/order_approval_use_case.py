from ordering.domain.order_status import OrderStatus
from ordering.repository.OrderRepository import OrderRepository
from ordering.api.ApprovedOrderCannotBeRejectedError import ApprovedOrderCannotBeRejectedError
from ordering.api.OrderApprovalRequest import OrderApprovalRequest
from ordering.api.RejectedOrderCannotBeApprovedError import RejectedOrderCannotBeApprovedError
from ordering.api.ShippedOrdersCannotBeChangedError import ShippedOrdersCannotBeChangedError


class OrderApprovalUseCase:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository

    def run(self, request: OrderApprovalRequest):
        order = self.order_repository.get_by_id(request.get_order_id())

        if order.get_status() is OrderStatus.SHIPPED:
            raise ShippedOrdersCannotBeChangedError()

        if request.is_approved() and order.get_status() is OrderStatus.REJECTED:
            raise RejectedOrderCannotBeApprovedError()

        if not request.is_approved() and order.get_status() is OrderStatus.APPROVED:
            raise ApprovedOrderCannotBeRejectedError()

        order.set_status(OrderStatus.APPROVED if request.is_approved() else OrderStatus.REJECTED)
        self.order_repository.save(order)
