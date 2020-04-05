import React from 'react';
import { useParams } from "react-router-dom";
import { useStore } from 'store';
import { useHydrateStoreOnPageLoad } from 'utils/customHooks.js';
// import styles from './styles.scss';


export default function DetailsPage () {
    const { get } = useStore();
    const project = get('project');
    const { projectId } = useParams();
    const projectNotLoaded = !project || project.id.toString() !== projectId;

    useHydrateStoreOnPageLoad(projectNotLoaded);

    return projectNotLoaded ? null : (
        <div>
            <h3>{project.project_name}</h3>
            <p>{project.project_summary}</p>
            <p>{project.project_description}</p>
        </div>
    )
}