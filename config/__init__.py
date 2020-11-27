from .development import DevelopmentConfig
from .produce import ProduceConfig

projectConfigs = {
    "development": development,
    "produce": ProduceConfig,
}
