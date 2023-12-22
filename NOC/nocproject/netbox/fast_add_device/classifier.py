




import pynetbox
from .my_pass import netbox_url,netbox_api_token


def classifier_device_type(man_name,model):

    nb = pynetbox.api(url=netbox_url,token=netbox_api_token)
    nb.http_session.verify = False
    try:
        d_type_name = nb.dcim.device_types.get(model=model)
        d_type_id = int(d_type_name.id)
        return d_type_id
    except Exception as err:
        print(err)
        try:
            device_type = nb.dcim.manufacturers.get(name=man_name)
            man_id = device_type.id
            model_slug = model.replace(" ", "-")
            create = nb.dcim.device_types.create(
                manufacturer=man_id,
                model=model,
                slug=model_slug.title()
            )
            device_type_name = nb.dcim.device_types.get(model=model)
            result_id = int(device_type_name.id)
            return result_id


        except pynetbox.core.query.RequestError as err:
            print(err)




