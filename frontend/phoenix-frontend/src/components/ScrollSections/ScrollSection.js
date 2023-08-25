import React from 'react';
import './ScrollSection.css';

export default function ScrollSection({sectionId, text, bgColor, children}) {
    return (
        <div style={{backgroundColor: `${bgColor}`}} className="scroll-section grid  xs:grid-cols-1 sm:grid-cols-3 gap-6 p-4 content-start" id={sectionId}>
            {children}
        </div>
    )
}