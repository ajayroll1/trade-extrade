import json
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from myapp.consumers import TradeConsumer

class TradeConsumerTests(TestCase):
    async def test_trade_consumer(self):
        communicator = WebsocketCommunicator(TradeConsumer.as_asgi(), "/ws/trades/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Test sending a message
        test_message = {
            "type": "trade",
            "data": {
                "symbol": "BTC/USD",
                "price": 50000,
                "quantity": 0.1
            }
        }
        await communicator.send_json_to(test_message)
        
        # Test receiving a message
        response = await communicator.receive_json_from()
        self.assertEqual(response["type"], "trade")
        self.assertEqual(response["data"]["symbol"], "BTC/USD")
        
        await communicator.disconnect() 