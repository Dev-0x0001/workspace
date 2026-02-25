import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const fetchUser = createAsyncThunk('user/fetch', async () => {
  const response = await fetch('/api/user');
  return response.json();
});

const userSlice = createSlice({
  name: 'user',
  initialState: { id: null, name: '', email: '' },
  reducers: {
    logout: (state) => {
      state.id = null;
      state.name = '';
      state.email = '';
    }
  },
  extraReducers: (builder) => {
    builder.addCase(fetchUser.fulfilled, (state, action) => {
      state.id = action.payload.id;
      state.name = action.payload.name;
      state.email = action.payload.email;
    });
  }
});

export const { logout } = userSlice.actions;
export default userSlice;