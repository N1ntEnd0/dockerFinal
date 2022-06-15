const SET_AUTH = 'auth/SET_STATUS';

export const authReducer = (state = {authStatus:false}, action) => {
  switch (action.type) {
    case SET_AUTH: {
      return {authStatus: action.payload};
    }
    default:
      return state;
  }
};

export const setAuthStatusAction = (payload) => ({ type: SET_AUTH, payload });



