from GlobalSerializer import GlobalSerializer
import hazelcast
from ECommerceDataHazelcast import ECommerceDataHazelcast
from hazelcast.proxy.reliable_topic import ReliableMessageListener


class MyMessageListener(ReliableMessageListener):
  def retrieve_initial_sequence(self):
    print('retrieve_initial_sequence')
    return -1
  def ZZZZZZZZZ_on_message(m):
    print('on_message')
    pass
      
print('olá mundo')
ecommerce_data = ECommerceDataHazelcast()
ecommerce_data.start()

listener = MyMessageListener()
ecommerce_data.register_listener(listener)
print(18)
while True:
  pass
ecommerce_data.shutdown()
