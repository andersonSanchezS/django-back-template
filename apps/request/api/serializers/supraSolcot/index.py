# Rest Framework
from rest_framework import serializers
# Models
from apps.request.models import SupraSolcot, Solcot
from apps.authentication.models import Users
from apps.misc.models import SubCategory
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException
# Utils
from apps.base.utils.index import ExtraFieldSerializer, parseDate
from apps.request.enums    import SolcotTypeEnum, SolcotStructureEnum
from apps.authentication.enums import RoleEnum
from apps.request.utils.index import getBuyer, genConsecutive

class SupraSolcotSerializer(serializers.ModelSerializer):
    solcots = ExtraFieldSerializer(source='*', required=True, error_messages={"required": "Los solcots son requeridos", "blank":"Los solcots son requeridos"})

    class Meta:
        model = SupraSolcot
        fields = '__all__'
        extra_kwargs = {
                        "solcots"        : { "error_messages": { "required": "Los solcots son requeridos", "blank":"Los solcots son requeridos" } },
                        "solcot_type"    : { "error_messages": { "required": "El tipo de solcot es requerido", "blank":"El tipo de solcot es requerido" } },
                        "client_email"   : { "error_messages": { "required": "El email del cliente es requerido", "blank":"El email del cliente es requerido" } },
                        "logistic_center": { "error_messages": { "required": "El centro logístico es requerido", "blank":"El centro logístico es requerido" } },
                        "shopping_group" : { "error_messages": { "required": "El grupo de compra es requerido", "blank":"El grupo de compra es requerido" } },
                        "purchase_organization": { "error_messages": { "required": "La organizacion de compra es requerida", "blank":"La organizacion de compra es requerida" } },
                        "category"       : { "error_messages": { "required": "La categoría es requerida", "blank": "La categoría es requerida" } },
                        }

    @transaction.atomic
    def create(self, validated_data):
        try:
            # create the supra solcot

            # Get the solcots from the validated data then delete it from the validated data
            solcots     = validated_data.pop('solcots')
            supraSolcot = SupraSolcot.objects.create(**validated_data)

            # Check the length of the solcots
            if len(solcots) == 0:
                raise HTTPException("Debe ingresar al menos un solcot", 400)
            for solcot in solcots:
                buyer = None
                
                # check if the solcot has the required fields
                requiredFields = SolcotStructureEnum.BASE.value
                for field in requiredFields:
                    if field not in solcot:
                        raise HTTPException(f"El campo {field} es requerido", 400)
                if validated_data['solcot_type'].id == SolcotTypeEnum.SERVICE.value or validated_data['solcot_type'].id == SolcotTypeEnum.MIXED.value:
                    if 'buyer' in solcot:
                        # check if the buyer exists and the role is buyer
                        buyer = Users.objects.filter(id=solcot['buyer'], role=RoleEnum.COMPRADOR.value, state=1).first()
                        if not buyer:
                            raise HTTPException("Este usuario no es un comprador", 400)
                    else:
                        buyer = getBuyer(validated_data['category'])

                    if buyer == None:
                        raise HTTPException("No hay compradores disponibles para esta categoría", 400)
                else:
                    buyer = getBuyer(validated_data['category'])

                # check if the solcot has a sub category
                try:
                    if 'sub_category' in solcot:
                        solcot['sub_category'] = SubCategory.objects.get(id=solcot['sub_category'])
                    else:
                        solcot['sub_category'] = None
                except SubCategory.DoesNotExist:
                    raise HTTPException("La sub categoría no existe", 400)
                
                # create the solcot
                solcotData = {
                    'consecutive'          : genConsecutive(),
                    'product'              : solcot['product'],
                    'quantity'             : solcot['quantity'],
                    'measurementUnit'      : solcot['measurementUnit'],
                    'budget'               : solcot['budget'],
                    'solcot_type'          : validated_data['solcot_type'],
                    'limit_date'           : parseDate(solcot['limit_date']),
                    'buyer'                : buyer,
                    'category'             : validated_data['category'],
                    'sub_category'         : solcot['sub_category'],
                    'shopping_group'       : validated_data['shopping_group'],
                    'purchase_organization': validated_data['purchase_organization'],
                    'logistic_center'      : validated_data['logistic_center'],
                    'supra_solcot'         : supraSolcot,
                    'user_created_at'      : validated_data['client'],
                    'is_unique_provider'   : solcot['is_unique_provider'] if 'is_unique_provider' in solcot else False,
                    'is_visit_required'    : solcot['is_visit_required'] if 'is_visit_required' in solcot else False,
                }

                # Save the solcot
                try:
                    Solcot.objects.create(**solcotData)
                except Exception as e:
                    raise HTTPException(str(e), 400)
            return supraSolcot
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
