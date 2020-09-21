import React from 'react';
import ProfilerModule from 'components/Profiler/ProfilerModule/ProfilerModule';

export default function MicroservicesModule ({isOpen, setOpen}) {
    return (
        <ProfilerModule title='[TODO] Microservices' isOpen={isOpen} setOpen={setOpen}>
            <h3>Microservices</h3>
            <p>
                Explore how splitting up the app's functionality into containers and AWS serverless services like AWS Fargate
                can change the various metrics, like how auto scaling dynamics change, and how spinning up new stacks
                should be easier/faster.
            </p>
            <p>
                • DB should be its own microservice instead of being attached to the web server instance.
            </p>
            <p>
                • Make the node react rendering server for Server Side Rendering its own microservice, AWS Lambda
                should be able to take care of that
            </p>
            <p>
                • Could the whole web server be AWS Lambda? Would need to find solution for authorization. Disadvantage
                of this architecture would be losing built in functionality of a framework like Django (ORM, Authorization and Admin pages).
            </p>
        </ProfilerModule>
    )
}