import json


def main():
    print('1)Объектти жаратуу\n2)Маалыматты кароо\n3)Так маалыматты кароо\n4)Объектти озгортуу\n5)Объектти жок кылуу\n6)Автоунаага лайк басуу\n7)Автоунаага комментарий жазуу\n8)Жумушту бутуруу ')    
    try:
        a=int(input('Тейлоону тандагыла:'))
        if a == 1:
            brand=input('Маркасы:')
            model=input('Модели:')
            year=int(input('Жылы:'))
            volume=input('Объёму:')
            color=input('Ону:')
            body=int(input('Кузовтун туру:\n1-Седан\n2-Универсал\n3-Купе\n4-Хэтчбек\n5-Минивен\n6-Внедорожник\n7-Пикап\n'))
            if body==1:
                body='Седан'
            elif body==2:
                body='Универсал'
            elif body==3:
                body='Купе'
            elif body==4:
                body='Хэтчбек'
            elif body==5:
                body='Минивен'
            elif body==6:
                body='Внедорожник'
            elif body==7:
                body='Пикап'
            mileage=int(input('Пробег:'))
            price=int(input('Баасы:'))
            Cars().create(brand, model, year, volume,color, body, mileage, price)
            main()
        elif a == 2 :
            print(Cars.listing())
            main()
        elif a == 3:
            object=int(input('Объекттин индексин киргизгиле:'))
            print(Cars.retrieve(object))
            main()
        elif a == 4:
            object=int(input('Объекттин индексин киргизгиле:'))
            kwargs={}
            obj=input('Объекттин индексин киргизгиле:')
            val=input('Кайсыга алмаштыргыныз келип жатат:')
            kwargs[obj]=val
            Cars().update_car(object, **kwargs)
            main()
        elif a == 5 :
            object=int(input('Объекттин индексин киргизгиле:'))
            Cars().delete_car(object)
            main()

        elif a == 6:
            id = int(input('Объекттин индексин киргизгиле:'))
            Cars().like_(id)
            main()
        elif a==7:
            id=int(input('Объекттин индексин киргизгиле:'))
            kwargs = {}
            com = input('Коммент: ')
            kwargs['coment'] = com
            Cars().coments(id, **kwargs)
            main()

        elif a == 8:
            print('Тейлоо бутту!')
    except:
        print('Маалымат туура берилген эмес!')
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
            return('Мындай продукт жок ')
        return car[0]


    @classmethod
    def send_auto_to_json(cls, auto):
        with open(Cars.FILE, 'w') as file:
            json.dump(auto, file)

    def send_cars_to_json(self):
        auto=Cars.listing()
        car={
            'id':Cars.get_id(),
            'Маркасы':self.brand,
            'Модели':self.model,
            'Жылы':self.year,
            'Объёму':self.volume,
            'Ону':self.color,
            'Кузовтун туру':self.body,
            'Пробег':self.milage,
            'Баасы':self.price,

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