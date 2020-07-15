import React from 'react';
import styles from './styles.scss';


export default function SchoolList ({ list }) {

    return (
        <div>
            <div className={styles.schoolListHeader}>
                <h2>School List</h2>
            </div>

            {list.map((school, i) =>
                <div className={styles.schoolSystem} key={i}>
                    <p>School Id: {school.db_profile_id}</p>
                    <p>School Name: {school.db_profile_name}</p>
                    <p>Number of Classes: {school.classes}</p>
                    <p>Number of Teachers: {school.teachers}</p>
                    <p>Number of Students: {school.students}</p>
                </div>
            )}
        </div>
    )
}