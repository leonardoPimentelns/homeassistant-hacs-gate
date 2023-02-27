"""Platform for sensor integration."""
from __future__ import annotations
from datetime import timedelta,datetime
import logging
import voluptuous
import gate_api
from gate_api.exceptions import ApiException, GateApiException

from homeassistant import const
from homeassistant.helpers import entity
from homeassistant import util
from homeassistant.helpers import config_validation
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
_LOGGER = logging.getLogger(__name__)


KEY = 'key'
SECRET ='secret'
UPDATE_FREQUENCY = timedelta(seconds=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(KEY): cv.string,
        vol.Required(SECRET): cv.string,
        
    }
)
def setup_platform(
    hass,
    config,
    add_entities,
    discovery_info
):
    """Set up the Espn sensors."""
    add_entities([GateSensor(config)],True)


class GateSensor(entity.Entity):
    """Representation of a Espn sensor."""

    def __init__(self,config):
        """Initialize a new Espn sensor."""
        self.config = config
        self._attr_name = "gate"
        self.event = None
        self.data = None
        


    @property
    def icon(self):
        """Return icon."""
        return "mdi:soccer"


    @util.Throttle(UPDATE_FREQUENCY)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant."""

        self.data = get_spot_list(self.config)


    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""
        self._attributes = {
            "logo": self.data ,

        }
        return  self._attributes



def get_spot_list(config):
    spot_currency = None
    spot_available = None
    spot_locked = None
    spot_total_available = None
    data = []

    configuration = gate_api.Configuration(
        host = "https://api.gateio.ws/api/v4",
        key = config[KEY],
        secret = config[SECRET]
    )


    api_client = gate_api.ApiClient(configuration)
    api_instance = gate_api.WalletApi(api_client)
    api_spot_instance = gate_api.SpotApi(api_client)

    api_response = api_spot_instance.list_tickers(currency_pair ='sdao_usdt')


    currency = 'USDT' 

    api_response = api_instance.get_total_balance(currency=currency)
    

    spot = gate_api.SpotApi(api_client)
    spot_list = spot.list_spot_accounts()
    for item in spot_list:
        if item.available > '1':
            spot_currency = item.currency
            spot_available = round(float(item.available),2)
            spot_locked =    round(float(item.locked),2)
            spot_total = (spot_available + spot_locked)
            wallet_amount = api_response.details['spot'].amount
            amount_currency = api_response.details['spot'].currency
            icon = f"https://www.gate.io/images/coin_icon/64/{spot_currency.lower()}.png"
            tickers = api_spot_instance.list_tickers(currency_pair =f"{item.currency}_USDT")

            tickers_value = float(tickers[0].last)

            tickers_total = (tickers_value*spot_total)
            result= {'spot_currency':spot_currency,
                        'icon':icon,
                        'price':tickers_value,
                        'price_total':tickers_total,
                        'quant_available':spot_available,
                        'quant_locked':spot_locked,
                        'spot_total':spot_total
                    }
            data.append(result)
    return data
