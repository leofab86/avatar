import { useEffect, useRef } from 'react';

export function useUpdateSelectedProfile(dbProfiles, setSelectedDbProfile) {
    const prevProfilesLength = useRef(dbProfiles.length);

    useEffect(function updateSelectedDbProfile_onDbProfilesChange() {
        const firstDbProfiles = prevProfilesLength.current === 0 && dbProfiles.length > 0;
        const dbProfileRemoved = prevProfilesLength.current > dbProfiles.length;
        const dbProfilesIncreased = prevProfilesLength !== 0 && prevProfilesLength.current < dbProfiles.length;

        if(firstDbProfiles || dbProfileRemoved) {
            setSelectedDbProfile(dbProfiles[0]?.db_profile_id || '')
        }

        if(dbProfilesIncreased) {
            setSelectedDbProfile(dbProfiles[dbProfiles.length - 1].db_profile_id)
        }
        prevProfilesLength.current = dbProfiles.length;
    }, [dbProfiles])
}