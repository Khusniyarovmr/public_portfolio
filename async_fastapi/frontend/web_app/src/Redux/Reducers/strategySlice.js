import { createSlice } from '@reduxjs/toolkit'

export const strategySlice = createSlice({
    name: 'strategy',
    initialState: {
        name: "new_strategy",
        user_id: 0,
        symbol_id: 0,
        symbol_name: 'BTCUSDT',
        signal_name: '',
        type: '',
        stock_market: 'Binance',
        lot_quantity: 0,
        lot_percent: 0,
        leverage: 10,
        tp_margin: 0.2,
        tp_price: 0.02,
        tp_count: 3,
        tp_enable: 1,
        sl_margin: 0.2,
        sl_price: 0.02,
        sl_enable: 0,
    },
    reducers: {
        setName: (state, action) => {
            state.name = action.payload.name
        },
        setUserId: (state, action) => {
            state.user_id = action.payload.user_id
        },
        setSymbolId: (state, action) => {
            state.symbol_id = action.payload.symbol_id
        },
        setSymbolName: (state, action) => {
            state.symbol_name = action.payload.symbol_name
        },
        setSignalName: (state, action) => {
            state.signal_name = action.payload.signal_name
        },
        setLotQuantity: (state, action) => {
            state.lot_quantity = action.payload.lot_quantity
        },
        setLotPercent: (state, action) => {
            state.lot_percent = action.payload.lot_percent
        },
        setLeverage: (state, action) => {
            state.leverage = action.payload.leverage
        },
        setTpMargin: (state, action) => {
            state.tp_margin = action.payload
        },
        setTpPrice: (state, action) => {
            state.tp_price = action.payload.tp_price
        },
        setTpCount: (state, action) => {
            state.tp_count = action.payload.tp_count
        },
        setTpEnable: (state, action) => {
            state.tp_enable = action.payload.tp_enable
        },
        setSlMargin: (state, action) => {
            state.sl_margin = action.payload.sl_margin
        },
        setSlPrice: (state, action) => {
            state.sl_price = action.payload.sl_price
        },
        setSlEnable: (state, action) => {
            state.sl_enable = action.payload.sl_enable
        }
    }
})

export const {
    setName,
    setUserId,
    setSymbolId,
    setSymbolName,
    setSignalName,
    setLotQuantity,
    setLotPercent ,
    setLeverage,
    setTpMargin,
    setTpPrice,
    setTpCount,
    setTpEnable,
    setSlMargin,
    setSlPrice,
    setSlEnable,
} = strategySlice.actions

export default strategySlice.reducer