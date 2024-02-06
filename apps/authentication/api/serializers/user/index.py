# Rest Framework
from rest_framework import serializers
# Models
from apps.authentication.models import Users
from django.db import transaction
# Utils
from apps.base.utils.index import genPassword
import random

import bcrypt
# Exceptions
from apps.base.exceptions import HTTPException

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {"email": { "error_messages": { "required": "El correo es requerido" } },
                        "phone_number":{ "error_messages": { "required": "El numero de teléfono es requerido" }} }

    @transaction.atomic
    def create(self, validated_data):
        try:
            # validate if description is empty and first_name and last_name are not
            isNaturalPerson = validated_data['first_name'] != "" or validated_data['last_name'] != ""
            if not isNaturalPerson and validated_data['description'] == "":
                raise HTTPException('La razón social es requerida', 400)
            elif isNaturalPerson and (validated_data['first_name'] == "" or validated_data['last_name'] == "") :
                raise HTTPException('El nombre y apellido son requeridos', 400)
            
            # Generate a random password
            password = genPassword(10) if 'password' not in validated_data else validated_data['password']
            validated_data['password'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
            # Generate an username
            validated_data['username'] = validated_data['first_name'] +'.'+validated_data['last_name'] if isNaturalPerson else None
            # check if the username is unique
            exists = True

            while exists:
                if validated_data['username'] is None:
                    break
                exists = Users.objects.filter(username=validated_data['username']).exists()
                if exists:
                    validated_data['username'] = validated_data['username'] + random.choice('1234567890')
                else:
                    break
                
            rolesData = validated_data.pop('roles', None)
            customPermissionsData = validated_data.pop('custom_permissions', None)

            user = Users.objects.create(**validated_data)
            # set the roles 
            if rolesData:
                user.roles.set(rolesData)
            else:
                raise HTTPException('El rol es requerido', 400)
            
            if customPermissionsData:
                user.custom_permissions.set(customPermissionsData)

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

            # update the user
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # set the roles 
            if rolesData:
                instance.roles.set(rolesData)

            if customPermissionsData:
                instance.custom_permissions.set(customPermissionsData)

            return instance
        except Exception as e:
            raise HTTPException(e.message, e.status_code)
        