# Rest Framework
from rest_framework import serializers
# Models
from apps.misc.models import Category, SubCategory
from django.db        import transaction
# Utils 
from apps.base.utils.index import ExtraFieldSerializer
from apps.base.exceptions import HTTPException


class CategorySerializer(serializers.ModelSerializer):
    subCategories = ExtraFieldSerializer(source='*', required=False)

    class Meta:
        model = Category
        fields = "__all__"
        extra_kwargs = {
                "description": { "error_messages": { "required": "La descripción es requerida", } },
                "code"       : { "error_messages": { "required": "El código es requerido" } }  
                }
        
    @transaction.atomic
    def create(self, validated_data):
        try:
            subCategoriesData = validated_data.pop('subCategories', [])
            category          =  Category.objects.create(**validated_data)

            if subCategoriesData:
                for subCategoryData in subCategoriesData:
                    SubCategory.objects.create(category=category,user_created_at=validated_data['user_created_at'], **subCategoryData)

            return category
        except Exception as e:
            raise HTTPException(str(e), 400)

    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            # update the category
            instance.description = validated_data.get('description', instance.description)
            instance.code        = validated_data.get('code', instance.code)
            instance.save()

            # update the subCategories
            subCategoriesData = validated_data.pop('subCategories', [])

            for subCategoryData in subCategoriesData:
                subCategoryId = subCategoryData.get('id', None)
                if subCategoryId:
                    subCategory                 = SubCategory.objects.get(id=subCategoryId)
                    subCategory.description     = subCategoryData.get('description', subCategory.description)
                    subCategory.code            = subCategoryData.get('code', subCategory.code)
                    subCategory.user_updated_at = validated_data['user_updated_at']
                    subCategory.save()
                else:
                    SubCategory.objects.create(category=instance,user_created_at=validated_data['user_updated_at'] **subCategoryData)

            return instance
        except Exception as e:
            raise HTTPException(str(e), 400)

    def to_representation(self, instance):
        representation                  = super().to_representation(instance)
        subCategories                   = SubCategory.objects.filter(category=instance)
        representation['subCategories'] = [{ 'id': subCategory.id, 'code': subCategory.code, 'description': subCategory.description } for subCategory in subCategories]
        return representation

