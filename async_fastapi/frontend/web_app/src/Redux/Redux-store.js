import {configureStore} from '@reduxjs/toolkit';
import userSlice from "./Reducers/userSlice";
import strategySlice from "./Reducers/strategySlice";
import symbolSlice from "./Reducers/symbolSlice";

export const store = configureStore({
    reducer: {
        user: userSlice,
        strategy: strategySlice,
        symbol: symbolSlice,
    }
});

window.store = store;