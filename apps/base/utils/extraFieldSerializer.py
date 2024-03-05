from rest_framework import serializers


class ExtraFieldSerializer(serializers.Serializer): 
    callback_to_representation= None 
    def __init__(self, *args, **kwargs): 
        self.callback_to_representation = kwargs.pop('callback_to_representation',None) 
        super(ExtraFieldSerializer, self).__init__(*args, **kwargs) 
    def to_representation(self, instance): 
        # this would have the same as body as in a SerializerMethodField 
        return self.callback_to_representation(instance) if self.callback_to_representation is not None else None 
    
    def to_internal_value(self, data): 
        # This must return a dictionary that will be used to 
        # # update the caller's validation data, i.e. if the result 
        # # produced should just be set back into the field that this 
        # # serializer is set to, return the following: 
        return { self.field_name:data 
                # self.field_name: 'Any python object made with data: %s' % data 
            }