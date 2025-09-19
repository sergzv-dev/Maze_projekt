class MyObject:
    def to_json(self):
        data = self.__dict__.copy()
        for key in data:
            value = data[key]
            if hasattr(value, 'to_json'):
                data[key] = value.to_json()
        data.update({'cls': self.__class__.__name__})
        return data