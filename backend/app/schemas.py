"""
Pydantic schemas and schemas validation constraints for the Customer Segmentation API.
"""
from pydantic import BaseModel, Field

class CustomerInput(BaseModel):
    """
    Schema for validating customer RFM features submitted for segment prediction.
    All attributes represent positive metrics.
    """
    recency: float = Field(
        ..., 
        ge=0, 
        description="Recency (Days since last purchase). Must be non-negative."
    )
    frequency: float = Field(
        ..., 
        ge=0, 
        description="Frequency (Number of unique invoices). Must be non-negative."
    )
    monetary: float = Field(
        ..., 
        ge=0, 
        description="Monetary (Total spending value). Must be non-negative."
    )
