# cookiecutter_flag {%- if cookiecutter.enable_jwt == 'True' %}
from .abstract_authentication import AbstractAuthentication
from .authenticate import Authentication
# cookiecutter_flag {%- endif %}
