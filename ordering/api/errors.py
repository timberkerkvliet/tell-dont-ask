class ApprovedOrderCannotBeRejectedError(Exception):
    def __repr__(self):
        return "ApprovedOrderCannotBeRejectedError"


class OrderCannotBeShippedError(Exception):
    def __repr__(self):
        return "OrderCannotBeShippedError"


class OrderCannotBeShippedTwiceError(Exception):
    def __repr__(self):
        return "OrderCannotBeShippedTwiceException"


class RejectedOrderCannotBeApprovedError(Exception):
    def __repr__(self):
        return "RejectedOrderCannotBeApprovedError"


class ShippedOrdersCannotBeChangedError(Exception):
    def __repr__(self):
        return "ShippedOrdersCannotBeChangedError"


class UnknownProductError(Exception):
    def __repr__(self):
        return "UnknownProductError"
