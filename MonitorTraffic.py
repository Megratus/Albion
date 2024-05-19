from AlbiPy import sniffing_thread
from time import sleep
import datetime
import json

data = []
i = 1

#while i<6:

thread = sniffing_thread()
thread.start()

sleep(5)

thread.stop()
orders = thread.get_data()

data = json.loads(str(orders))


for order in orders:
    item = {"id": order.pk}
    for attribute in order.id:
        if attribute.feature == feature:
            item[attribute.attribute.name] = attribute.value
    data.append(item)

jsonData=json.dumps(data)


    #for order in orders:
    # data['ItemId'] =  
     #print(datetime.datetime.now(), order.Id, order.ItemTypeId, order.UnitPriceSilver , order.Amount, order.AuctionType)
   
    print("Data: ", i, data)
    i=i+1




