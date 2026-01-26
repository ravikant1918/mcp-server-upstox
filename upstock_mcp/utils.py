import json
import numpy as np
import pandas as pd
from typing import Any

def to_json_safe(obj: Any) -> Any:
    """
    Recursively convert objects to JSON-safe primitives.
    Handles NumPy types, Pandas types, and NaNs.
    """
    if isinstance(obj, dict):
        return {k: to_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        return [to_json_safe(item) for item in obj]
    elif isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        if np.isnan(obj):
            return None
        return float(obj)
    elif isinstance(obj, (np.ndarray, pd.Series)):
        return to_json_safe(obj.tolist())
    elif isinstance(obj, pd.DataFrame):
        return to_json_safe(obj.to_dict(orient="records"))
    elif pd.isna(obj):
        return None
    elif isinstance(obj, (pd.Timestamp, np.datetime64)):
        return str(obj)
    else:
        return obj

def format_response(data: Any = None, error: Any = None, metadata: dict = None) -> dict:
    """
    Standardize the MCP tool return format.
    """
    response = {
        "success": error is None,
        "data": to_json_safe(data),
        "error": to_json_safe(error),
        "metadata": to_json_safe(metadata or {})
    }
    return response

def format_error(message: str, error_type: str = "StandardError", details: Any = None) -> dict:
    """
    Create a structured error object.
    """
    return {
        "type": error_type,
        "message": message,
        "details": to_json_safe(details)
    }
