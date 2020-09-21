import React from 'react';
import ProfilerModule from 'components/Profiler/ProfilerModule/ProfilerModule';

export default function CachingModule ({isOpen, setOpen}) {
    return (
        <ProfilerModule title='[TODO] Caching Strategies' isOpen={isOpen} setOpen={setOpen}>
            <h3>Caching Strategies</h3>
            <p>Explore how caching strategies can improve performance</p>
        </ProfilerModule>
    )
}