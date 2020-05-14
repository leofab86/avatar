import React, {useState} from 'react';
import cn from 'classnames';
import { useStore } from 'store';
import { createDatabaseProfile, deleteDatabaseProfile, checkDatabaseProgress } from 'actions/api';
import { useUpdateSelectedProfile } from './hooks';
import styles from './styles.scss';


export default function DataModelConfigModule ({ dbProfiles, selectedDbProfile, setSelectedDbProfile }) {
    const {deleteDbProfileFromStore, hydrateStore} = useStore();
    const [progress, setProgress] = useState(null);


    useUpdateSelectedProfile(dbProfiles, setSelectedDbProfile);

    const checkProgress = db_profile => {
        if(db_profile.completion_progress === 100) {
            hydrateStore.db_profile(db_profile);
            setProgress(null)
        } else {
            setProgress(db_profile.completion_progress);
            setTimeout(() => {
                checkDatabaseProgress(db_profile.db_profile_id)
                    .then(({ db_profile }) => checkProgress(db_profile))
            }, 800);
        }
    };

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
                checkProgress(db_profile)
            }
        })
    };

    const deleteProfile = () =>
        deleteDatabaseProfile(selectedDbProfile)
            .then(status => status === 200 && deleteDbProfileFromStore(selectedDbProfile));

    return (
        <div className={cn('profilerModule', styles.dataModelConfigModule)}>
            <h3>Data Model Config</h3>
            <p>
                Create a set of data using a school system model. Choose the number of classes, teachers and
                students. With high values, this can generate a pretty complex hierarchical data
                structure that will affect system performance necessitating thoughtful optimization of your
                queries.
            </p>

            <div className={styles.savedConfigs}>
                <h4 className={styles.savedConfigsHeader}>Select from existing configs:</h4>
                <select
                    className={styles.savedConfigsSelect}
                    value={selectedDbProfile}
                    onChange={e => setSelectedDbProfile(e.target.value)}
                >
                  {dbProfiles?.map(dbProfile =>
                      <option value={dbProfile.db_profile_id} key={dbProfile.db_profile_id}>
                          {dbProfile.db_profile_name}
                      </option>
                  )}
                </select>
                <button className={'profilerButton'} type='button' onClick={deleteProfile}>Delete Profile</button>
            </div>

            <h4 className={styles.configFormHeader}>Create new config:</h4>
            <form className={styles.configForm} onSubmit={onSubmit}>
                <label htmlFor="db_profile_name">Database Profile Name</label>
                <input type="text" id="db_profile_name"/>

                <label htmlFor="classes">Number of Classes</label>
                <input type="number" id="classes" />

                <label htmlFor="class_types">Number of Class Types (maximum 16)</label>
                <input type="number" id="class_types"/>

                <label htmlFor="teachers">Number of Teachers</label>
                <input type="number" id="teachers"/>

                <label htmlFor="classes_per_teacher">Classes per Teacher</label>
                <input type="number" id="classes_per_teacher"/>

                <label htmlFor="students">Number of Students</label>
                <input type="number" id="students"/>

                <label htmlFor="classes_per_student">Classes per Student</label>
                <input type="number" id="classes_per_student"/>

                <div className={styles.submitRow}>
                    <button
                        className={cn('profilerButton', styles.configFormSubmitButton)}
                        type="submit"
                    >
                        Create
                    </button>

                    {progress !== null && (
                        <div className={styles.progressBar}>
                            <div className={styles.progressBarFill} style={{ width: `${progress <= 5 ? 5 :progress}%` }}/>
                        </div>
                    )}
                </div>

            </form>
        </div>
    )
}