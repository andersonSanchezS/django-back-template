# Rest Framework
from rest_framework import serializers
# Models
from apps.authentication.models import Users
from django.db import transaction
# Utils
from apps.base.utils.index import genPassword
import random
from apps.authentication.enums import RoleEnum
import bcrypt
# Exceptions
from apps.base.exceptions import HTTPException

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {
            "email": { "error_messages": { "required": "El correo es requerido" } },
            "phone_number":{ "error_messages": { "required": "El numero de teléfono es requerido" }},
            "first_name": { "error_messages": { "required": "El nombre es requerido" }},
            "last_name": { "error_messages": { "required": "El apellido es requerido" }},
            "type_document": { "error_messages": { "required": "El tipo de documento es requerido" }},
            "document_number": { "error_messages": { "required": "El número de documento es requerido" }},
            }

    @transaction.atomic
    def create(self, validated_data):
        try:            
            # Generate a random password
            password = genPassword(10) if 'password' not in validated_data else validated_data['password']
            validated_data['password'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
            # Generate an username
            validated_data['username'] = validated_data['first_name'] +'.'+validated_data['last_name'] 

            # check if the email has petromil domain next to the @
            if '@petromil' not in validated_data['email']:
                pass
            else:
                validated_data['is_ldap_user'] = True
            
            # check if the username is unique
            exists = True

            while exists:
                exists = Users.objects.filter(username=validated_data['username']).exists()
                if exists:
                    validated_data['username'] = validated_data['username'] + random.choice('1234567890')
                else:
                    break
                
            rolesData = validated_data.pop('roles', None)
            customPermissionsData = validated_data.pop('custom_permissions', None)
            categoriesData = validated_data.pop('categories', None)

            # check if the role are different from administrador
            if not rolesData:
                raise HTTPException('El rol es requerido', 400)
            
            if RoleEnum.ADMINISTRADOR.value and RoleEnum.SUPERVISOR.value not in rolesData and len(categoriesData) == 0:
                raise HTTPException('Los usuarios con este rol requieren categorías', 400)
            
            user = Users.objects.create(**validated_data)
            # set the roles 
            if rolesData:
                user.roles.set(rolesData)
            else:
                raise HTTPException('El rol es requerido', 400)
            
            if customPermissionsData:
                user.custom_permissions.set(customPermissionsData)

            if categoriesData:
                user.categories.set(categoriesData)
            # send the password to the user
                
            return user
        except Exception as e:
            raise HTTPException(str(e), 500)
        
    @transaction.atomic
    def update(self, instance, validated_data):
        try:            
            # exclude the roles and custom permissions from the validated data
            rolesData = validated_data.pop('roles', None)
            customPermissionsData = validated_data.pop('custom_permissions', None)
            categoriesData = validated_data.pop('categories', None)

            # update the user

            if rolesData:
                instance.roles.set(rolesData)

            if customPermissionsData:
                instance.custom_permissions.set(customPermissionsData)

            if categoriesData:
                instance.categories.set(categoriesData)

            return super().update(instance, validated_data)
        except Exception as e:
            raise HTTPException(e.message, e.status_code)
        