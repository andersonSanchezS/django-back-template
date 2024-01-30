# Rest Framework
from rest_framework import serializers
# Models
from apps.authentication.models import User
# Utils
from apps.base.utils.index import genPassword, genUlid

import bcrypt
# Exceptions
from apps.base.exceptions import HTTPException

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


    def create(self, validated_data):
        try:
            # Generate a random uid
            validated_data['id'] = genUlid()
            # Generate a random password
            password = genPassword(10)
            validated_data['encryptedPassword'] = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
            # Create the new user
            user = User.objects.create(**validated_data)
            return user
        except Exception as e:
            raise HTTPException(e.message, 500)
        