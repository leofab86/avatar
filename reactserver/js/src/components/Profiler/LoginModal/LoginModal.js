import React from 'react';
import styles from './styles.scss';

export default function LoginModal () {

    return (
        <div className={styles.loginModal}>
            <h2 className={styles.header}>Sign in to Avatar Profiler</h2>
            <p>
                Welcome to the Avatar Profiler. The purpose of this application is to demonstrate and compare live
                implementations of common web technology stacks that are capable of meeting modern business needs.
            </p>
            <p>
                This includes system designs that can automatically scale to handle high traffic and high data throughput,
                systems that utilize serverless and microservices architecture, and more.
            </p>
            <h4>Why do I need to sign in?</h4>
            <p>
                This application will use <a href='https://aws.amazon.com/cloudformation/' target='_blank'>AWS Cloud Formation</a> to
                launch application stacks specifically for you. These will serve as personal sandboxes where you can
                test them under load, see performance analytics, and generally learn more about the technologies involved.
            </p>
            <p>
                These resources cost money, so they will be shut down after a period of inactivity and you will have
                the option to restart them anytime you return to the site.
            </p>
            <p>
                An account is used to keep track of these application stacks, so you can view and control their status.
            </p>
            <p>
                Please create an account using Github single sign on below. If you prefer not to sign in, some profiling
                features will not be available to you.
            </p>
            <div className={styles.loginButtonContainer}>
                <a className={styles.loginButton} href='/social-auth/login/github/'>Sign in with Github</a>
            </div>
        </div>
    )
}