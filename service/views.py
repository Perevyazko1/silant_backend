import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import CustomUser
from .models import Machine, Maintenance, Complaint, MachineModelReference, EngineModelReference, \
    TransmissionModelReference, DrivingBridgeModelReference, ControlledBridgeModelReference,TypeOfMaintenanceReference,\
    RecoveryMethodReference,FailureNodeReference


@api_view(['GET'])
def get_machine_data(request):
    factory_number = request.GET['factory_number']
    try:
        machine = Machine.objects.get(factory_number=factory_number)
    except:
        return Response(status=status.HTTP_200_OK)

    result = {
        'factory_number': factory_number,
        'machine_model': machine.machine_model.name,
        'engine_model': machine.engine_model.name,
        'engine_number': machine.engine_number,
        'transmission_model': machine.transmission_model.name,
        'transmission_number': machine.transmission_number,
        'driving_bridge_model': machine.driving_bridge_model.name,
        'driving_bridge_number': machine.driving_bridge_number,
        'controlled_bridge_model': machine.controlled_bridge_model.name,
        'controlled_bridge_number': machine.controlled_bridge_number
    }
    try:
        if request.user == machine.client or request.user == machine.service_company or request.user.role == 'manager':
            authenticated_data = {
                'delivery_contract': machine.delivery_contract,
                'date_of_shipment': machine.date_of_shipment.strftime("%d.%m.%Y"),
                'consignee': machine.consignee,
                'delivery_address': machine.delivery_address,
                'complete_set': machine.complete_set,
                'client': machine.client.first_name,
                'service_company': machine.service_company.first_name,
            }
            result.update(authenticated_data)
        else:
            authenticated_data_forbidden_user = {
                'delivery_contract': 'Данные доступны для владельцев техники',
                'date_of_shipment': 'Данные доступны для владельцев техники',
                'consignee': 'Данные доступны для владельцев техники',
                'delivery_address': 'Данные доступны для владельцев техники',
                'complete_set': 'Данные доступны для владельцев техники',
                'client': 'Данные доступны для владельцев техники',
                'service_company': 'Данные доступны для владельцев техники',
            }

            result.update(authenticated_data_forbidden_user)

    except:
        authenticated_data_forbidden_user = {
            'delivery_contract': 'Данные доступны для владельцев техники',
            'date_of_shipment': 'Данные доступны для владельцев техники',
            'consignee': 'Данные доступны для владельцев техники',
            'delivery_address': 'Данные доступны для владельцев техники',
            'complete_set': 'Данные доступны для владельцев техники',
            'client': 'Данные доступны для владельцев техники',
            'service_company': 'Данные доступны для владельцев техники',
        }

        result.update(authenticated_data_forbidden_user)

    return Response(status=status.HTTP_200_OK, data=result)


