import { applyMiddleware, combineReducers, createStore } from 'redux'
import thunk from 'redux-thunk'
import { persistStore } from 'redux-persist'
import { CookieStorage } from 'redux-persist-cookie-storage'
import Cookies from 'cookies-js'
import { accessReducer } from './reducers/tokenStorage/accessStore'
import persistReducer from 'redux-persist/es/persistReducer'
import { authReducer } from './reducers/authStorage/authStore'


const accessPersistConfig = {
  key: 'accessToken',
  storage: new CookieStorage(Cookies, {
    expiration: {
      'default': 86400 // one day
    }
  }),
  whitelist: ['accessToken']
}

const authStatusPersistConfig = {
  key: 'authStatus',
  storage: new CookieStorage(Cookies, {
    expiration: {
      'default': 86400
    }
  }),
  whitelist: ['authStatus']
}


const rootReducer = combineReducers({
  accessToken:persistReducer(accessPersistConfig, accessReducer),
  authStatus:persistReducer(authStatusPersistConfig, authReducer),
})


export const store = createStore(rootReducer, applyMiddleware(thunk));
export const persistor = persistStore(store, {});