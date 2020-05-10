import React from 'react';
import { Link } from "react-router-dom";
import { useStore } from 'store';
import { useHydrateStoreOnPageLoad } from 'actions';
import styles from './styles.scss';


export default function Home () {
    const projects = useStore().getFromStore('projects');

    useHydrateStoreOnPageLoad(!projects);

    return (
        <div className={styles.testModule}>
            {projects?.map(project =>
                <Link key={project.id} to={`/details/${project.id}`}>
                    <div  className={styles.project}>
                        <h3>{project.project_name}</h3>
                        <pre>{project.project_summary}</pre>
                    </div>
                </Link>
            )}
        </div>
    )
}