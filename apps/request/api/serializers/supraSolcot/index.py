# Rest Framework
from rest_framework import serializers
# Models
from apps.request.models import SupraSolcot, Solcot, SolcotType
from apps.authentication.models import Users
from django.db import transaction
# Exceptions
from apps.base.exceptions import HTTPException
# Utils
from apps.base.utils.index import ExtraFieldSerializer
from apps.request.enums    import SolcotTypeEnum, SolcotStructureEnum, ProcessStateEnum
from apps.authentication.enums import RoleEnum
from apps.request.utils.index import getBuyer, genConsecutive, getWorkDay

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
            globalBuyer = None
            
            # Get the solcots from the validated data then delete it from the validated data
            solcots     = validated_data.pop('solcots')
            supraSolcot = SupraSolcot.objects.create(**validated_data)

            # Check the length of the solcots
            if len(solcots) == 0:
                raise HTTPException("Debe ingresar al menos un solcot", 400)

            for solcot in solcots:
                selectedBuyer = None

                is_service_or_mixed = validated_data['solcot_type'].id in [SolcotTypeEnum.SERVICE.value, SolcotTypeEnum.MIXED.value]
                
                if is_service_or_mixed:
                    globalBuyer = getBuyer(validated_data['category'])
                elif 'buyer' in solcot and solcot['buyer'] is not None:
                    selectedBuyer = Users.objects.filter(id=solcot['buyer'], roles__in=RoleEnum.COMPRADOR.value, state=1).first()
                    if not selectedBuyer:
                        raise HTTPException("El comprador no existe", 400)
                else:
                    selectedBuyer = getBuyer(validated_data['category'])


                # check if the solcot has the required fields
                requiredFields = SolcotStructureEnum.BASE.value
                for field in requiredFields:
                    if field not in solcot:
                        raise HTTPException(f"El campo {field} es requerido", 400)

                solcotTypeInstance = SolcotType.objects.get(pk=solcot['solcot_type'])
                
                # calc the limit date
                solcot['limit_date'] = getWorkDay(solcotTypeInstance).date()
                # create the solcot
                solcotData = {
                    'consecutive'          : genConsecutive(),
                    'product'              : solcot['product'],
                    'quantity'             : solcot['quantity'],
                    'measurementUnit'      : solcot['measurementUnit'],
                    'budget'               : solcot['budget'],
                    'solcot_type'          : solcotTypeInstance,
                    'limit_date'           : solcot['limit_date'],
                    'buyer'                : globalBuyer if is_service_or_mixed else selectedBuyer,
                    'category'             : validated_data['category'],
                    'shopping_group'       : validated_data['shopping_group'],
                    'purchase_organization': validated_data['purchase_organization'],
                    'logistic_center'      : validated_data['logistic_center'],
                    'supra_solcot'         : supraSolcot,
                    'user_created_at'      : validated_data['user_created_at'],
                    'is_unique_provider'   : solcot['is_unique_provider'] if 'is_unique_provider' in solcot else False,
                    'is_visit_required'    : solcot['is_visit_required'] if 'is_visit_required' in solcot else False,
                }
                # Save the solcot
                try:
                    createSolcot = Solcot.objects.create(**solcotData)
                    # set the subcategories
                    if 'sub_categories' in solcot:
                        createSolcot.sub_categories.set(solcot['sub_categories'])
                except Exception as e:
                    raise HTTPException(str(e), 400)
            return supraSolcot
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            # Validate the state of the supra solcot
            if instance.process_state != ProcessStateEnum.PENDING.value:
                raise HTTPException("No se puede modificar una supra solcot que no esté en estado pendiente", 400)
            
            globalBuyer = None                    
            # get the solcots from the validated data then delete it from the validated data
            solcots = validated_data.pop('solcots')

            # Check the length of the solcots
            if len(solcots) == 0:
                raise HTTPException("Debe ingresar al menos un solcot", 400)
            
            for solcot in solcots:
                typeSolcotInstance = SolcotType.objects.get(id=solcot['solcot_type'])
                # update the limit date
                solcot['limit_date'] = getWorkDay(typeSolcotInstance).date()
                
                # if the solcot has an id check if it exists
                if 'id' in solcot:
                    solcotInstance = Solcot.objects.filter(id=solcot['id']).first()

                    if not solcotInstance:
                        raise HTTPException(f"El solcot con id {solcot['id']} no existe", 400)
                    
                    # check if the solcot has the required fields
                    requiredFields = SolcotStructureEnum.BASE.value
                    for field in requiredFields:
                        if field not in solcot:
                            raise HTTPException(f"El campo {field} es requerido", 400)
                    
                    # update the solcot
                    solcotInstance.buyer            = Users.objects.filter(id=solcot['buyer']).first() if 'buyer' in solcot and solcot['buyer'] is not None else solcotInstance.buyer
                    solcotInstance.product          = solcot['product']
                    solcotInstance.quantity         = solcot['quantity']
                    solcotInstance.measurementUnit  = solcot['measurementUnit']
                    solcotInstance.budget           = solcot['budget']
                    solcotInstance.solcot_type      = typeSolcotInstance
                    solcotInstance.specification    = solcot['specification'] if 'specification' in solcot else None
                    solcotInstance.description      = solcot['description'] if 'description' in solcot else None
                    solcotInstance.limit_date       = solcot['limit_date']
                    solcotInstance.contract_manager = solcot['contract_manager']
                    solcotInstance.category         = validated_data['category']
                    solcotInstance.sub_categories.set(solcot['sub_categories']) if 'sub_categories' in solcot else solcotInstance.sub_categories.set([])
                    solcotInstance.shopping_group        = validated_data['shopping_group']
                    solcotInstance.purchase_organization = validated_data['purchase_organization']
                    solcotInstance.logistic_center       = validated_data['logistic_center']
                    solcotInstance.is_unique_provider    = solcot['is_unique_provider'] if 'is_unique_provider' in solcot else False
                    solcotInstance.is_visit_required     = solcot['is_visit_required'] if 'is_visit_required' in solcot else False
                    solcotInstance.user_updated_at       = validated_data['user_updated_at']
                    solcotInstance.save()
                else:
                    is_service_or_mixed = validated_data['solcot_type'].id in [SolcotTypeEnum.SERVICE.value, SolcotTypeEnum.MIXED.value]

                    if is_service_or_mixed:
                        # check for other solcots with the same supra solcot
                        solcots = Solcot.objects.filter(supra_solcot=instance)
                        if solcots.count() > 0:
                            globalBuyer = solcots.first().buyer
                        else:
                            globalBuyer = getBuyer(validated_data['category'])
                    elif 'buyer' in solcot and solcot['buyer'] is not None:
                        selectedBuyer = Users.objects.filter(id=solcot['buyer'], roles__in=RoleEnum.COMPRADOR.value, state=1).first()
                        if not selectedBuyer:
                            raise HTTPException("El comprador no existe", 400)
                    else:
                        selectedBuyer = getBuyer(validated_data['category'])
                    solcotData = {
                    'consecutive'          : genConsecutive(),
                    'product'              : solcot['product'],
                    'quantity'             : solcot['quantity'],
                    'measurementUnit'      : solcot['measurementUnit'],
                    'budget'               : solcot['budget'],
                    'solcot_type'          : typeSolcotInstance,
                    'limit_date'           : getWorkDay(typeSolcotInstance).date(),
                    'buyer'                : globalBuyer if is_service_or_mixed else selectedBuyer,
                    'category'             : validated_data['category'],
                    'shopping_group'       : validated_data['shopping_group'],
                    'purchase_organization': validated_data['purchase_organization'],
                    'logistic_center'      : validated_data['logistic_center'],
                    'supra_solcot'         : instance,
                    'user_created_at'      : validated_data['user_updated_at'],
                    'is_unique_provider'   : solcot['is_unique_provider'] if 'is_unique_provider' in solcot else False,
                    'is_visit_required'    : solcot['is_visit_required'] if 'is_visit_required' in solcot else False,
                    }

                    # Save the solcot
                    try:
                        createSolcot = Solcot.objects.create(**solcotData)
                        # set the subcategories
                        if 'sub_categories' in solcot:
                            createSolcot.sub_categories.set(solcot['sub_categories'])
                    except Exception as e:
                        raise HTTPException(str(e), 400)

            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(str(e), 400)
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # get the solcots from the supra solcot
        solcots = Solcot.objects.filter(supra_solcot=instance)
        representation['solcots'] = [{
            'id'                       : solcot.id,
            'consecutive'              : solcot.consecutive,
            'product'                  : solcot.product,
            'quantity'                 : solcot.quantity,
            'measurementUnit'          : solcot.measurementUnit,
            'budget'                   : solcot.budget,
            'solcot_type'              : solcot.solcot_type.description,
            'solcot_type_id'           : solcot.solcot_type.id,
            'limit_date'               : solcot.limit_date,
            'buyer'                    : solcot.buyer.first_name + " " + solcot.buyer.last_name if solcot.buyer else None,
            'buyer_id'                 : solcot.buyer.id if solcot.buyer else None,
            'category'                 : solcot.category.description,
            'category_id'              : solcot.category.id,
            'sub_categories'           : [{'description': subCategory.description, 'id':subCategory.id} for subCategory in solcot.sub_categories.all()],
            'shopping_group'           : solcot.shopping_group.description,
            'shopping_group_id'        : solcot.shopping_group.id,
            'purchase_organization'    : solcot.purchase_organization.description,
            'purchase_organization_id' : solcot.purchase_organization.id,
            'logistic_center'          : solcot.logistic_center.description,
            'logistic_center_id'       : solcot.logistic_center.id,
            'is_unique_provider'       : solcot.is_unique_provider,
            'is_visit_required'        : solcot.is_visit_required,
            'user_created_at'          : solcot.user_created_at.first_name + " " + solcot.user_created_at.last_name,
            'user_created_at_id'       : solcot.user_created_at.id,
            'created_at'               : solcot.created_at,
            'updated_at'               : solcot.updated_at,
            'is_viewed_by_buyer'       : solcot.is_viewed_by_buyer,
            'accepted_at'              : solcot.accepted_at,
            'finished_at'              : solcot.finished_at,
            'process_state'            : solcot.process_state,
            'is_unique_provider'       : solcot.is_unique_provider,
            'is_visit_required'        : solcot.is_visit_required,
            'contract_manager'         : solcot.contract_manager,
            'solpet_code'              : solcot.solpet_code,
            'global_administration'    : solcot.global_administration,
            'global_utility'           : solcot.global_utility,
            'global_contingencies'     : solcot.global_contingencies,
            'specification'            : solcot.specification,
            'description'              : solcot.description,
        } for solcot in solcots] 
        return representation
