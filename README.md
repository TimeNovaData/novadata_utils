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
- NovadataModelSerializer, classe que traz a serialização de todos os seus objetos necessários para o front-end
