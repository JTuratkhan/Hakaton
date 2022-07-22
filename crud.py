import json


def main():
    print('1)Objektti jaratuu\n2)Maalymatty karoo\n3)Tak maalymatty karoo\n4)Objektti ozgortuu\n5)Objektti jok kyluu\n6)Avtounaaga like basuu\n7)Avtounaaga kommentariy jazuu\n8)Jumushtuu buturuu ')    
    try:
        a=int(input('Teiloonu tandagyla'))
        if a == 1:
            brand=input('Markasy:')
            model=input('Modeli:')
            year=int(input('Jyly:'))
            volume=input('Obyomu:')
            color=input('Onu:')
            body=int(input('Kuzovtun turu\n1-Sedan\n2-Universal\n3-Kupe\n4-Hatchback\n5-Minivan\n6-Vnedorojnik\n7-Pickup\n'))
            if body==1:
                body='Sedan'
            elif body==2:
                body='Universal'
            elif body==3:
                body='Kupe'
            elif body==4:
                body='Hatchback'
            elif body==5:
                body='Minivan'
            elif body==6:
                body='Vnedorojnik'
            elif body==7:
                body='Pickup'
            mileage=int(input('Probeg:'))
            price=int(input('Baasy:'))
            Cars().create(brand, model, year, volume,color, body, mileage, price)
            main()
        elif a == 2 :
            print(Cars.listing())
            main()
        elif a == 3:
            object=int(input('Objekttin indexin kirgizgile: '))
            print(Cars.retrieve(object))
            main()
        elif a == 4:
            object=int(input('Objekttin indexin kirgizgile: '))
            kwargs={}
            obj=input('Objekttin indexin kirgizgile: ')
            val=input('Kaisyga almashtyrgynyz kelip jatat: ')
            kwargs[obj]=val
            Cars().update_car(object, **kwargs)
            main()
        elif a == 5 :
            object=int(input('Objekttin indexin kirgizgile: '))
            Cars().delete_car(object)
            main()

        elif a == 6:
            id = int(input('Objekttin indexin kirgizgile: '))
            Cars().like_(id)
            main()
        elif a==7:
            id=int(input('Objekttin indexin kirgizgile: '))
            kwargs = {}
            com = input('komment')
            kwargs['coment'] = com
            Cars().coments(id, **kwargs)
            main()

        elif a == 8:
            print('Teiloo buttu!')
    except:
        print('Maalymat tuura berilgen emes!')
        main()


class Cars:
    FILE='jsondb/auto.json'
    id=0
    coment=None
    like=0

    def create(self, brand, model, year, volume,color, body, mileage, price):
        self.brand=brand
        self.model=model
        self.year=year
        self.volume=volume
        self.color=color
        self.body=body
        self.milage=mileage
        self.price=price
        self.send_cars_to_json()
    
    @classmethod
    def get_id(cls):
        cls.id+=1
        return cls.id     
    @classmethod
    def listing(cls):
        with open(cls.FILE) as file:
            return json.load(file)
    @staticmethod
    def get_one_car(auto,id):
        car= list(filter(lambda x : x['id']==id , auto))
        if not car:
            return('Myndai produkt jok')
        return car[0]


    @classmethod
    def send_auto_to_json(cls, auto):
        with open(Cars.FILE, 'w') as file:
            json.dump(auto, file)

    def send_cars_to_json(self):
        auto=Cars.listing()
        car={
            'id':Cars.get_id(),
            'Markasy':self.brand,
            'Modeli':self.model,
            'Jyly':self.year,
            'Obyomu':self.volume,
            'Onu':self.color,
            'Kuzovtun turu':self.body,
            'Probeg':self.milage,
            'Baasy':self.price,

        }
        auto.append(car)
         
        with open(Cars.FILE, 'w') as file:
            json.dump(auto, file)

        return{'satus':'201', 'msg':'car'}

    @classmethod
    def retrieve(cls,id):
        auto = cls.listing()
        car=cls.get_one_car(auto, id)
        return car


    @classmethod
    def update_car(cls,id, **kwargs):
        data=cls.listing()
        car = cls.get_one_car(data,id)
        index = data.index(car)
        data[index].update(**kwargs)
        cls.send_auto_to_json(data)
        return{'status':'200','msg':'Updated'}
    @classmethod
    def delete_car(cls,id):
        data=cls.listing()
        car=cls.get_one_car(data,id)
        if type(car)!=dict:
            return car
        index=data.index(car)
        data.pop(index)
        cls.send_auto_to_json(data)
        print({'status':'204','msg':'Deleted'})
    @classmethod
    def like_(cls, id):
        data = cls.listing()
        car = cls.get_one_car(data,id)
        index = data.index(car)
        data[index].update(like = 1)
        cls.send_auto_to_json(data)
        return {'status':'200','msg':'liked'}

    @classmethod
    def dislike(cls, id):
        data = cls.listing()
        car = cls.get_one_car(data,id)
        index = data.index(car)
        data[index].update(like = 0)
        cls.send_auto_to_json(data)
        return {'status':'200','msg':'disliked'}

    @classmethod
    def coments(cls,id, **kwargs ):
        data=cls.listing()
        car = cls.get_one_car(data,id)
        index = data.index(car)
        data[index].update(**kwargs)
        cls.send_auto_to_json(data)
        return{'status':'200','msg':'comented'}

    with open (FILE, 'w')as file :
        json.dump([],file)

main()