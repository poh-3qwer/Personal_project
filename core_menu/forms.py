from django.forms import ModelForm
from core_menu.models import Instrument


class InstrumentForm(ModelForm):

    class Meta:
        model = Instrument
        fields = ['category',
                  'name',
                  'production_year',
                  'serial_number',
                  'manufacturer',
                  'brand',
                  'product_condition',
                  'complectation',
                  'instrument_image',
                  'price',
                  ]