const SET_ACCESS = 'access/SET_ACCESS';

export const accessReducer = (state = {accessToken:""}, action) => {
  switch (action.type) {
    case SET_ACCESS: {
      return {accessToken: action.payload};
    }
    default:
      return state;
  }
};


export const setAccessAction = (payload) => ({ type: SET_ACCESS, payload });



