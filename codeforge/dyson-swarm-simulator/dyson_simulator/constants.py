from typing import Final

# Physical Constants (in SI units)
SOLAR_LUMINOSITY: Final[float] = 3.828e26  # Watts
SOLAR_MASS: Final[float] = 1.989e30  # Kilograms
ASTRONOMICAL_UNIT: Final[float] = 1.496e11  # Meters
SPEED_OF_LIGHT: Final[float] = 299792458  # Meters per second
GRAVITATIONAL_CONSTANT: Final[float] = 6.67430e-11  # m³/kg/s²

# Dyson Swarm Parameters
DYSON_CAPTURE_EFFICIENCY: Final[float] = 0.95  # 95% efficiency
MINIMUM_COLLECTOR_AREA: Final[float] = 1000.0  # Square meters
MAX_LAUNCH_MASS_RATE: Final[float] = 1000000.0  # Kilograms per year
TARGET_CAPTURE_PERCENT: Final[float] = 0.50  # 50% of solar luminosity

# Material Properties
SILICON_DENSITY: Final[float] = 2330.0  # kg/m³
ALUMINUM_DENSITY: Final[float] = 2700.0  # kg/m³
SILICON_ATOMIC_MASS: Final[float] = 28.0855  # g/mol
AVOGADRO_CONSTANT: Final[float] = 6.02214076e23  # 1/mol

# Economic and Manufacturing Constants
MANUFACTURING_COST_PER_KG: Final[float] = 1000.0  # USD per kilogram
TRANSPORT_COST_PER_KG: Final[float] = 500.0  # USD per kilogram
ANNUAL_BUDGET: Final[float] = 1e12  # USD per year

# Time Constants
SECONDS_PER_YEAR: Final[int] = 31536000
SECONDS_PER_DAY: Final[int] = 86400
SECONDS_PER_HOUR: Final[int] = 3600

# Simulation Configuration
DEFAULT_SIMULATION_YEARS: Final[int] = 100
DEFAULT_TIMESTEP_YEARS: Final[float] = 1.0
DEFAULT_OUTPUT_INTERVAL: Final[int] = 10

# Validation thresholds
MIN_VALID_CAPTURE_PERCENT: Final[float] = 0.01
MAX_VALID_CAPTURE_PERCENT: Final[float] = 0.99
MIN_VALID_MASS_RATE: Final[float] = 1.0
MAX_VALID_MASS_RATE: Final[float] = 1e10

# Error margins
ENERGY_CALCULATION_ERROR_MARGIN: Final[float] = 1e-9
MASS_CALCULATION_ERROR_MARGIN: Final[float] = 1e-6

# Additional constants
EARTH_MASS: Final[float] = 5.972e24  # kg
AU: Final[float] = ASTRONOMICAL_UNIT