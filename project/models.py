from pydantic import BaseModel, Field

class StockQuery(BaseModel):
    ticker: str = Field(None, description="The stock ticker symbol", example="AAPL")
    period: str = Field(..., description="The period for fetching stock data (e.g., '1mo', '3mo', '1y')", example="1mo")
    file_name: str = Field(..., description="The Excel file name to save the data", example="stock_data.xlsx")
    close_price: float = Field(None, description="The closing price to filter stocks", example=3000.0)
