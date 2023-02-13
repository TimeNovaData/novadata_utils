# novadata utils
Pacote para facilitar o seu dia a dia como programador Django.

## Getting Started
#### Dependências
Django
Django Rest Framework




#### Installation
```shell
pip install novadata-utils
```

Settings.py:
```python
INSTALLED_APPS = [
    ...
    'novadata_utils',
    ...
]
```


## Features
- NovadataModelViewSet, classe que implementa o create e o update para o ModelViewSet do Django Rest Framework
### Usage
```python
from novadata_utils.viewsets import NovadataModelViewSet


class MyViewSet(NovadataModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
```


- NovadataModelSerializer, classe que traz a serialização de todos os seus objetos necessários para o front-end
### Usage
```python
from novadata_utils.serializers import NovadataModelSerializer


class MySerializer(NovadataModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

- LoginUsernameEmail, classe para realizar autenticação com username ou email
### Usage
```python
# settings.py
AUTHENTICATION_BACKENDS = [
    "novadata_utils.auth.LoginUsernameEmail",
]
```
