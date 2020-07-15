import React, {useState, useContext} from 'react';


const StoreContext = React.createContext({});

const modalState = {
    Component: null,
};

export const StoreProvider = ({ children, store }) => {
  const defaultStore = {
      ...store,
      modalState
  };
  const [storeState, setStore] = useState(defaultStore);
  return (
    <StoreContext.Provider value={{store: storeState, setStore}}>
      {children}
    </StoreContext.Provider>
  )
};


const _hydrateConfigs = {
    'project': {},
    'projects': {},
    'db_profiles': {},
    'db_profile': {
        transformer: (store, data) => {
            return {...store, db_profiles: [...store.db_profiles, data]}
        }
    },
    'classes': {}
};

function _generateHydrateStoreFunctions (setStore) {
    const hydrateStoreFunctions = {};
    for (const prop in _hydrateConfigs) {
        const hydrateConfig = _hydrateConfigs[prop];
        hydrateStoreFunctions[prop] = data => setStore(
            prevStoreState => hydrateConfig.transformer
                ? hydrateConfig.transformer(prevStoreState, data)
                : ({...prevStoreState, [prop]: data})
        )
    }
    return hydrateStoreFunctions
}

export const useStore = () => {
  const {store, setStore} = useContext(StoreContext);
  return {
    getFromStore: path => {
        const pathArray = path.split('.');
        let result = store;
        for (const key of pathArray) {
            if(result === undefined || result === null || typeof result !== 'object') {
                return result
            }
            result = result[key]
        }
        return result
    },

    openModal: Component => setStore(prevState => ({...prevState, modalState: { Component }})),
    closeModal: () => setStore(prevState => ({...prevState, modalState: { Component: null }})),

    hydrateStore: _generateHydrateStoreFunctions(setStore),

    deleteDbProfileFromStore: db_profile_id => setStore(prevState => ({
      ...prevState,
      db_profiles: prevState.db_profiles.filter(profile => profile.db_profile_id !== db_profile_id )
    })),
  }
};
