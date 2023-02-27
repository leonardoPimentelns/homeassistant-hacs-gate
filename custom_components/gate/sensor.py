"""Platform for sensor integration."""
from __future__ import annotations

from datetime import timedelta,datetime
import logging
import voluptuous
from __future__ import print_function
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


KEY = 'key'=
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
        self._attr_name = self.config[NAME]
        self.event = None
        self.data = []
        


    @property
    def icon(self):
        """Return icon."""
        return "mdi:soccer"


    @util.Throttle(UPDATE_FREQUENCY)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        
        spot_currency = None
        spot_available = None
        spot_locked = None
        spot_total_available = None

        configuration = gate_api.Configuration(
            host = "https://api.gateio.ws/api/v4",
            key = self.config[KEY],
            secret = self.config[SECRET]
        )


        api_client = gate_api.ApiClient(configuration)
        # Create an instance of the API class
        api_instance = gate_api.WalletApi(api_client)
        api_spot_instance = gate_api.SpotApi(api_client)

        api_response = api_spot_instance.list_tickers(currency_pair ='sdao_usdt')


        currency = 'USDT' # str | Currency unit used to calculate the balance amount. BTC, CNY, USD and USDT are allowed. USDT is the default. (optional) (default to 'USDT')
        # print(spot.list_all_open_orders())

        def get_spot_list():
            api_response = api_instance.get_total_balance(currency=currency)
            print(round(float(api_response.details['spot'].amount),2))

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

                    tickers_value = round(float(tickers[0].last),2)

                    tickers_total = (tickers_value*spot_total)
                    result= {'spot_currency':spot_currency,
                             'icon':icon,
                             'price':tickers_value,
                             'price_total':tickers_total,
                             'quant_available':spot_available,
                             'quant_locked':spot_locked,
                             'spot_total':spot_total
                            }
                    self.data.append(result)
   

        
        
            


    @property
    def extra_state_attributes(self):
        """Return device specific state attributes."""
        self._attributes = {
            "logo": self.data ,

        }
        return  self._attributes



