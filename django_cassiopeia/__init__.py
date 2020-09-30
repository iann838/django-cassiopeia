import cassiopeia
import stores
from .utils import cassiopeia_init, create_pipeline

cassiopeia._configuration.settings.create_pipeline = create_pipeline
cassiopeia.datastores.DjangoCache = stores.DjangoCache
cassiopeia.datastores.Omnistone = stores.Omnistone

cassiopeia.apply_settings(cassiopeia_init())
