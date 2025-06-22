from __future__ import annotations

from typing import Optional, Dict, Any
import os

from .client import Client


class BinanceTradingClient:
    """Simple wrapper around :class:`Client` for live trading."""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, testnet: bool = False) -> None:
        self.client = Client(api_key=api_key or os.getenv("BINANCE_API_KEY"),
                             api_secret=api_secret or os.getenv("BINANCE_API_SECRET"),
                             testnet=testnet)

    def create_order(self, symbol: str, side: str, order_type: str = "MARKET", quantity: float | None = None,
                     price: float | None = None, **kwargs: Any) -> Dict[str, Any]:
        """Place a new order on Binance."""
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side.upper(),
            "type": order_type.upper(),
        }
        if quantity is not None:
            params["quantity"] = quantity
        if price is not None:
            params["price"] = price
        params.update(kwargs)
        return self.client.create_order(**params)

    def cancel_order(self, symbol: str, order_id: Optional[int] = None, orig_client_order_id: Optional[str] = None) -> Dict[str, Any]:
        """Cancel an existing order."""
        params: Dict[str, Any] = {"symbol": symbol}
        if order_id is not None:
            params["orderId"] = order_id
        if orig_client_order_id is not None:
            params["origClientOrderId"] = orig_client_order_id
        return self.client.cancel_order(**params)

    def get_open_orders(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve current open orders."""
        if symbol:
            return self.client.get_open_orders(symbol=symbol)
        return self.client.get_open_orders()

    def get_account(self) -> Dict[str, Any]:
        """Return current account information."""
        return self.client.get_account()

