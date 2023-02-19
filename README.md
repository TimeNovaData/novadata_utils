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
### NovadataModelViewSet
Classe que implementa o create e o update para o ModelViewSet do Django Rest Framework

Exemplo:
```python
from novadata_utils.viewsets import NovadataModelViewSet


class MyViewSet(NovadataModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer
```


### NovadataModelSerializer
Classe que traz a serialização de todos os seus objetos necessários para o front-end.

Exemplo:

```python
from novadata_utils.serializers import NovadataModelSerializer


class MySerializer(NovadataModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'
```

### LoginUsernameEmail
Classe para realizar autenticação com username ou email

Exemplo:
```python
# settings.py
AUTHENTICATION_BACKENDS = [
    "novadata_utils.auth.LoginUsernameEmail",
]
```

### NovadataModelAdmin
Classe para facilitar a criação de ModelAdmin, implmentando diversas funcionalidades.

Exemplo:
```python
from novadata_utils.admin import NovadataModelAdmin


class MyAdmin(NovadataModelAdmin):
    search_fields = [
        'example1',
        'example2',
    ]
```

### reverse_lazy_plus
Classe para redirecionamento avançado.

Funciona como a reverse_lazy do Django, porém aceitando parâmetros GET, # e parâmetros de url.

Exemplo:
```python
from novadata_utils.redirect import reverse_lazy_plus

reverse_lazy_plus(
    'testings',
    url_params=[1, 'type_example'],
    get_params={'mensagem': 'Esta é uma mensagem'},
    '#aba-6',
)
# Output:
# /testings/1/type_example?mensagem=Esta%20é%20uma%20mensagem#aba-6
```
