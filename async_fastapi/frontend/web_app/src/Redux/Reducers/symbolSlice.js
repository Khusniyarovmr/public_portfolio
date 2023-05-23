import { createSlice } from '@reduxjs/toolkit'

export const symbolSlice = createSlice({
    name: 'symbol',
    initialState: {
        id: 0,
        symbol_name: 'BTCUSDT',
        price: 0,
        ticker_size: 2,
        status: 'TRADING',
        contract_type: 'PERPETUAL'
    },
    reducers: {
        setId: (state, action) => {
            state.id = action.payload.id
        },
        setSymbolName: (state, action) => {
            state.symbol_name = action.payload.symbol_name
        },
        setPrice: (state, action) => {
            state.price = action.payload.price
        },
        setTickerSize: (state, action) => {
            state.ticker_size = action.payload.ticker_size
        },
        setStatus: (state, action) => {
            state.status = action.payload.status
        },
        setContractType: (state, action) => {
            state.contract_type = action.payload.contract_type
        }
    }
})

export const { setId, setSymbolName, setPrice, setTickerSize, setStatus, setContractType } = symbolSlice.actions

export default symbolSlice.reducer


