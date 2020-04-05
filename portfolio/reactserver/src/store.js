import React, {useState, useContext} from 'react';


const StoreContext = React.createContext({});

export const StoreProvider = ({ children, store }) => {
  const [storeState, setStore] = useState(store);
  return (
    <StoreContext.Provider value={{store: storeState, setStore}}>
      {children}
    </StoreContext.Provider>
  )
};

export const useStore = () => {
  const {store, setStore} = useContext(StoreContext);
  return {
    get: path => {
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

    hydrateStore: {
        project: project => setStore(prevState => ({...prevState, project})),
        projects: projects => setStore(prevState => ({...prevState, projects})),
    }
  }
};
