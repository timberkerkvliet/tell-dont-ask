import decimal
import unittest

from src.domain.Category import Category
from src.domain.OrderStatus import OrderStatus
from src.domain.Product import Product
from src.service.OrderCreationUseCase import OrderCreationUseCase
from src.api.SellItemRequest import SellItemRequest
from src.api.SellItemsRequest import SellItemsRequest
from src.api.UnknownProductError import UnknownProductError
from test.doubles.InMemoryProductCatalog import InMemoryProductCatalog
from test.doubles.TestOrderRepository import TestOrderRepository


class TestOrderCreationUseCase(unittest.TestCase):
    def setUp(self):
        self.order_repository = TestOrderRepository()

        food = Category()
        food.set_name("food")
        food.set_tax_percentage(decimal.Decimal("10"))

        product1 = Product()
        product1.set_name("salad")
        product1.set_price(decimal.Decimal("3.56"))
        product1.set_category(food)

        product2 = Product()
        product2.set_name("tomato")
        product2.set_price(decimal.Decimal("4.65"))
        product2.set_category(food)

        productCatalog = InMemoryProductCatalog([product1, product2])
        self.use_case = OrderCreationUseCase(self.order_repository, productCatalog)

    def test_sell_multiple_items(self):
        salad_request = SellItemRequest()
        salad_request.set_product_name("salad")
        salad_request.set_quantity(2)

        tomato_request = SellItemRequest()
        tomato_request.set_product_name("tomato")
        tomato_request.set_quantity(3)

        request = SellItemsRequest()
        request.set_requests([salad_request, tomato_request])

        self.use_case.run(request)

        inserted_order = self.order_repository.get_saved_order()

        self.assertEqual(OrderStatus.CREATED, inserted_order.get_status())
        self.assertEqual(decimal.Decimal("23.20"), inserted_order.get_total())
        self.assertEqual(decimal.Decimal("2.13"), inserted_order.get_tax())
        self.assertEqual(decimal.Decimal("2.13"), inserted_order.get_tax())
        self.assertEqual("EUR", inserted_order.get_currency())
        self.assertEqual(2, len(inserted_order.get_items()))

        first_item = inserted_order.get_items()[0]
        self.assertEqual("salad", first_item.get_product().get_name())
        self.assertEqual(decimal.Decimal("3.56"), first_item.get_product().get_price())
        self.assertEqual(2, first_item.get_quantity())
        self.assertEqual(decimal.Decimal("7.84"), first_item.get_taxed_amount())
        self.assertEqual(decimal.Decimal("0.72"), first_item.get_tax())

        second_item = inserted_order.get_items()[1]
        self.assertEqual("tomato", second_item.get_product().get_name())
        self.assertEqual(decimal.Decimal("4.65"), second_item.get_product().get_price())
        self.assertEqual(3, second_item.get_quantity())
        self.assertEqual(decimal.Decimal("15.36"), second_item.get_taxed_amount())
        self.assertEqual(decimal.Decimal("1.41"), second_item.get_tax())

    def test_unknown_product(self):
        request = SellItemsRequest()
        request.set_requests([])
        unknown_product_request = SellItemRequest()
        unknown_product_request.set_product_name("unknown product")
        request.get_requests().append(unknown_product_request)

        with self.assertRaises(UnknownProductError):
            self.use_case.run(request)
