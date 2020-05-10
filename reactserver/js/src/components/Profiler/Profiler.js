import React, { useState, useEffect } from 'react';
import { useStore } from 'store';
import { useHydrateStoreOnPageLoad, createDatabaseProfile, deleteDatabaseProfile } from 'actions';
import styles from './styles.scss';


export default function Profiler () {
    const {getFromStore, hydrateStore, deleteDbProfileFromStore} = useStore();
    const dbProfiles = getFromStore('db_profiles');
    const [selectedDbProfile, setSelectedDbProfile] = useState(dbProfiles?.[0]?.db_profile_id);

    useHydrateStoreOnPageLoad(!dbProfiles);

    useEffect(function updateSelectedDbProfile_whenDbProfilesChange () {
        setSelectedDbProfile(dbProfiles?.[0]?.db_profile_id || '')
    }, [dbProfiles]);

    const onSubmit = (e) => {
        e.preventDefault();
        const form = e.target;
        const db_profile_name = form.querySelector('#db_profile_name').value;
        const classes = form.querySelector('#classes').value;
        const class_types = form.querySelector('#class_types').value;
        const teachers = form.querySelector('#teachers').value;
        const classes_per_teacher = form.querySelector('#classes_per_teacher').value;
        const students = form.querySelector('#students').value;
        const classes_per_student = form.querySelector('#classes_per_student').value;

        createDatabaseProfile({
            db_profile_name,
            classes,
            class_types,
            teachers,
            classes_per_teacher,
            students,
            classes_per_student
        }).then(({ db_profile }) => {
            if(db_profile) {
                hydrateStore.db_profile(db_profile)
            }
        })
    };

    const deleteProfile = () => {
        deleteDatabaseProfile(selectedDbProfile).then(r => {
            if (r === 200 || r === 404) {
                deleteDbProfileFromStore(selectedDbProfile)
            }
        })
    };

    return (
        <div>
            <h3>Database Config:</h3>
            <div>
                <select value={selectedDbProfile} onChange={e => setSelectedDbProfile(e.target.value)}>
                  {dbProfiles?.map(dbProfile =>
                      <option value={dbProfile.db_profile_id} key={dbProfile.db_profile_id}>
                          {dbProfile.db_profile_name}
                      </option>
                  )}
                </select>
                <button type='button' onClick={deleteProfile}>Delete Profile</button>
            </div>

            <form className={styles.databaseProfileForm} onSubmit={onSubmit}>
                <label htmlFor="db_profile_name">Database Profile Name</label>
                <input type="text" id="db_profile_name"/>

                <label htmlFor="classes">Number of Classes</label>
                <input type="number" id="classes" />

                <label htmlFor="class_types">Number of class types</label>
                <input type="number" id="class_types"/>

                <label htmlFor="teachers">Number of Teachers</label>
                <input type="number" id="teachers"/>

                <label htmlFor="classes_per_teacher">Classes per Teacher</label>
                <input type="number" id="classes_per_teacher"/>

                <label htmlFor="students">Number of Students</label>
                <input type="number" id="students"/>

                <label htmlFor="classes_per_student">Classes per Student</label>
                <input type="number" id="classes_per_student"/>

                <button type="submit">Create</button>
            </form>
        </div>
    )
}