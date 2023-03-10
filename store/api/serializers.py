from base64 import b64encode
import zlib

def obj_to_dict(obj):
    # fields = obj.__dict__.items()
    fields = obj._meta.get_fields()
    obj_dict = {}

    for field in fields:
        field_Val = getattr(obj, field.name)

        # if field.get_internal_type() == "ForeignKey":
        #     continue
        if field.many_to_many:
            objects=[]
            for object in field_Val.values():
                related_dict = {}
                for key,val in object.items():
                    if key!='id':
                        related_dict[key]=val
                objects.append(related_dict)
            obj_dict[field.name] = objects

        # elif field.get_internal_type() == "FileField" and field_Val.width:
        #     with open(field_Val.path, "rb") as img:
        #         image_data = str(base64.b64encode(img.read()), "utf-8")
        #         # image_data = base64img.decode('utf-8')
        #         obj_dict[field.name] = image_data
        elif field.get_internal_type()=="BinaryField":
            compressed_img = zlib.compress(field_Val)
            obj_dict[field.name] =  b64encode(compressed_img).decode('utf8')
        else:
            obj_dict[field.name] = field_Val
    return obj_dict

