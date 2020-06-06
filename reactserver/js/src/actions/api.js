import { useEffect } from 'react';
import Cookie from 'js-cookie';
import { useStore } from 'store';



function buildQueryParams(params) {
    let queryParams = '?';
    for (const paramKey in params) {
        if (params[paramKey]) {
            queryParams += `${paramKey}=${params[paramKey]}&`
        }
    }
    return queryParams
}

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

export const checkDatabaseProgress = db_profile_id => {
    return fetch(window.location.origin + '/profiler/check_progress/' + db_profile_id)
        .then(r => r.json())
};

export const getDatabaseProfile = (db_profile_id, params) => {
    const queryParams = buildQueryParams(params);
    return fetch(window.location.origin + '/profiler/database_profile/' + db_profile_id + queryParams, {
      method: 'GET',
      headers: {
          'X-CSRFToken': Cookie.get('csrftoken')
      },
  }).then(r => r.json())
};

export const deleteDatabaseProfile = db_profile_id => {
    return fetch(window.location.origin + '/profiler/database_profile/' + db_profile_id, {
      method: 'DELETE',
      headers: {
          'X-CSRFToken': Cookie.get('csrftoken')
      },
  }).then(r => r.status)
};