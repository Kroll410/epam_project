from init import db
from inspect import getmembers

TYPES = {
    'Long Text': db.Column(db.String(255)),
    'Text': db.Column(db.String(45)),
    'Float': db.Column(db.Float()),
    'Integer': db.Column(db.Integer()),
    'Boolean': db.Column(db.Boolean()),
    'DATE': db.Column(db.Date()),
}


def class_factory(_metadata: dict, base=db.Model, with_id=True):

    _metadata = dict(_metadata)
    print(_metadata)
    table_name = _metadata.pop('table-name')

    f_class_attributes = {}
    if with_id:
        f_class_attributes.update({
            'id': db.Column(db.Integer, primary_key=True)
        })

    prev_pair = None
    for i, f_pair in enumerate(_metadata.items()):
        if i % 2 == 0:
            prev_pair = f_pair
            continue

        _, val = prev_pair
        _, val_type = f_pair

        try:
            datatype = TYPES[val_type]
        except KeyError:
            raise KeyError('Invalid data was entered')

        f_class_attributes.update({
            val: datatype
        })
    else:
        f_class_attributes.update({
            'uuid': db.Column(db.String(36), unique=True)
        })

    def __init__(self, **kwargs):
        base.__init__(self, self.__tablename__)
        class_attributes = [x[0] for x in getmembers(self.__class__) if
                            not (x[0].startswith('__') and x[0].endswith('__'))]

        if [x[0] for x in kwargs] == class_attributes:
            for pair, class_attr in zip(kwargs.items(), class_attributes):
                curr_init_attr, curr_init_value = pair
                setattr(self, class_attr, curr_init_value)
        else:
            raise KeyError('Invalid data was entered')

    def __repr__(self):
        return f'{self.__tablename__}'

    new_class = type(table_name, (base,), dict({
        "__init__": __init__,
        '__tablename__': table_name,

        '__repr__': __repr__,
    }, **f_class_attributes))

    return new_class
