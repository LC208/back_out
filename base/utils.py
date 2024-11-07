from rest_framework.response import Response


def validate(model, request, field_name, **filters):
    model_selected = model.objects.filter(**filters)
    if model_selected.exists() and field_name in request.data:
        model_data = request.data.get(field_name)
        model.objects.filter(**filters).update(**model_data)
    elif not model_selected.exists() and field_name in request.data:
        return Response( str(model)+" not found", status=404)
    elif field_name not in request.data:
        return None
    return [model,*filters,model_data]

def model_update(data):
    if data is None:
        return
    data[0].objects.filter(*data[1]).update(**data[2])

class Utils:
    pass

