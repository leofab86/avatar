import { useEffect } from 'react';
import Cookie from 'js-cookie';
import { useStore } from 'store';


export const useHydrateStoreOnPageLoad = (conditional) => {
    const { hydrateStore } = useStore();
    useEffect(function hydratePageAfterMount () {
        if(conditional) {
            fetch(window.location.href + '?json=true').then(r => r.json())
                .then(resp => {
                    for (const key in resp) {
                        hydrateStore[key]?.(resp[key])
                    }
                })
        }
    }, []);
};

export const createDatabaseProfile = (data) => {
  return fetch(window.location.origin + '/profiler/create_database_profile', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookie.get('csrftoken')
      },
      body: JSON.stringify(data)
  }).then(r => r.json())
};

export const deleteDatabaseProfile = db_profile_id => {
    return fetch(window.location.origin + '/profiler/delete_database_profile', {
      method: 'DELETE',
      headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': Cookie.get('csrftoken')
      },
      body: JSON.stringify({db_profile_id})
  }).then(r => r.status)
};