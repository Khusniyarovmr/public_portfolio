import { createSlice } from '@reduxjs/toolkit'

export const userSlice = createSlice({
    name: 'user',
    initialState: {
        username: 'nickname',
        email: 'example@gmail.com',
        role_id: 1,
        is_superuser: 0,
        first_name: '',
        last_name: '',
        telegram_chat_id: 10000000,
    },
    reducers: {
        setUserName: (state, action) => {
            state.username = action.payload.username
        },
        setEmail: (state, action) => {
            state.email = action.payload.email
        },
        setRoleId: (state, action) => {
            state.role_id = action.payload.role_id
        },
        setIsSuperuser: (state, action) => {
            state.is_superuser = action.payload.is_superuser
        },
        setFirstName: (state, action) => {
            state.first_name = action.payload.first_name
        },
        setLastName: (state, action) => {
            state.last_name = action.payload.last_name
        },
        setTelegramChatId: (state, action) => {
            state.telegram_chat_id = action.payload.telegram_chat_id
        },
        setUserInfo: (state, action) => {
            Object.assign(state, action.payload);
        }
    }
})

export const {
    setUserName,
    setEmail,
    setRoleId,
    setIsSuperuser,
    setFirstName,
    setLastName,
    setTelegramChatId,
    setUserInfo
} = userSlice.actions

export default userSlice.reducer