import { useEffect } from 'react';
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