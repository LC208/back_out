from rest_framework.response import Response


def validate(model, request, field_name, index):
    model_selected = model.objects.filter(user = index)
    if model_selected.exists() and field_name in request.data:
        model_data = request.data.get(field_name)
        model.objects.filter(user = index).update(**model_data)
    elif not model_selected.exists() and field_name in request.data:
        return [False,Response( str(model)+" not found", status=404)]
    return [True,None]


class Utils:
    pass