@api_view(['POST'])
def post_machine_data(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа'})
    if request.user.role != 'manager':
        return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа'})
    try:
        factory_number = request.data['factory_number']
        machine_model = MachineModelReference.objects.get_or_create(name=request.data['machine_model'])[0]
        engine_model = EngineModelReference.objects.get_or_create(name=request.data['engine_model'])[0]
        engine_number = request.data['engine_number']
        transmission_model = TransmissionModelReference.objects.get_or_create(name=request.data['transmission_model'])[
            0]
        transmission_number = request.data['transmission_number']
        driving_bridge_model = \
        DrivingBridgeModelReference.objects.get_or_create(name=request.data['driving_bridge_model'])[0]
        driving_bridge_number = request.data['driving_bridge_number']
        controlled_bridge_model = \
        ControlledBridgeModelReference.objects.get_or_create(name=request.data['controlled_bridge_model'])[0]
        controlled_bridge_number = request.data['controlled_bridge_number']
        delivery_contract = request.data['delivery_contract']
        date_of_shipment = datetime.datetime.strptime(request.data['date_of_shipment'], "%d.%m.%Y")
        consignee = request.data['consignee']
        delivery_address = request.data['delivery_address']
        complete_set = request.data['complete_set']
        client = CustomUser.objects.get(first_name=request.data['client'])
        service_company = CustomUser.objects.get(first_name=request.data['service_company'])

        machine = Machine.objects.update_or_create(
            factory_number=factory_number,
            defaults={
                'machine_model': machine_model,
                'engine_model': engine_model,
                'engine_number': engine_number,
                'transmission_model': transmission_model,
                'transmission_number': transmission_number,
                'driving_bridge_model': driving_bridge_model,
                'driving_bridge_number': driving_bridge_number,
                'controlled_bridge_model': controlled_bridge_model,
                'controlled_bridge_number': controlled_bridge_number,
                'delivery_contract': delivery_contract,
                'date_of_shipment': date_of_shipment,
                'consignee': consignee,
                'delivery_address': delivery_address,
                'complete_set': complete_set,
                'client': client,
                'service_company': service_company,
            }
        )
    except Exception as e:
        print(e)
        result = f'Ошибка обновления данных машины, перепроверьте данные!'
        return Response(status=status.HTTP_200_OK, data={'result': result})

    if machine[1]:
        result = f'Успешно создана новая машина {factory_number}!'
    else:
        result = f'Успешно обновлены данные машины {factory_number}!'
    return Response(status=status.HTTP_200_OK, data={'result': result})


@api_view(['POST'])
def post_maintenance_data(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа'})
    if request.user.role != 'manager':
        return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа'})
    try:
        type_of_maintenance = TypeOfMaintenanceReference.objects.get_or_create(name=request.data['type_of_maintenance'])[0]
        date_of_maintenance = datetime.datetime.strptime(request.data['date_of_maintenance'], "%d.%m.%Y")
        operating_time = request.data['operating_time']
        order_number = request.data['order_number']
        order_date = datetime.datetime.strptime(request.data['order_date'], "%d.%m.%Y")
        machine = Machine.objects.get_or_create(factory_number=request.data['machine'])[0]

        maintenance = Maintenance.objects.update_or_create(
            order_number=order_number,
            defaults={
                'type_of_maintenance': type_of_maintenance,
                'date_of_maintenance': date_of_maintenance,
                'operating_time': operating_time,
                'order_date': order_date,
                'machine': machine,
            }
        )
    except Exception as e:
        print(e)
        result = f'Ошибка обновления данных ТО, перепроверьте данные!'
        return Response(status=status.HTTP_200_OK, data={'result': result})

    if maintenance[1]:
        result = f'Успешно создано новое ТО {order_number}!'
    else:
        result = f'Успешно обновлены данные ТО {order_number}!'
    return Response(status=status.HTTP_200_OK, data={'result': result})


@api_view(['POST'])
def post_complaints_data(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа'})
    if request.user.role != 'manager':
        return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа'})
    try:
        date_of_refusal = datetime.datetime.strptime(request.data['date_of_refusal'], "%d.%m.%Y")
        operating_time = request.data['operating_time']
        failure_node = FailureNodeReference.objects.get_or_create(name=request.data['failure_node'])[0]
        failure_description = request.data['failure_description']
        recovery_method = RecoveryMethodReference.objects.get_or_create(name=request.data['recovery_method'])[0]
        parts_used = request.data['parts_used']
        date_of_restoration = datetime.datetime.strptime(request.data['date_of_restoration'], "%d.%m.%Y")
        equipment_downtime = request.data['equipment_downtime']
        machine = Machine.objects.get_or_create(factory_number=request.data['machine'])[0]


        maintenance = Complaint.objects.update_or_create(
            failure_description=failure_description,
            defaults={
                'date_of_refusal': date_of_refusal,
                'operating_time': operating_time,
                'failure_node': failure_node,
                'recovery_method': recovery_method,
                'parts_used': parts_used,
                'date_of_restoration': date_of_restoration,
                'equipment_downtime': equipment_downtime,
                'machine': machine})
    except Exception as e:
        print(e)
        result = f'Ошибка обновления данных рекламации, перепроверьте данные!'
        return Response(status=status.HTTP_200_OK, data={'result': result})

    if maintenance[1]:
        result = f'Успешно создано новая рекламация {failure_description}!'
    else:
        result = f'Успешно обновлена рекламация {failure_description}!'
    return Response(status=status.HTTP_200_OK, data={'result': result})


@api_view(['GET'])
def get_machine_list(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_200_OK, data={'result': 'ошибка доступа'})
    factory_number_filer = request.GET['factory_number']
    machine_model_filer = request.GET['machine_model']
    engine_model_filer = request.GET['engine_model']
    transmission_model_filer = request.GET['transmission_model']
    driving_bridge_model_filer = request.GET['driving_bridge_model']
    controlled_bridge_model = request.GET['controlled_bridge_model']

    machine_list = Machine.objects.all()

    if factory_number_filer != "":
        machine_list = machine_list.filter(factory_number__contains=factory_number_filer)

    if machine_model_filer != "Все модели":
        machine_list = machine_list.filter(machine_model__name=machine_model_filer)

    if engine_model_filer != "Все модели":
        machine_list = machine_list.filter(engine_model__name=engine_model_filer)

    if transmission_model_filer != "Все модели":
        machine_list = machine_list.filter(transmission_model__name=transmission_model_filer)

    if driving_bridge_model_filer != "Все модели":
        machine_list = machine_list.filter(driving_bridge_model__name=driving_bridge_model_filer)

    if controlled_bridge_model != "Все модели":
        machine_list = machine_list.filter(controlled_bridge_model__name=controlled_bridge_model)

    data = {
        'machine_list_data': machine_list.values(
            'id',
            'factory_number',
            'machine_model__name',
            'engine_model__name',
            'transmission_model__name',
            'driving_bridge_model__name',
            'controlled_bridge_model__name'
        ),
        'filter_data': {
            'machine_models': MachineModelReference.objects.all().values('name'),
            'engine_models': EngineModelReference.objects.all().values('name'),
            'transmission_models': TransmissionModelReference.objects.all().values('name'),
            'driving_bridge_models': DrivingBridgeModelReference.objects.all().values('name'),
            'controlled_bridge_models': ControlledBridgeModelReference.objects.all().values('name'),
        },
        'users_data': CustomUser.objects.filter(role="client").values('first_name'),
        'services_data': CustomUser.objects.filter(role="service_organisation").values('first_name'),
    }

    return Response(status=status.HTTP_200_OK, data=data)


@api_view(['GET'])
def get_maintenance(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа'})
    # print(request.user.username)
    # if request.user.role != 'service_organisation' and request.user.role != 'manager':
    #     return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа роли'})
    factory_number = request.GET['factory_number']
    maintenances = Maintenance.objects.filter(machine__factory_number=factory_number)
    result = []
    for maintenance in maintenances:
        if maintenance.machine.service_company == request.user or maintenance.machine.client == request.user or request.user.role == 'manager':
            result = {
                'id': maintenance.id,
                'type_of_maintenance': maintenance.type_of_maintenance.name,
                'date_of_maintenance': maintenance.date_of_maintenance.strftime("%d.%m.%Y"),
                'operating_time': maintenance.operating_time,
                'order_number': maintenance.order_number,
                'order_date': maintenance.order_date.strftime("%d.%m.%Y"),
                'machine': maintenance.machine.factory_number,
                'select_data':{
                    'machine': Machine.objects.all().values('factory_number'),
                    'type_maintenance': TypeOfMaintenanceReference.objects.all().values('name')

                }
            }

        else:
            result = {
                'id': "Данные Вам недоступны",
                'type_of_maintenance': "Данные Вам недоступны",
                'date_of_maintenance': "Данные Вам недоступны",
                'operating_time': "Данные Вам недоступны",
                'order_number': "Данные Вам недоступны",
                'order_date': "Данные Вам недоступны",
                'machine': "Данные Вам недоступны",
                'select_data': {
                    'machine': Machine.objects.all().values('factory_number'),
                    'type_maintenance': TypeOfMaintenanceReference.objects.all().values('name')

                }

            }

    return Response(status=status.HTTP_200_OK, data=result)


@api_view(['GET'])
def get_complaints(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа'})
    # if request.user.role != 'service_organisation' or request.user.role != 'manager':
    #     Response(status=status.HTTP_200_OK, data={'result': 'Ошибка доступа роли'})
    factory_number = request.GET['factory_number']
    complaints = Complaint.objects.filter(machine__factory_number=factory_number)
    result = {}
    for complaint in complaints:
        if complaint.machine.service_company == request.user or complaint.machine.client == request.user or request.user.role == 'manager':
            result = {
                    'id': complaint.id,
                    'date_of_refusal': complaint.date_of_refusal.strftime("%d.%m.%Y"),
                    'operating_time': complaint.operating_time,
                    'failure_node': complaint.failure_node.name,
                    'failure_description': complaint.failure_description,
                    'recovery_method': complaint.failure_description,
                    'parts_used': complaint.parts_used,
                    'date_of_restoration': complaint.date_of_restoration.strftime("%d.%m.%Y"),
                    'equipment_downtime': complaint.equipment_downtime,
                    'machine': complaint.machine.factory_number,
                    'select_data':{
                        'machine': Machine.objects.all().values('factory_number'),
                        'failure_node': FailureNodeReference.objects.all().values('name'),
                        'recovery_method': RecoveryMethodReference.objects.all().values('name')
                    }

            }
        else:
            result = {
                'id': "Данные Вам недоступны",
                'date_of_refusal': "Данные Вам недоступны",
                'operating_time': "Данные Вам недоступны",
                'failure_node': "Данные Вам недоступны",
                'failure_description': "Данные Вам недоступны",
                'recovery_method': "Данные Вам недоступны",
                'parts_used': "Данные Вам недоступны",
                'date_of_restoration': "Данные Вам недоступны",
                'get_equipment_downtime': "Данные Вам недоступны",
                'machine': "Данные Вам недоступны",
                'select_data': {
                    'machine': Machine.objects.all().values('factory_number'),
                    'failure_node': FailureNodeReference.objects.all().values('name'),
                    'recovery_method': RecoveryMethodReference.objects.all().values('name')
                }

            }
            print(result)
    return Response(status=status.HTTP_200_OK, data=result)
